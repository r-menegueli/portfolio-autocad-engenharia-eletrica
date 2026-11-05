"""Renderiza os sete artefatos do Projeto 12 (Grupo Moto-Gerador com QTA) para SVG, PDF e PNG."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from portfolio_config import load_config  # noqa: E402
from renderizar import artifact_bounds, render_document  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    artifacts = [item for item in config["artifacts"] if item["id"].startswith("p12-")]
    if len(artifacts) != 7:
        raise RuntimeError(f"esperados 7 artefatos P12; encontrados {len(artifacts)}")
    for artifact in artifacts:
        source = root / artifact["source"]
        outputs = {kind: root / artifact[kind] for kind in ("svg", "pdf", "png")}
        for out_path in outputs.values():
            out_path.parent.mkdir(parents=True, exist_ok=True)
        render_document(source, outputs, artifact_bounds(artifact, config), config, args.dpi, artifact)
        print(f"Renderizado: {artifact['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
