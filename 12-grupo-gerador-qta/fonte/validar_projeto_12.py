"""Valida calculos, referencias e DXFs do Projeto 12 (Grupo Moto-Gerador com QTA)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import ezdxf


PROJECT_SLUG = "12-grupo-gerador-qta"
SHEETS = (
    "01_diagrama_unifilar_qta.dxf",
    "02_diagrama_trifilar_potencia.dxf",
    "03_diagrama_funcional_comando.dxf",
    "04_regua_bornes_interligacao.dxf",
    "05_layout_painel_qta.dxf",
    "06_planta_instalacao_gmg.dxf",
    "07_sequencia_transferencia_qta.dxf",
    "08_matriz_causa_efeito_qta.dxf",
    "09_cadastro_cargas_essenciais_qce.dxf",
)
REQUIRED_TAGS = {
    "GMG-01",
    "QTA",
    "USCA-01",
    "K1",
    "K2",
    "DJ-REDE",
    "DJ-GER",
    "250 kVA",
    "380/220 V",
    "QCE",
    "INT-MEC",
    "MATRIZ CAUSA-EFEITO DO GMG E QTA",
    "CADASTRO DE CARGAS ESSENCIAIS DO QCE",
    "E01",
    "E09",
    "CAB-AL-ILUM",
    "CAB-AL-INC",
    "CAB-AL-CPD",
    "CAB-AL-UTIL",
    "PENDENTE",
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
        expected_sheet = f"{index:02d}/{len(SHEETS):02d}"
        if expected_sheet not in text:
            errors.append(f"Numeracao de prancha {expected_sheet} nao encontrada em {filename}")

    combined_text = " ".join(all_texts)
    for tag in sorted(REQUIRED_TAGS):
        if tag not in combined_text:
            errors.append(f"Tag obrigatoria nao encontrada nas pranchas: {tag}")

    materials = read_rows(project_dir / "lista-materiais.csv")
    cables = read_rows(project_dir / "lista-cabos.csv")
    cause_effect = read_rows(project_dir / "matriz-causa-efeito.csv")
    load_schedule = read_rows(project_dir / "cadastro-cargas-qce.csv")
    if len(materials) < 15:
        errors.append("Lista de materiais possui menos de 15 itens.")
    if len(cables) < 10:
        errors.append("Lista de cabos possui menos de 10 itens.")
    expected_events = [f"E{index:02d}" for index in range(1, 10)]
    actual_events = [row.get("id", "") for row in cause_effect]
    if actual_events != expected_events:
        errors.append("Matriz causa-efeito deve conter exatamente os eventos E01 a E09 em ordem.")
    for index, row in enumerate(cause_effect, start=1):
        if any(not row.get(column, "").strip() for column in ("evento", "deteccao_condicao", "resposta_conceitual", "alarme_indicacao", "retorno_limite")):
            errors.append(f"Evento E{index:02d} possui campo vazio na matriz causa-efeito.")
    if not any("pendente" in row.get("resposta_conceitual", "").lower() for row in cause_effect):
        errors.append("As respostas ainda indefinidas da matriz devem permanecer explicitamente pendentes.")
    expected_load_ids = ["CAB-AL-ILUM", "CAB-AL-INC", "CAB-AL-CPD", "CAB-AL-UTIL"]
    actual_load_ids = [row.get("cabo_id", "") for row in load_schedule]
    if actual_load_ids != expected_load_ids:
        errors.append("O cadastro QCE deve conter os quatro alimentadores documentados, na ordem definida.")
    source_cables = {row.get("cabo", ""): row for row in cables}
    unknown_load_fields = (
        "potencia_instalada_kw",
        "corrente_nominal_a",
        "partida_regime",
        "regime_simultaneidade",
        "prioridade_sequenciamento",
    )
    for row in load_schedule:
        source = source_cables.get(row.get("cabo_id", ""))
        if source is None:
            errors.append(f"Cabo de carga QCE ausente da lista de cabos: {row.get('cabo_id', '')}")
            continue
        for schedule_field, cable_field in (
            ("destino", "para"),
            ("funcao", "funcao"),
            ("formacao", "formacao"),
            ("comprimento_assumido_m", "comprimento_assumido_m"),
        ):
            if row.get(schedule_field, "") != source.get(cable_field, ""):
                errors.append(f"Divergencia entre cadastro QCE e lista de cabos: {row.get('cabo_id', '')}/{schedule_field}")
        for field in unknown_load_fields:
            if row.get(field, "").strip().upper() != "PENDENTE":
                errors.append(f"Campo sem fonte no cadastro QCE deve permanecer pendente: {row.get('cabo_id', '')}/{field}")

    report = {
        "project": PROJECT_SLUG,
        "sheets_checked": len(SHEETS),
        "cause_effect_events": len(cause_effect),
        "qce_load_feeders": len(load_schedule),
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
    print(f"Validacao Projeto 12: PASS ({len(SHEETS)} pranchas, {len(cause_effect)} eventos, {len(load_schedule)} alimentadores QCE, {len(materials)} materiais, {len(cables)} cabos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
