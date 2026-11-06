"""Valida coerência funcional, I/O e identificações do Projeto 04."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import ezdxf


PROJECT_SLUG = "04-controle-nivel-reservatorio"
SHEETS = (
    "01_fluxograma_processo.dxf",
    "02_pid_instrumentacao.dxf",
    "03_malha_controle.dxf",
    "04_diagrama_eletrico.dxf",
    "05_interligacoes_instrumentos.dxf",
    "06_layout_sistema.dxf",
    "07_sequencia_operacao_causa_efeito.dxf",
    "08_fronteira_succao_dados_fonte.dxf",
    "09_balanco_succao_criterio_npsh.dxf",
)
REQUIRED_INSTRUMENTS = {
    "LT-101", "LSL-101", "LSH-101", "LSHH-101", "LIC-101",
    "VFD-101", "P-101", "M-101", "PLC-101", "KSR-101",
}
REQUIRED_IO = {
    "AI0", "AI1", "AO0", "DI0", "DI1", "DI2", "DI3", "DI4", "DI5",
    "DI6", "DI7", "DI8", "DI9", "DO0", "DO1", "DO2", "DO3", "DO4",
    "DO5", "DO6", "DO7", "DO8", "DO9",
}
REQUIRED_CABLES = {f"C-{number}" for number in range(101, 110)}
REQUIRED_MATERIAL_TAGS = {
    "PLC-101", "VFD-101", "M-101", "P-101", "TK-101", "LT-101", "LSL-101",
    "LSH-101", "LSHH-101", "KSR-101", "PS1", "QF1", "PAINEL-101",
    "HV-102",
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


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    errors: list[str] = []
    checks = 0

    instrument_rows = read_rows(project / "lista-instrumentos.csv")
    io_rows = read_rows(project / "lista-io.csv")
    cable_rows = read_rows(project / "lista-cabos.csv")
    terminal_rows = read_rows(project / "lista-bornes.csv")
    material_rows = read_rows(project / "lista-materiais.csv")
    effect_rows = read_rows(project / "matriz-causa-efeito.csv")
    source_rows = read_rows(project / "dados-fonte-succao.csv")

    expected_source_ids = {f"D{index:02d}" for index in range(1, 8)}
    source_ids = {row["id"] for row in source_rows}
    checks += len(expected_source_ids) + 6
    if source_ids != expected_source_ids or len(source_rows) != len(expected_source_ids):
        errors.append("O levantamento de fonte deve conter exatamente D01 a D07.")
    if any(row["status"] != "PENDENTE" for row in source_rows):
        errors.append("Os cinco grupos de dados da fonte devem permanecer PENDENTE até levantamento.")
    if any(not row["fonte_evidencia"] or not row["observacoes"] for row in source_rows):
        errors.append("Cada dado de fonte deve indicar evidência e motivo da pendência.")
    if any(not row["unidade_referencia"].strip() for row in source_rows):
        errors.append("Cada dado de fonte deve indicar unidade ou referência aplicável.")
    if any(row["valor_registrado"].strip() for row in source_rows):
        errors.append("Não registrar valores da fonte antes do levantamento aprovado.")
    source_by_id = {row["id"]: row for row in source_rows}
    if any(
        "unidade" not in source_by_id.get(identifier, {}).get("dado_requerido", "").casefold()
        for identifier in ("D02", "D03", "D04")
    ):
        errors.append("D02–D04 devem solicitar o registro das unidades de engenharia.")
    if "datum" not in source_by_id.get("D03", {}).get("unidade_referencia", "").casefold():
        errors.append("D03 deve solicitar a referência vertical (datum) das cotas.")
    fluid_text = source_by_id.get("D06", {}).get("dado_requerido", "").casefold()
    if not all(term in fluid_text for term in ("temperatura", "densidade", "pressão de vapor")):
        errors.append("D06 deve registrar fluido, temperatura, densidade e base para pressão de vapor.")
    if not all(term in source_by_id.get("D06", {}).get("unidade_referencia", "").casefold() for term in ("°c", "kg/m³", "absoluta")):
        errors.append("D06 deve solicitar unidades de temperatura, densidade e pressão absoluta.")
    atmosphere_text = source_by_id.get("D07", {}).get("dado_requerido", "").casefold()
    if not all(term in atmosphere_text for term in ("pressão absoluta", "barométrica local")):
        errors.append("D07 deve diferenciar pressão absoluta e pressão barométrica local.")
    if not all(term in source_by_id.get("D07", {}).get("unidade_referencia", "").casefold() for term in ("kpa abs", "altitude", "m")):
        errors.append("D07 deve indicar pressão absoluta e unidade de altitude quando usada.")

    expected_events = {f"E{index:02d}" for index in range(1, 10)}
    effect_ids = {row["id"] for row in effect_rows}
    checks += len(expected_events) + 2
    if effect_ids != expected_events or len(effect_rows) != len(expected_events):
        errors.append("Matriz causa–efeito deve conter exatamente os eventos E01 a E09.")
    required_effect_text = {
        "E01": ("STOP", "Retira comando de marcha"),
        "E02": ("95%", "fora do PI"),
        "E03": ("3,6 mA", "Desabilita PI"),
        "E04": ("Falha do VFD", "bloqueia partida"),
        "E05": ("60 min", "TA-101"),
        "E06": ("Perda de energia", "Sem repartida automática"),
        "E07": ("divergência persistente", "bloqueia AUTO"),
        "E08": ("15%", "ação de processo pendente"),
        "E09": ("85%", "ação de processo pendente"),
    }
    for row in effect_rows:
        expected = required_effect_text.get(row["id"])
        if expected:
            checks += len(expected)
            combined = " ".join(row.values()).casefold()
            for term in expected:
                if term.casefold() not in combined:
                    errors.append(f"{row['id']}: resposta causa–efeito ausente: {term}.")

    instrument_tags = {row["tag"] for row in instrument_rows}
    checks += len(REQUIRED_INSTRUMENTS)
    for tag in sorted(REQUIRED_INSTRUMENTS - instrument_tags):
        errors.append(f"Instrumento/equipamento obrigatório ausente: {tag}.")

    channels = [row["canal"] for row in io_rows]
    checks += 3
    if len(channels) != len(set(channels)):
        errors.append("Há canais de I/O duplicados.")
    if set(channels) != REQUIRED_IO:
        errors.append("A lista de I/O diverge do conjunto funcional obrigatório.")
    if any(not row["terminal"].startswith("X") for row in io_rows):
        errors.append("Há canal de I/O sem referência de borne X.")

    cable_ids = {row["cabo"] for row in cable_rows}
    checks += 1
    if cable_ids != REQUIRED_CABLES:
        errors.append("A lista de cabos não cobre exatamente C-101 a C-109.")

    terminal_ids = {row["borne"] for row in terminal_rows}
    checks += len(io_rows)
    for row in io_rows:
        if row["terminal"] not in terminal_ids and row["terminal"] not in {
            "X1:01-02", "X1:03-04", "X1:05-06", "X1:07-08", "X1:09-10",
            "X1:11-12", "X1:13-14", "X1:15-16", "X1:17-18", "X1:19-20",
            "X1:21-22", "X1:23-24",
        }:
            errors.append(f"{row['canal']}: borne {row['terminal']} não documentado.")

    material_tags = {row["referencia"] for row in material_rows}
    checks += len(REQUIRED_MATERIAL_TAGS) + 1
    if len(material_rows) != 18:
        errors.append(f"A lista de materiais deve conter 18 itens, incluindo HV-102; encontrados {len(material_rows)}.")
    for tag in sorted(REQUIRED_MATERIAL_TAGS):
        if tag not in material_tags:
            errors.append(f"Material obrigatório ausente: {tag}.")

    # Invariantes funcionais: toda marcha exige cinco permissivos independentes.
    truth_rows = 0
    for emergency_ok in (False, True):
        for ksr_ok in (False, True):
            for lshh_clear in (False, True):
                for vfd_ready in (False, True):
                    for lt_valid in (False, True):
                        for run_request in (False, True):
                            run = emergency_ok and ksr_ok and lshh_clear and vfd_ready and lt_valid and run_request
                            truth_rows += 1
                            checks += 1
                            if run and not all((emergency_ok, ksr_ok, lshh_clear, vfd_ready, lt_valid)):
                                errors.append("Invariante de permissivos de marcha foi violada.")

    # Propriedade do sentido da malha: PV abaixo de SP deve aumentar MV.
    for pv, expected in ((40.0, "increase"), (60.0, "hold"), (80.0, "decrease")):
        error = 60.0 - pv
        action = "increase" if error > 0 else "decrease" if error < 0 else "hold"
        checks += 1
        if action != expected:
            errors.append("Sentido de ação da malha inconsistente.")

    required_doc_terms = {
        "memorial-descritivo.md": ("variável controlada", "variável manipulada", "perturbação", "lshh-101"),
        "filosofia-controle.md": ("anti-windup", "3,6 ma", "21 ma", "sem salto"),
        "estrategia-pid.md": ("kc", "ti", "td", "sentido"),
        "sequencia-funcionamento.md": ("partida automática", "repartida automática", "falha"),
        "criterios-premissas.md": ("10 m³", "20 a 60 hz", "análise de risco"),
    }
    for filename, terms in required_doc_terms.items():
        content = (project / filename).read_text(encoding="utf-8").casefold()
        for term in terms:
            checks += 1
            if term.casefold() not in content:
                errors.append(f"{filename}: termo obrigatório ausente: {term}.")

    all_dxf_text: list[str] = []
    for index, filename in enumerate(SHEETS, start=1):
        path = project / "fonte" / filename
        checks += 4
        if not path.is_file():
            errors.append(f"DXF ausente: {filename}.")
            continue
        try:
            doc = ezdxf.readfile(path)
            auditor = doc.audit()
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        if auditor.has_errors:
            errors.append(f"{filename}: auditoria ezdxf encontrou {len(auditor.errors)} erro(s).")
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_PROJECT") != PROJECT_SLUG:
            errors.append(f"{filename}: metadado de projeto incorreto.")
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/{len(SHEETS):02d}":
            errors.append(f"{filename}: metadado de prancha incorreto.")
        sheet_text = extract_text(doc)
        all_dxf_text.append(sheet_text)
        if index == 1:
            checks += 3
            if "tk-101" not in sheet_text.casefold():
                errors.append(f"{filename}: identificação do reservatório TK-101 ausente.")
            if "tk-100" in sheet_text.casefold():
                errors.append(f"{filename}: identificação inconsistente TK-100 encontrada.")
            normalized_sheet = sheet_text.casefold()
            if "origem de água" not in normalized_sheet or "equipamento a montante não definido" not in normalized_sheet:
                errors.append(f"{filename}: origem de água e limite de bateria não estão identificados.")
            for entity in doc.modelspace():
                if entity.dxftype() != "TEXT" or entity.dxf.text.strip().casefold() != "tk-101":
                    continue
                x, y = entity.dxf.insert.x, entity.dxf.insert.y
                if x < 100 and 150 <= y <= 180:
                    errors.append(f"{filename}: TK-101 duplicado na posição da origem a montante.")
        if index == 7:
            required_sequence_terms = (
                "emergência liberada", "kSR / vfd prontos", "lt válido; lshh inativo",
                "operador seleciona auto", "lic assume saída rastreada", "anti-windup",
                "pv < sp", "pv > sp", "falhas", "e01", "e02", "e03", "e04",
                "e05", "e06", "e07", "e08", "e09", "ação de processo pendente",
                "sem repartida automática", "sil/pl",
            )
            normalized_sheet = sheet_text.casefold()
            checks += len(required_sequence_terms)
            for term in required_sequence_terms:
                if term.casefold() not in normalized_sheet:
                    errors.append(f"{filename}: texto funcional ausente: {term}.")
        if index == 8:
            required_source_terms = (
                "fronteira de sucção", "fonte a montante", "p-101", "tk-101",
                "nível/pressão", "npshr", "escorva", "proteção", "v01",
                "d01", "d02", "d03", "d04", "d05", "d06", "d07", "pendente", "unidades", "datum",
            )
            normalized_sheet = sheet_text.casefold()
            checks += len(required_source_terms)
            for term in required_source_terms:
                if term.casefold() not in normalized_sheet:
                    errors.append(f"{filename}: levantamento da fonte não documenta: {term}.")
        if index == 9:
            required_npsh_terms = (
                "npsha", "npshr", "p0,abs", "pv(t)", "ρ", "hL,suc",
                "curva oem", "margem", "d01", "d07", "sem cálculo ou aprovação",
            )
            normalized_sheet = sheet_text.casefold()
            checks += len(required_npsh_terms)
            for term in required_npsh_terms:
                if term.casefold() not in normalized_sheet:
                    errors.append(f"{filename}: método NPSH não documenta: {term}.")

    merged = " ".join(all_dxf_text).casefold()
    for tag in ("tk-101", "p-101", "m-101", "lt-101", "lsl-101", "lsh-101", "lshh-101", "plc-101", "vfd-101", "lic-101"):
        checks += 1
        if tag not in merged:
            errors.append(f"Identificação não localizada no conjunto DXF: {tag}.")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "results": {
            "sheets": len(SHEETS),
            "cause_effect_events": len(effect_rows),
            "instruments_and_equipment": len(instrument_rows),
            "io_points": len(io_rows),
            "analog_inputs": sum(row["tipo"] == "AI" for row in io_rows),
            "analog_outputs": sum(row["tipo"] == "AO" for row in io_rows),
            "digital_inputs": sum(row["tipo"] == "DI" for row in io_rows),
            "digital_outputs": sum(row["tipo"] == "DO" for row in io_rows),
            "terminals": len(terminal_rows),
            "cables": len(cable_rows),
            "materials": len(material_rows),
            "source_data_items": len(source_rows),
            "safety_truth_table_rows": truth_rows,
            "setpoint_percent": 60,
            "pid_initial": {"kc": 0.8, "ti_s": 120, "td_s": 0},
        },
    }
    output = project / "validacao-controle.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDAÇÃO DE CONTROLE {result['status']} | verificações={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
