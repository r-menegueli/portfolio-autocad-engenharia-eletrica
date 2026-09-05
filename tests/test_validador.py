from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import ezdxf
from PIL import Image
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gerar_template_a3 import build_template  # noqa: E402
from portfolio_config import load_config  # noqa: E402
from validar_portfolio import Validator, overlap_ratio  # noqa: E402


class Box:
    def __init__(self, x0: float, y0: float, x1: float, y1: float) -> None:
        self.extmin = type("Point", (), {"x": x0, "y": y0})()
        self.extmax = type("Point", (), {"x": x1, "y": y1})()


def fixture_root(tmp_path: Path) -> Path:
    shutil.copy2(ROOT / "portfolio.toml", tmp_path / "portfolio.toml")
    return tmp_path


def codes(validator: Validator) -> set[str]:
    return {item.code for item in validator.diagnostics}


def test_overlap_ratio_distinguishes_overlap_and_touch() -> None:
    assert overlap_ratio(Box(0, 0, 10, 10), Box(5, 5, 15, 15), shrink=0.0) == pytest.approx(0.25)
    assert overlap_ratio(Box(0, 0, 10, 10), Box(10, 0, 20, 10), shrink=0.0) == 0.0


def test_corrupt_dxf_is_rejected(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    bad = root / "bad.dxf"
    bad.write_text("isto definitivamente nao e um arquivo dxf valido", encoding="utf-8")
    validator = Validator(root)
    validator.check_dxf(bad, {"require_a3": True, "require_notice": True})
    assert "DXF_READ" in codes(validator)


def test_layers_bounds_and_duplicate_text_are_detected(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    config = load_config(root)
    drawing = root / "drawing.dxf"
    build_template(config, drawing)
    doc = ezdxf.readfile(drawing)
    msp = doc.modelspace()
    msp.add_line((5, 5), (20, 20), dxfattribs={"layer": "05_POTENCIA"})
    for _ in range(2):
        msp.add_text("DUPLICADO", dxfattribs={"layer": "02_TEXTO", "height": 3}).set_placement((150, 150))
    doc.layers.remove("10_ELETROCALHAS")
    doc.saveas(drawing, encoding="utf-8")

    validator = Validator(root)
    validator.check_dxf(drawing, {"require_a3": True, "require_notice": True})
    found = codes(validator)
    assert "DXF_LAYERS" in found
    assert "DXF_OUTSIDE_FRAME" in found
    assert "TEXT_OVERLAP" in found


def test_broken_links_and_temporary_files_are_detected(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    (root / "README.md").write_text("[quebrado](ausente.md)\n", encoding="utf-8")
    (root / "desenho.dwl2").write_text("lock", encoding="utf-8")
    validator = Validator(root)
    validator.check_markdown_links()
    validator.check_temporary_files()
    assert {"LINK_BROKEN", "TEMPORARY_FILE"}.issubset(codes(validator))


def test_invalid_svg_png_and_pdf_are_detected(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    validator = Validator(root)
    svg = root / "bad.svg"
    png = root / "bad.png"
    pdf = root / "bad.pdf"
    svg.write_text("<svg>", encoding="utf-8")
    Image.new("RGB", (100, 100), "white").save(png)
    pdf.write_bytes(b"%PDF-corrompido")
    validator.check_svg(svg, require_a3=True)
    validator.check_png(png, require_a3=True)
    validator.check_pdf(pdf, require_a3=True)
    assert {"SVG_PARSE", "PNG_RESOLUTION", "PNG_UNIFORM", "PDF_PARSE"}.issubset(codes(validator))


def test_renamed_dxf_is_not_accepted_as_dwg(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    fake = root / "falso.dwg"
    fake.write_text("0\nSECTION\n", encoding="ascii")
    validator = Validator(root)
    validator.check_dwg_files()
    assert {"DWG_SIGNATURE", "DWG_EVIDENCE"}.issubset(codes(validator))


def test_invalid_csv_contract_is_detected(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    table = root / "lista-materiais.csv"
    table.write_text("item,quantidade\n1,0\n1,abc\n", encoding="utf-8")
    validator = Validator(root)
    validator.check_csv_table(
        table,
        required_columns=("item", "quantidade", "unidade"),
        unique_column="item",
        numeric_columns=("quantidade",),
    )
    assert {"CSV_COLUMNS", "CSV_NUMBER", "CSV_DUPLICATE"}.issubset(codes(validator))


def test_template_generation_is_reproducible_across_processes(tmp_path: Path) -> None:
    hashes: list[tuple[bytes, bytes]] = []
    for name in ("run-a", "run-b"):
        target = tmp_path / name
        target.mkdir()
        shutil.copy2(ROOT / "portfolio.toml", target / "portfolio.toml")
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "gerar_template_a3.py"), "--root", str(target)],
            check=True,
            capture_output=True,
        )
        hashes.append(
            (
                (target / "templates" / "template-a3.dxf").read_bytes(),
                (target / "templates" / "carimbo-a3" / "carimbo-a3.dxf").read_bytes(),
            )
        )
    assert hashes[0] == hashes[1]


def test_current_repository_passes_strict_validation() -> None:
    validator = Validator(ROOT, strict=True)
    validator.run()
    result = validator.result()
    assert result["status"] == "PASS", json.dumps(result, ensure_ascii=False, indent=2)
