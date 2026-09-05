"""Leitura centralizada da configuracao do portfolio."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "portfolio.toml"


def load_config(root: Path | None = None) -> dict:
    """Carrega o TOML a partir da raiz indicada."""
    base = Path(root).resolve() if root else ROOT
    with (base / "portfolio.toml").open("rb") as stream:
        return tomllib.load(stream)


@dataclass(frozen=True)
class SheetGeometry:
    width: float
    height: float
    frame_left: float
    frame_bottom: float
    frame_right: float
    frame_top: float
    tolerance: float

    @classmethod
    def from_config(cls, config: dict) -> "SheetGeometry":
        page = config["page"]
        return cls(
            width=float(page["width"]),
            height=float(page["height"]),
            frame_left=float(page["frame_left"]),
            frame_bottom=float(page["frame_bottom"]),
            frame_right=float(page["frame_right"]),
            frame_top=float(page["frame_top"]),
            tolerance=float(page["tolerance"]),
        )


def required_layers(config: dict) -> tuple[str, ...]:
    return tuple(config["layers"]["required"])
