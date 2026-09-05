"""Executa a cadeia reproduzivel: gerar DXF, renderizar e validar."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from portfolio_config import ROOT


def run(script: str, root: Path, *extra: str) -> None:
    command = [sys.executable, str(root / "scripts" / script), "--root", str(root), *extra]
    print("+", " ".join(command))
    subprocess.run(command, cwd=root, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true", help="Falha tambem em avisos")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    run("gerar_template_a3.py", root)
    run("renderizar.py", root)
    validation_args = ["--strict"] if args.strict else []
    run("validar_portfolio.py", root, *validation_args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
