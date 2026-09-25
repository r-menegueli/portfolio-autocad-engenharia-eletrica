"""Valida calculos, referencias e DXFs do Projeto 11 (Subestacao de Media Tensao)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import ezdxf


PROJECT_SLUG = "11-subestacao-media-tensao"
SHEETS = (
    "01_diagrama_unifilar_geral.dxf",
    "02_planta_baixa_subestacao.dxf",
    "03_cortes_detalhes_eletromecanicos.dxf",
    "04_diagrama_funcional_protecao.dxf",
    "05_malha_aterramento.dxf",
    "06_spda_geral.dxf",
)
REQUIRED_TAGS = {
    "TR-01",
    "DJ-MT",
    "SEC-01",
    "RELE DIGITAL",
    "QGBT",
    "DJ-GERAL",
    "DPS-BT",
    "BEP",
    "BUCHHOLZ",
    "500 kVA",
    "13,8 kV",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def extract_text(doc: ezdxf.document.Drawing) -> str:
    values: list[str] = []
    for entity in doc.modelspace():
        if entity.dxftype() == "TEXT":
            values.append(entity.dxf.text)
        elif entity.dxftype() == "MTEXT":
            values.append(entity.plain_text())
        elif entity.dxftype() == "INSERT":
            values.extend(attrib.dxf.text for attrib in entity.attribs)
    return " ".join(values)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    project_dir = root / PROJECT_SLUG
    source_dir = project_dir / "fonte"

    errors: list[str] = []
    all_texts: list[str] = []

    for index, filename in enumerate(SHEETS, start=1):
        dxf_path = source_dir / filename
        if not dxf_path.exists():
            errors.append(f"DXF ausente: {filename}")
            continue
        doc = ezdxf.readfile(dxf_path)
        audit = doc.audit()
        if audit.errors:
            errors.append(f"Erros de auditoria em {filename}: {len(audit.errors)}")
        text = extract_text(doc)
        all_texts.append(text)
        expected_sheet = f"{index:02d}/06"
        if expected_sheet not in text:
            errors.append(f"Numeracao de prancha {expected_sheet} nao encontrada em {filename}")

    combined_text = " ".join(all_texts)
    for tag in sorted(REQUIRED_TAGS):
        if tag not in combined_text:
            errors.append(f"Tag obrigatoria nao encontrada nas pranchas: {tag}")

    materials = read_rows(project_dir / "lista-materiais.csv")
    cables = read_rows(project_dir / "lista-cabos.csv")
    if len(materials) < 15:
        errors.append("Lista de materiais possui menos de 15 itens.")
    if len(cables) < 10:
        errors.append("Lista de cabos possui menos de 10 itens.")

    report = {
        "project": PROJECT_SLUG,
        "sheets_checked": len(SHEETS),
        "materials_count": len(materials),
        "cables_count": len(cables),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    (project_dir / "validacao.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if errors:
        for err in errors:
            print(f"[ERRO] {err}")
        return 1
    print(f"Validacao Projeto 11: PASS ({len(SHEETS)} pranchas, {len(materials)} materiais, {len(cables)} cabos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
