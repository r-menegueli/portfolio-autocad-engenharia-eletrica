from __future__ import annotations

from pathlib import Path

import ezdxf
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "fonte" / "05_sistema_excitacao_avr.dxf"
PDF = ROOT / "exports" / "05_sistema_excitacao_avr.pdf"


def _modelspace_text(path: Path) -> tuple[str, set[str], int]:
    document = ezdxf.readfile(path)
    values: list[str] = []
    layers: set[str] = set()
    line_count = 0
    for entity in document.modelspace():
        layers.add(entity.dxf.layer)
        if entity.dxftype() == "TEXT":
            values.append(entity.dxf.text)
        elif entity.dxftype() == "MTEXT":
            values.append(entity.text)
        if entity.dxftype() in {"LINE", "LWPOLYLINE"}:
            line_count += 1
    return " ".join(values).upper(), layers, line_count


def test_excitation_sheet_has_power_control_interlock_and_terminal_details() -> None:
    text, layers, line_count = _modelspace_text(SOURCE)
    for required in (
        "G1 / BARRA 13,8 KV",
        "TE1",
        "BR1",
        "41E",
        "KFD / RFD",
        "PT1/CT1",
        "AVR1 - REGULADOR DE TENSAO",
        "KP + KI/S",
        "OEL/UEL",
        "52G/86G",
        "64F / 41E",
        "XT1:01-03",
        "XT2:03-04",
        "Y41E",
    ):
        assert required in text
    assert {"05_POTENCIA", "06_COMANDO", "07_INSTRUMENTACAO", "09_BORNES"} <= layers
    assert line_count > 100


def test_excitation_pdf_has_searchable_equipment_tags() -> None:
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 1
    text = (reader.pages[0].extract_text() or "").upper()
    for required in ("TE1", "BR1", "AVR1", "Y41E", "XT1:01-03", "OEL/UEL"):
        assert required in text
