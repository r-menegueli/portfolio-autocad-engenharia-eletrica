from __future__ import annotations

from pathlib import Path
import tomllib

import ezdxf


ROOT = Path(__file__).resolve().parents[2]
SHEET = ROOT / "25-usina-cogeracao-biomassa" / "fonte" / "02_implantacao_casa_maquinas.dxf"


def test_site_plan_has_physical_mm_geometry_and_true_1_to_500_insertion() -> None:
    doc = ezdxf.readfile(SHEET)
    block = doc.blocks.get("P25_IMPLANTACAO_COGERACAO_MM")
    assert any(entity.dxftype() == "LINE" for entity in block)
    boundary = [
        entity for entity in block
        if entity.dxftype() == "LWPOLYLINE"
        and entity.dxf.layer == "11_ARQUITETURA"
        and len(entity) == 4
    ]
    assert boundary
    points = [tuple(round(v, 3) for v in point[:2]) for point in boundary[0].get_points()]
    assert points == [(0.0, 0.0), (100000.0, 0.0), (100000.0, 65000.0), (0.0, 65000.0)]

    inserts = [entity for entity in doc.modelspace().query("INSERT") if entity.dxf.name == block.name]
    assert len(inserts) == 1
    assert inserts[0].dxf.xscale == inserts[0].dxf.yscale == 1 / 500
    title = next(entity for entity in doc.modelspace().query("INSERT") if entity.dxf.name == "CARIMBO_A3")
    assert {attr.dxf.tag: attr.dxf.text for attr in title.attribs}["ESCALA"] == "1:500"


def test_project_colors_follow_the_central_palette() -> None:
    with (ROOT / "portfolio.toml").open("rb") as stream:
        config = tomllib.load(stream)
    doc = ezdxf.readfile(SHEET)
    expected = config["project_layer_colors"]["p25"]
    for name, color in expected.items():
        assert doc.layers.get(name).dxf.color == color
