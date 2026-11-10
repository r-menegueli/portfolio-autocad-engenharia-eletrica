[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BatchCommand,

    [Parameter(Mandatory = $true)]
    [string]$EvidencePath,

    [string[]]$StartupOptions = @(),

    [double]$MinimumFreeRamGB = 0.20,

    [double]$MaximumCommitRatio = 0.95,

    [int]$SampleIntervalMilliseconds = 500,

    [int]$MaximumRuntimeSeconds = 900,

    [string]$MatlabPath = 'C:\Program Files\MATLAB\R2026a\bin\matlab.exe'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-MemoryState {
    $os = Get-CimInstance Win32_OperatingSystem
    $perf = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory -ErrorAction SilentlyContinue
    [pscustomobject]@{
        free_physical_ram_gb = [math]::Round([double]$os.FreePhysicalMemory / 1MB, 3)
        committed_gb = if ($perf) { [math]::Round([double]$perf.CommittedBytes / 1GB, 3) } else { $null }
        commit_limit_gb = if ($perf) { [math]::Round([double]$perf.CommitLimit / 1GB, 3) } else { $null }
        commit_ratio = if ($perf -and $perf.CommitLimit) { [math]::Round([double]$perf.CommittedBytes / [double]$perf.CommitLimit, 4) } else { $null }
    }
}

function Get-DescendantProcessIds {
    param([int]$RootProcessId)
    $cim = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
    $ids = [System.Collections.Generic.HashSet[int]]::new()
    [void]$ids.Add($RootProcessId)
    $changed = $true
    while ($changed) {
        $changed = $false
        foreach ($item in $cim) {
            $parentId = [int]$item.ParentProcessId
            $processId = [int]$item.ProcessId
            if ($ids.Contains($parentId) -and -not $ids.Contains($processId)) {
                [void]$ids.Add($processId)
                $changed = $true
            }
        }
    }
    return @($ids)
}

function Stop-OwnedProcessTree {
    param([int]$RootProcessId)
    $ids = @(Get-DescendantProcessIds -RootProcessId $RootProcessId | Sort-Object -Descending)
    foreach ($processId in $ids) {
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            try { $process.Kill() } catch { }
        }
    }
}

if (-not (Test-Path -LiteralPath $MatlabPath -PathType Leaf)) {
    throw "Executável MATLAB não encontrado: $MatlabPath"
}
foreach ($option in $StartupOptions) {
    if ($option -notin @('-nojvm', '-singleCompThread')) {
        throw "Opção de inicialização não permitida pelo medidor: $option"
    }
}

