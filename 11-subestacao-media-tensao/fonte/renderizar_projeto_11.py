"""Renderiza os artefatos do Projeto 11 (Subestacao de Media Tensao) para SVG, PDF e PNG."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from portfolio_config import load_config  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    artifacts = [item for item in config["artifacts"] if item["id"].startswith("p11-")]
    expected_count = next(
        project["sheet_count"]
        for project in config["projects"]
        if project["id"] == "11-subestacao-media-tensao"
    )
    if len(artifacts) != expected_count:
        raise RuntimeError(f"esperados {expected_count} artefatos P11; encontrados {len(artifacts)}")
    command = [
        sys.executable,
        str(root / "scripts" / "renderizar.py"),
        "--root",
        str(root),
        "--dpi",
        str(args.dpi),
    ]
    for artifact in artifacts:
        command.extend(("--artifact", artifact["id"]))
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
