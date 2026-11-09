"""Gera DXFs e derivados do estudo P23 a partir do manifesto central."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    command = [
        sys.executable,
        str(args.root.resolve() / "scripts" / "engineering_studies.py"),
        "--root",
        str(args.root.resolve()),
        "--project",
        "p23",
    ]
    if args.no_render:
        command.append("--no-render")
    subprocess.run(command, cwd=args.root.resolve(), check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
