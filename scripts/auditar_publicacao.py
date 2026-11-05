"""Audita o repositorio e seu historico antes de uma publicacao no GitHub."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import io
import json
from pathlib import Path
import re
import subprocess
from typing import Iterable
from urllib.parse import unquote
from zipfile import BadZipFile, ZipFile

import ezdxf
from openpyxl import load_workbook
from PIL import Image
from pypdf import PdfReader


TEXT_LIMIT = 8 * 1024 * 1024
WARNING_SIZE = 50 * 1024 * 1024
BLOCKING_SIZE = 100 * 1024 * 1024
TEMPORARY_NAME = re.compile(
    r"(?i)(^|/)(?:\.env(?:\..+)?|id_rsa|id_ed25519|credentials?(?:\..+)?|"
    r"secrets?(?:\..+)?|tokens?(?:\..+)?|\.npmrc|\.pypirc|\.netrc)$|"
    r"(?:\.bak|\.tmp|\.temp|\.swp|\.swo|\.dwl|\.dwl2|\.sv\$|\.log|\.p12|"
    r"\.pfx|\.pem|\.key|\.kdbx|\.sqlite|\.db|\.dump)$|(?:^|/)~\$|"
    r"(?:^|/)(?:desktop\.ini|thumbs\.db|\.ds_store)$"
)
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
LOCAL_PATH = re.compile(
    r"(?i)(?:\b[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\"'<>]+|"
    r"/(?:home|Users)/[^/\s]+/[^\s\"'<>]+|"
    r"file:" + r"//(?:/[A-Z]:[\\/]|/(?:home|Users)/|[A-Z0-9._-]+/)[^\s\"'<>]+)"
)
CPF_CANDIDATE = re.compile(r"(?<!\d)(\d{3}[. -]?\d{3}[. -]?\d{3}[-. ]?\d{2})(?!\d)")
SHA256_HEX = re.compile(r"(?i)\b[0-9a-f]{64}\b")
RG_LABELED = re.compile(
    r"(?i)\b(?:RG|registro\s+geral)\s*[:#=-]\s*([0-9]{1,2}\.?[0-9]{3}\.?[0-9]{3}[- ]?[0-9X])\b"
)
PHONE = re.compile(
    r"(?<!\d)(?:\+?55[ .-]+)?(?:\([1-9][0-9]\)|[1-9][0-9][ .-])"
    r"[ .-]?(?:9[0-9]{4}|[2-8][0-9]{3})[ .-][0-9]{4}(?!\d)"
)
ADDRESS = re.compile(
    r"(?i)\b(?:Rua|Avenida|Av\.|Travessa|Alameda|Rodovia|Estrada)\s+"
    r"[A-ZÀ-ÖØ-öø-ÿ][^\n,;]{2,80}(?:,\s*\d{1,6})?"
)
KNOWN_CREDENTIALS = [
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bAIza[A-Za-z0-9_-]{30,}\b"),
]
CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?i)\b(?:password|passwd|senha|token|secret|api[_-]?key|client[_-]?secret|"
    r"access[_-]?key)\b\s*[:=]\s*[\"']?([^\s\"'#,;}{]{4,})"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    location: str
    detail: str


def run_git(root: Path, *args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        text=not binary,
        stderr=subprocess.DEVNULL,
    )


def repository_paths(root: Path) -> list[str]:
    output = run_git(
        root,
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
        binary=True,
    )
    assert isinstance(output, bytes)
    candidates = sorted(
        item.decode("utf-8", "surrogateescape") for item in output.split(b"\0") if item
    )
    return [relative for relative in candidates if (root / relative).is_file()]


def is_valid_cpf(value: str) -> bool:
    digits = [int(char) for char in value if char.isdigit()]
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    first = (sum(number * weight for number, weight in zip(digits[:9], range(10, 1, -1))) * 10) % 11
    first = 0 if first == 10 else first
    second = (sum(number * weight for number, weight in zip(digits[:10], range(11, 1, -1))) * 10) % 11
    second = 0 if second == 10 else second
    return digits[-2:] == [first, second]


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def redacted(value: str) -> str:
    if "@" in value:
        left, domain = value.rsplit("@", 1)
        return f"{left[:1]}***@{domain}"
    if len(value) <= 6:
        return "***"
    return f"{value[:2]}***{value[-2:]}"


def add_match(
    findings: list[Finding],
    severity: str,
    category: str,
    location: str,
    text: str,
    match: re.Match[str],
) -> None:
    value = match.group(0)
    findings.append(
        Finding(
            severity,
            category,
            f"{location}:{line_number(text, match.start())}",
            f"padrão mascarado {redacted(value)}",
        )
    )


def scan_text(
    text: str,
    location: str,
    findings: list[Finding],
    historical: bool = False,
    numeric_pii: bool = True,
) -> None:
    prefix = "history_" if historical else ""
    for match in EMAIL.finditer(text):
        add_match(findings, "ERROR", f"{prefix}email", location, text, match)
    for match in LOCAL_PATH.finditer(text):
        add_match(findings, "ERROR", f"{prefix}local_path", location, text, match)
    if numeric_pii:
        scan_numeric_pii(text, location, findings, historical)
    private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
    if private_key_marker in text:
        offset = text.index(private_key_marker)
        findings.append(
            Finding(
                "ERROR",
                f"{prefix}private_key",
                f"{location}:{line_number(text, offset)}",
                "chave privada em formato PEM",
            )
        )
    for pattern in KNOWN_CREDENTIALS:
        for match in pattern.finditer(text):
            add_match(findings, "ERROR", f"{prefix}credential", location, text, match)
    for match in CREDENTIAL_ASSIGNMENT.finditer(text):
        candidate = match.group(1).lower()
        if candidate in {"none", "null", "false", "true", "example", "placeholder"}:
            continue
        if candidate.startswith(("${", "%", "os.", "env", "getenv", "process.")):
            continue
        add_match(findings, "ERROR", f"{prefix}credential_assignment", location, text, match)


def scan_numeric_pii(
    text: str,
    location: str,
    findings: list[Finding],
    historical: bool = False,
) -> None:
    prefix = "history_" if historical else ""
    # A valid-looking CPF can occur by chance in a hexadecimal content hash.
    numeric_text = SHA256_HEX.sub(lambda match: " " * len(match.group(0)), text)
    for match in CPF_CANDIDATE.finditer(numeric_text):
        if is_valid_cpf(match.group(1)):
            add_match(findings, "ERROR", f"{prefix}cpf", location, text, match)
    for pattern, category in ((RG_LABELED, "rg"), (PHONE, "phone"), (ADDRESS, "address")):
        for match in pattern.finditer(text):
            add_match(findings, "ERROR", f"{prefix}{category}", location, text, match)


def dxf_visible_text(text: str) -> str:
    try:
        document = ezdxf.read(io.StringIO(text))
    except Exception:
        return ""
    values: list[str] = []
    for entity in document.entitydb.values():
        kind = entity.dxftype()
        if kind == "TEXT":
            values.append(str(entity.dxf.text))
        elif kind == "MTEXT":
            values.append(entity.plain_text())
        elif kind in {"ATTRIB", "ATTDEF"}:
            values.append(str(entity.dxf.text))
    return "\n".join(values)


def text_from_bytes(data: bytes) -> str | None:
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("cp1252")
        except UnicodeDecodeError:
            return None


def scan_links(root: Path, paths: Iterable[str], findings: list[Finding]) -> int:
    checked = 0
    for relative in paths:
        if not relative.lower().endswith(".md"):
            continue
        source = root / relative
        text = source.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            raw = match.group(1).strip().strip("<>")
            if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_text = unquote(raw.split("#", 1)[0])
            checked += 1
            if re.match(r"(?i)^[a-z]:[\\/]", target_text) or target_text.startswith(("/", "\\")):
                findings.append(Finding("ERROR", "absolute_link", f"{relative}:{line_number(text, match.start())}", "link não relativo"))
                continue
            target = (source.parent / target_text).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                findings.append(Finding("ERROR", "escaping_link", f"{relative}:{line_number(text, match.start())}", "link sai da raiz"))
                continue
            if not target.exists():
                findings.append(Finding("ERROR", "broken_link", f"{relative}:{line_number(text, match.start())}", target_text))
    return checked


def scan_binary_metadata(root: Path, paths: Iterable[str], findings: list[Finding]) -> dict[str, int]:
    counts = Counter()
    for relative in paths:
        path = root / relative
        suffix = path.suffix.lower()
        metadata_parts: list[tuple[str, str]] = []
        try:
            if suffix == ".pdf":
                counts["pdf"] += 1
                reader = PdfReader(path)
                metadata_parts = [(str(key), str(value)) for key, value in (reader.metadata or {}).items() if value is not None]
                visible_text = "\n".join(page.extract_text() or "" for page in reader.pages)
                scan_text(visible_text, f"{relative}[visible_text]", findings)
            elif suffix == ".png":
                counts["png"] += 1
                with Image.open(path) as image:
                    metadata_parts = [(str(key), str(value)) for key, value in image.info.items()]
            elif suffix == ".xlsx":
                counts["xlsx"] += 1
                with ZipFile(path) as archive:
                    for member in ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml"):
                        if member in archive.namelist():
                            metadata_parts.append((member, archive.read(member).decode("utf-8", "replace")))
                workbook = load_workbook(path, data_only=False, read_only=True)
                cell_text = "\n".join(
                    str(cell.value)
                    for sheet in workbook.worksheets
                    for row in sheet.iter_rows()
                    for cell in row
                    if cell.value is not None
                )
                workbook.close()
                scan_text(cell_text, f"{relative}[cells]", findings)
        except (BadZipFile, OSError, ValueError) as exc:
            findings.append(Finding("ERROR", "metadata_read", relative, type(exc).__name__))
            continue
        for key, value in metadata_parts:
            metadata_findings: list[Finding] = []
            scan_text(value, f"{relative}[{key}]", metadata_findings)
            findings.extend(metadata_findings)
    return dict(counts)


def history_blobs(root: Path) -> tuple[list[tuple[str, str, int]], dict[str, bytes]]:
    raw_objects = str(run_git(root, "rev-list", "--objects", "--all")).splitlines()
    path_by_oid: dict[str, str] = {}
    oids: list[str] = []
    for line in raw_objects:
        oid, _, path = line.partition(" ")
        oids.append(oid)
        if path:
            path_by_oid.setdefault(oid, path)
    batch_input = ("\n".join(oids) + "\n").encode()
    batch = subprocess.check_output(
        ["git", "-C", str(root), "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        input=batch_input,
    ).decode().splitlines()
    blobs: list[tuple[str, str, int]] = []
    contents: dict[str, bytes] = {}
    content_oids: list[str] = []
    for line in batch:
        oid, kind, size_text = line.split()
        if kind != "blob":
            continue
        size = int(size_text)
        path = path_by_oid.get(oid, "(caminho histórico desconhecido)")
        blobs.append((oid, path, size))
        if size <= TEXT_LIMIT:
            content_oids.append(oid)
    if content_oids:
        packed = subprocess.check_output(
            ["git", "-C", str(root), "cat-file", "--batch"],
            input=("\n".join(content_oids) + "\n").encode(),
        )
        stream = io.BytesIO(packed)
        for requested_oid in content_oids:
            header = stream.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise RuntimeError(f"Resposta inesperada de git cat-file para {requested_oid}")
            oid, _, size_text = header
            contents[oid] = stream.read(int(size_text))
            if stream.read(1) != b"\n":
                raise RuntimeError(f"Separador ausente em git cat-file para {requested_oid}")
    return blobs, contents


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", type=Path, default=Path("work/auditoria-publicacao.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    paths = repository_paths(root)
    findings: list[Finding] = []
    extension_counts = Counter()
    current_sizes: list[tuple[int, str]] = []

    for relative in paths:
        path = root / relative
        size = path.stat().st_size
        extension_counts[path.suffix.lower() or "(sem extensão)"] += 1
        current_sizes.append((size, relative))
        if TEMPORARY_NAME.search(relative.replace("\\", "/")):
            findings.append(Finding("ERROR", "suspicious_filename", relative, "nome temporário ou sensível"))
        if size > BLOCKING_SIZE:
            findings.append(Finding("ERROR", "current_file_over_100_mib", relative, f"{size} bytes"))
        elif size > WARNING_SIZE:
            findings.append(Finding("WARNING", "current_file_over_50_mib", relative, f"{size} bytes"))
        if size <= TEXT_LIMIT:
            text = text_from_bytes(path.read_bytes())
            if text is not None:
                suffix = path.suffix.lower()
                scan_text(text, relative, findings, numeric_pii=suffix not in {".dxf", ".svg"})
                if suffix == ".dxf":
                    scan_numeric_pii(dxf_visible_text(text), f"{relative}[entities]", findings)

    links_checked = scan_links(root, paths, findings)
    metadata_counts = scan_binary_metadata(root, paths, findings)

    blobs, history_contents = history_blobs(root)
    for oid, path, size in blobs:
        normalized = path.replace("\\", "/")
        if TEMPORARY_NAME.search(normalized):
            findings.append(Finding("ERROR", "history_suspicious_filename", f"{oid[:12]}:{path}", "nome temporário ou sensível"))
        if size > BLOCKING_SIZE:
            findings.append(Finding("ERROR", "history_blob_over_100_mib", f"{oid[:12]}:{path}", f"{size} bytes"))
        elif size > WARNING_SIZE:
            findings.append(Finding("WARNING", "history_blob_over_50_mib", f"{oid[:12]}:{path}", f"{size} bytes"))
        data = history_contents.get(oid)
        if data is not None:
            text = text_from_bytes(data)
            if text is not None:
                suffix = Path(path).suffix.lower()
                scan_text(
                    text,
                    f"{oid[:12]}:{path}",
                    findings,
                    historical=True,
                    numeric_pii=suffix not in {".dxf", ".svg"},
                )
                if suffix == ".dxf":
                    scan_numeric_pii(
                        dxf_visible_text(text),
                        f"{oid[:12]}:{path}[entities]",
                        findings,
                        historical=True,
                    )

    commit_rows = str(run_git(root, "log", "--all", "--format=%H%x09%an%x09%ae")).splitlines()
    commit_identities = set()
    for row in commit_rows:
        oid, name, email = row.split("\t", 2)
        commit_identities.add((name, email))
        domain = email.rsplit("@", 1)[-1].lower() if "@" in email else ""
        if domain not in {"localhost", "users.noreply.github.com"}:
            findings.append(Finding("WARNING", "commit_email", oid[:12], f"{name}: {redacted(email)}"))

    package_json = root / "package.json"
    if package_json.exists():
        package = json.loads(package_json.read_text(encoding="utf-8"))
        dependencies = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
        if dependencies and not any((root / name).exists() for name in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock")):
            findings.append(Finding("WARNING", "node_lock_missing", "package.json", "dependências Node sem lockfile"))
        for name in dependencies:
            if name.startswith("@oai/"):
                findings.append(Finding("WARNING", "potentially_private_dependency", "package.json", name))

    requirement_lines = [
        line.strip()
        for line in (root / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    for line in requirement_lines:
        if "==" not in line:
            findings.append(Finding("WARNING", "python_dependency_unpinned", "requirements.txt", line))

    license_text = (root / "LICENSE").read_text(encoding="utf-8") if (root / "LICENSE").exists() else ""
    if "MIT License" not in license_text or "CC BY-NC 4.0" not in license_text:
        findings.append(Finding("ERROR", "license_scope", "LICENSE", "escopo dual MIT/CC BY-NC não identificado"))

    status_lines = str(run_git(root, "status", "--porcelain=v1")).splitlines()
    remotes = str(run_git(root, "remote")).splitlines()
    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARNING"]
    result = {
        "schema_version": 1,
        "status": "FAIL" if errors else "WARN" if warnings else "PASS",
        "repository": str(root),
        "branch": str(run_git(root, "branch", "--show-current")).strip(),
        "commits": int(str(run_git(root, "rev-list", "--count", "--all")).strip()),
        "remotes": remotes,
        "working_tree_entries": status_lines,
        "current": {
            "files": len(paths),
            "bytes": sum(size for size, _ in current_sizes),
            "largest": [
                {"path": path, "bytes": size}
                for size, path in sorted(current_sizes, reverse=True)[:20]
            ],
            "extensions": dict(sorted(extension_counts.items())),
        },
        "history": {
            "blobs": len(blobs),
            "bytes_uncompressed": sum(size for _, _, size in blobs),
            "largest": [
                {"oid": oid, "path": path, "bytes": size}
                for oid, path, size in sorted(blobs, key=lambda item: item[2], reverse=True)[:20]
            ],
            "identities": [
                {"name": name, "email": redacted(email)}
                for name, email in sorted(commit_identities)
            ],
        },
        "links_checked": links_checked,
        "metadata_files": metadata_counts,
        "findings": [asdict(item) for item in findings],
        "summary": {"errors": len(errors), "warnings": len(warnings)},
    }
    output = args.json if args.json.is_absolute() else root / args.json
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"PUBLICACAO {result['status']} | arquivos={len(paths)} commits={result['commits']} "
        f"blobs={len(blobs)} links={links_checked} erros={len(errors)} avisos={len(warnings)}"
    )
    print(f"RESULTADO={output.relative_to(root)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
