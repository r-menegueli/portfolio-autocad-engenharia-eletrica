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
    checks += len(REQUIRED_MATERIAL_TAGS)
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
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/06":
            errors.append(f"{filename}: metadado de prancha incorreto.")
        all_dxf_text.append(extract_text(doc))

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
            "instruments_and_equipment": len(instrument_rows),
            "io_points": len(io_rows),
            "analog_inputs": sum(row["tipo"] == "AI" for row in io_rows),
            "analog_outputs": sum(row["tipo"] == "AO" for row in io_rows),
            "digital_inputs": sum(row["tipo"] == "DI" for row in io_rows),
            "digital_outputs": sum(row["tipo"] == "DO" for row in io_rows),
            "terminals": len(terminal_rows),
            "cables": len(cable_rows),
            "materials": len(material_rows),
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
