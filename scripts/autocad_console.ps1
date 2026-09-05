[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Audit', 'Convert')]
    [string]$Action,

    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputDwg,

    [string]$EvidencePath,

    [ValidateSet('pt-BR', 'en-US')]
    [string]$Language = 'pt-BR'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Find-AcCoreConsole {
    $candidates = @(
        'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe',
        'C:\Program Files\Autodesk\AutoCAD 2026\accoreconsole.exe',
        'C:\Program Files\Autodesk\AutoCAD 2025\accoreconsole.exe'
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    $registryRoots = @(
        'HKLM:\SOFTWARE\Autodesk\AutoCAD',
        'HKLM:\SOFTWARE\WOW6432Node\Autodesk\AutoCAD'
    )
    foreach ($registryRoot in $registryRoots) {
        if (-not (Test-Path -LiteralPath $registryRoot)) {
            continue
        }
        $installKeys = Get-ChildItem -LiteralPath $registryRoot -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.PSChildName -eq 'Install' }
        foreach ($key in $installKeys) {
            $properties = Get-ItemProperty -LiteralPath $key.PSPath -ErrorAction SilentlyContinue
            if ($properties.INSTALLDIR) {
                $candidate = Join-Path $properties.INSTALLDIR 'accoreconsole.exe'
                if (Test-Path -LiteralPath $candidate -PathType Leaf) {
                    return (Resolve-Path -LiteralPath $candidate).Path
                }
            }
        }
    }
    throw 'AcCoreConsole nao encontrado. Instale o AutoCAD ou use apenas DXF.'
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Invoke-CoreConsole {
    param(
        [string]$ConsolePath,
        [string]$DrawingPath,
        [string]$ScriptPath,
        [string]$LanguageCode,
        [string]$LogPath
    )
    $consoleWorkingDirectory = Split-Path -Parent $LogPath
    Push-Location -LiteralPath $consoleWorkingDirectory
    try {
        $captured = & $ConsolePath /i $DrawingPath /s $ScriptPath /l $LanguageCode 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $clean = ($captured | Out-String) -replace "`0", ''
    [System.IO.File]::WriteAllText($LogPath, $clean, [System.Text.UTF8Encoding]::new($false))
    return [pscustomobject]@{
        ExitCode = $exitCode
        Log = $clean
    }
}

$console = Find-AcCoreConsole
$input = (Resolve-Path -LiteralPath $InputPath).Path
if ([System.IO.Path]::GetExtension($input).ToLowerInvariant() -notin @('.dxf', '.dwg')) {
    throw 'A entrada precisa ser DXF ou DWG real.'
}

$temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('portfolio-autocad-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temporaryRoot | Out-Null
try {
    $auditScript = Join-Path $PSScriptRoot 'autocad\auditar.scr'
    $firstLog = Join-Path $temporaryRoot 'abertura.log'

    if ($Action -eq 'Audit') {
        $audit = Invoke-CoreConsole -ConsolePath $console -DrawingPath $input -ScriptPath $auditScript -LanguageCode $Language -LogPath $firstLog
        if ($audit.ExitCode -ne 0) {
            throw "AutoCAD falhou ao abrir/auditar o desenho (exit $($audit.ExitCode)). Consulte $firstLog"
        }
        Write-Output "AUTOCAD_AUDIT=PASS"
        Write-Output "CONSOLE=$console"
        Write-Output "INPUT_SHA256=$(Get-Sha256 $input)"
        exit 0
    }

    if (-not $OutputDwg) {
        throw 'OutputDwg e obrigatorio para Action=Convert.'
    }
    if ([System.IO.Path]::GetExtension($OutputDwg).ToLowerInvariant() -ne '.dwg') {
        throw 'A saida deve usar a extensao .dwg.'
    }
    if ([System.IO.Path]::GetExtension($input).ToLowerInvariant() -ne '.dxf') {
        throw 'A conversao controlada aceita apenas fonte .dxf.'
    }

    $output = [System.IO.Path]::GetFullPath($OutputDwg)
    if ($output -eq $input) {
        throw 'Entrada e saida nao podem ser o mesmo arquivo.'
    }
    $outputDirectory = Split-Path -Parent $output
    if (-not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory | Out-Null
    }
    if (Test-Path -LiteralPath $output) {
        throw "A saida ja existe; remova-a explicitamente antes de converter: $output"
    }

    $forwardOutput = $output.Replace('\', '/')
    $convertScript = Join-Path $temporaryRoot 'converter.scr'
    $scriptLines = @(
        '_.FILEDIA',
        '0',
        '_.CMDDIA',
        '0',
        '_.AUDIT',
        '_N',
        '_.SAVEAS',
        '2018',
        $forwardOutput,
        '_.QUIT',
        '_Y'
    )
    [System.IO.File]::WriteAllLines($convertScript, $scriptLines, [System.Text.Encoding]::ASCII)
    $convertLog = Join-Path $temporaryRoot 'conversao.log'
    $conversion = Invoke-CoreConsole -ConsolePath $console -DrawingPath $input -ScriptPath $convertScript -LanguageCode $Language -LogPath $convertLog
    if ($conversion.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $output -PathType Leaf)) {
        throw "Conversao AutoCAD falhou (exit $($conversion.ExitCode)). Consulte $convertLog"
    }

    $bytes = [System.IO.File]::ReadAllBytes($output)
    if ($bytes.Length -lt 6) {
        throw 'DWG gerado esta vazio ou truncado.'
    }
    $signature = [System.Text.Encoding]::ASCII.GetString($bytes, 0, 6)
    if ($signature -notmatch '^AC10\d{2}$') {
        throw "Assinatura DWG invalida: $signature"
    }

    $reopenLog = Join-Path $temporaryRoot 'reabertura.log'
    $reopen = Invoke-CoreConsole -ConsolePath $console -DrawingPath $output -ScriptPath $auditScript -LanguageCode $Language -LogPath $reopenLog
    if ($reopen.ExitCode -ne 0) {
        throw "DWG criado, mas a reabertura falhou (exit $($reopen.ExitCode)). Consulte $reopenLog"
    }

    $consoleInfo = (Get-Item -LiteralPath $console).VersionInfo
    $evidence = [ordered]@{
        schema_version = 1
        status = 'PASS'
        converter = 'Autodesk AcCoreConsole'
        converter_version = $consoleInfo.FileVersion
        source_format = 'DXF'
        output_format = 'DWG'
        output_signature = $signature
        source_sha256 = Get-Sha256 $input
        output_sha256 = Get-Sha256 $output
        conversion_exit_code = $conversion.ExitCode
        reopen_exit_code = $reopen.ExitCode
        verified_actions = @('real_saveas', 'binary_signature', 'reopen', 'audit')
    }
    $evidenceFile = if ($EvidencePath) {
        [System.IO.Path]::GetFullPath($EvidencePath)
    } else {
        $output + '.validacao.json'
    }
    $evidenceDirectory = Split-Path -Parent $evidenceFile
    if (-not (Test-Path -LiteralPath $evidenceDirectory)) {
        New-Item -ItemType Directory -Path $evidenceDirectory | Out-Null
    }
    $json = $evidence | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText($evidenceFile, $json + "`n", [System.Text.UTF8Encoding]::new($false))

    Write-Output 'AUTOCAD_CONVERSION=PASS'
    Write-Output "DWG=$output"
    Write-Output "SIGNATURE=$signature"
    Write-Output "EVIDENCE=$evidenceFile"
    exit 0
}
finally {
    if (Test-Path -LiteralPath $temporaryRoot) {
        Remove-Item -LiteralPath $temporaryRoot -Recurse -Force
    }
}