$evidenceFullPath = [System.IO.Path]::GetFullPath($EvidencePath)
$evidenceDirectory = Split-Path -Parent $evidenceFullPath
if (-not (Test-Path -LiteralPath $evidenceDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $evidenceDirectory -Force | Out-Null
}

$before = Get-MemoryState
$started = Get-Date
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $MatlabPath
foreach ($option in $StartupOptions) { $psi.ArgumentList.Add($option) }
$psi.ArgumentList.Add('-batch')
$psi.ArgumentList.Add($BatchCommand)
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$process = [System.Diagnostics.Process]::Start($psi)
$rootProcessId = $process.Id
$stdoutTask = $process.StandardOutput.ReadToEndAsync()
$stderrTask = $process.StandardError.ReadToEndAsync()
$samples = [System.Collections.Generic.List[object]]::new()
$peakTreeWorkingSetMB = 0.0
$peakTreePrivateMB = 0.0
$minimumFreeGB = [double]$before.free_physical_ram_gb
$peakCommittedGB = [double]$before.committed_gb
$stopReason = $null

while (-not $process.HasExited) {
    Start-Sleep -Milliseconds $SampleIntervalMilliseconds
    $process.Refresh()
    $memory = Get-MemoryState
    $ids = @(Get-DescendantProcessIds -RootProcessId $rootProcessId)
    $tree = [System.Collections.Generic.List[object]]::new()
    $sumWorkingSet = 0.0
    $sumPrivate = 0.0
    foreach ($processId in $ids) {
        $item = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($item) {
            $ws = [double]$item.WorkingSet64 / 1MB
            $private = [double]$item.PrivateMemorySize64 / 1MB
            $sumWorkingSet += $ws
            $sumPrivate += $private
            $tree.Add([pscustomobject]@{
                pid = $processId
                name = $item.ProcessName
                working_set_mb = [math]::Round($ws, 1)
                private_bytes_mb = [math]::Round($private, 1)
            })
        }
    }
    $peakTreeWorkingSetMB = [math]::Max($peakTreeWorkingSetMB, $sumWorkingSet)
    $peakTreePrivateMB = [math]::Max($peakTreePrivateMB, $sumPrivate)
    $minimumFreeGB = [math]::Min($minimumFreeGB, [double]$memory.free_physical_ram_gb)
    if ($null -ne $memory.committed_gb) {
        $peakCommittedGB = [math]::Max($peakCommittedGB, [double]$memory.committed_gb)
    }
    $samples.Add([pscustomobject]@{
        elapsed_seconds = [math]::Round(((Get-Date) - $started).TotalSeconds, 2)
        free_physical_ram_gb = $memory.free_physical_ram_gb
        committed_gb = $memory.committed_gb
        commit_limit_gb = $memory.commit_limit_gb
        matlab_process_tree_working_set_mb = [math]::Round($sumWorkingSet, 1)
        matlab_process_tree_private_mb = [math]::Round($sumPrivate, 1)
        processes = @($tree)
    })

    if ([double]$memory.free_physical_ram_gb -lt $MinimumFreeRamGB) {
        $stopReason = "Interrompida com segurança: RAM física livre abaixo de $MinimumFreeRamGB GB."
        Stop-OwnedProcessTree -RootProcessId $rootProcessId
        break
    }
    if ($null -ne $memory.commit_ratio -and [double]$memory.commit_ratio -gt $MaximumCommitRatio) {
        $stopReason = "Interrompida com segurança: commit acima de $([math]::Round($MaximumCommitRatio * 100))% do limite."
        Stop-OwnedProcessTree -RootProcessId $rootProcessId
        break
    }
    if (((Get-Date) - $started).TotalSeconds -gt $MaximumRuntimeSeconds) {
        $stopReason = "Interrompida com segurança: ultrapassou $MaximumRuntimeSeconds segundos."
        Stop-OwnedProcessTree -RootProcessId $rootProcessId
        break
    }
}

try { $process.WaitForExit(10000) | Out-Null } catch { }
$after = Get-MemoryState
$ended = Get-Date
$exitCode = if ($process.HasExited) { $process.ExitCode } else { $null }
$stdout = if ($stdoutTask.IsCompleted) { $stdoutTask.Result } else { '' }
$stderr = if ($stderrTask.IsCompleted) { $stderrTask.Result } else { '' }
$result = [ordered]@{
    started_at = $started.ToString('o')
    ended_at = $ended.ToString('o')
    duration_seconds = [math]::Round(($ended - $started).TotalSeconds, 2)
    matlab_path = $MatlabPath
    startup_options = @($StartupOptions)
    matlab_root_process_id = $rootProcessId
    batch_command = $BatchCommand
    exit_code = $exitCode
    stop_reason = $stopReason
    ram_before = $before
    minimum_free_physical_ram_gb = [math]::Round($minimumFreeGB, 3)
    peak_process_tree_working_set_mb = [math]::Round($peakTreeWorkingSetMB, 1)
    peak_process_tree_private_mb = [math]::Round($peakTreePrivateMB, 1)
    peak_system_committed_gb = [math]::Round($peakCommittedGB, 3)
    ram_after = $after
    released_free_ram_gb = [math]::Round([double]$after.free_physical_ram_gb - [double]$minimumFreeGB, 3)
    stdout = $stdout
    stderr = $stderr
    samples = @($samples)
}
$json = $result | ConvertTo-Json -Depth 9
[System.IO.File]::WriteAllText($evidenceFullPath, $json + "`n", [System.Text.UTF8Encoding]::new($false))
Write-Output "MATLAB_EXIT_CODE=$exitCode"
Write-Output "DURATION_SECONDS=$($result.duration_seconds)"
Write-Output "MIN_FREE_RAM_GB=$($result.minimum_free_physical_ram_gb)"
Write-Output "PEAK_PROCESS_TREE_WORKING_SET_MB=$($result.peak_process_tree_working_set_mb)"
Write-Output "PEAK_COMMITTED_GB=$($result.peak_system_committed_gb)"
Write-Output "STOP_REASON=$stopReason"
Write-Output "EVIDENCE=$evidenceFullPath"
if ($stdout) { Write-Output $stdout }
if ($stderr) { Write-Output $stderr }
if ($exitCode -ne 0 -or $stopReason) { exit 1 }
