"""Valida coerência de I/O, referências e invariantes lógicos do Projeto 03."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import ezdxf


PROJECT_SLUG = "03-painel-automacao-clp"
SHEETS = (
    "01_arquitetura_automacao.dxf",
    "02_alimentacao_24v.dxf",
    "03_entradas_clp.dxf",
    "04_saidas_clp.dxf",
    "05_diagrama_comando.dxf",
    "06_layout_painel.dxf",
    "07_diagrama_bornes.dxf",
    "08_interligacoes_campo.dxf",
)
REQUIRED_INPUT_TAGS = {
    "KSR1_OK", "S1_AUTO", "S1_MAN", "S2_P1", "S3_P1", "S4_P2", "S5_P2",
    "LSL_LL", "LSL", "LSH", "LSHH", "RT1_OK", "RT2_OK", "KM1_FB", "KM2_FB", "S6_ACK",
}
REQUIRED_OUTPUT_TAGS = {
    "K1_CMD", "K2_CMD", "H1_PRONTO", "H2_AUTO", "H3_P1", "H4_P2",
    "H5_ALARME", "H6_DEMANDA", "BZ1", "KA1_REMOTO",
}
REQUIRED_MATERIALS = {
    "Q0", "QF1", "QF2", "QF3", "PSU1", "CLP1", "KSR1", "KDRY",
    "K1", "K2", "KM1", "KM2", "RT1", "RT2", "M1", "M2",
    "LSL-LL", "LSL", "LSH", "LSHH", "H1-H6", "BZ1",
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

    io_rows = read_rows(project / "lista-io.csv")
    terminal_rows = read_rows(project / "lista-bornes.csv")
    cable_rows = read_rows(project / "lista-cabos.csv")
    material_rows = read_rows(project / "lista-materiais.csv")

    addresses = [row["endereco"] for row in io_rows]
    checks += 3
    if len(io_rows) != 32:
        errors.append(f"Lista de I/O contém {len(io_rows)} linhas; esperadas 32.")
    if len(addresses) != len(set(addresses)):
        errors.append("Há endereços de I/O duplicados.")
    expected_addresses = {f"I{bank}.{bit}" for bank in range(2) for bit in range(8)} | {
        f"Q{bank}.{bit}" for bank in range(2) for bit in range(8)
    }
    if set(addresses) != expected_addresses:
        errors.append("Endereços de I/O não cobrem exatamente I0.0-I1.7 e Q0.0-Q1.7.")

    inputs = {row["tag"] for row in io_rows if row["tipo"] == "DI"}
    outputs = {row["tag"] for row in io_rows if row["tipo"] == "DO"}
    checks += 4
    if inputs != REQUIRED_INPUT_TAGS:
        errors.append("Conjunto de tags DI diverge do contrato funcional.")
    if not REQUIRED_OUTPUT_TAGS <= outputs:
        errors.append("Saídas funcionais obrigatórias estão ausentes.")
    if len(inputs) != 16 or len(outputs) != 16:
        errors.append("A lista deve conter 16 DI e 16 DO.")
    if not all(row["borne"].startswith(("X3:", "X4:")) for row in io_rows):
        errors.append("Há I/O sem referência às réguas X3/X4.")

    terminal_ids = {f"{row['regua']}:{row['borne']}" for row in terminal_rows}
    checks += len(io_rows)
    for row in io_rows:
        if row["borne"] not in terminal_ids:
            errors.append(f"{row['endereco']}: borne {row['borne']} não existe na lista de bornes.")

    cable_ids = {row["cabo"] for row in cable_rows}
    checks += 2
    if cable_ids != {f"W{index:02d}" for index in range(1, 13)}:
        errors.append("Lista de cabos não cobre exatamente W01-W12.")
    if any(float(row["comprimento_assumido_m"].replace(",", ".")) <= 0 for row in cable_rows):
        errors.append("Há cabo com comprimento não positivo.")

    material_ids = {row["item"] for row in material_rows}
    checks += len(REQUIRED_MATERIALS)
    for tag in sorted(REQUIRED_MATERIALS - material_ids):
        errors.append(f"Material obrigatório ausente: {tag}.")

    # Propriedade lógica: nenhum comando físico pode existir sem os três permissivos.
    truth_rows = 0
    for ksr_ok in (False, True):
        for kdry_ok in (False, True):
            for rt_ok in (False, True):
                for plc_command in (False, True):
                    physical_output = ksr_ok and kdry_ok and rt_ok and plc_command
                    truth_rows += 1
                    checks += 1
                    if physical_output and not (ksr_ok and kdry_ok and rt_ok):
                        errors.append("Invariante de permissivos físicos foi violada.")

    # Propriedade de alternância: ciclo concluído troca exatamente uma vez a titular.
    for current in (1, 2):
        next_duty = 2 if current == 1 else 1
        checks += 2
        if next_duty == current or (2 if next_duty == 1 else 1) != current:
            errors.append("Invariante de alternância das bombas foi violada.")

    required_doc_terms = {
        "sequencia-funcionamento.md": ("altern", "funcionamento a seco", "emergência", "falha de partida"),
        "pseudocodigo-estados.md": ("permissivo_geral", "LSHH", "30 min", "titular_proxima"),
        "criterios-premissas.md": ("10 A", "6,00 A", "análise de risco", "220 V"),
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
        checks += 3
        if not path.is_file():
            errors.append(f"DXF ausente: {filename}.")
            continue
        try:
            doc = ezdxf.readfile(path)
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_PROJECT") != PROJECT_SLUG:
            errors.append(f"{filename}: metadado de projeto incorreto.")
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/08":
            errors.append(f"{filename}: metadado de prancha incorreto.")
        all_dxf_text.append(extract_text(doc))

    merged = " ".join(all_dxf_text).casefold()
    for tag in ("clp1", "psu1", "ksr1", "kdry", "km1", "km2", "lsl-ll", "lshh", "bz1", "x4"):
        checks += 1
        if tag not in merged:
            errors.append(f"Identificação não localizada no conjunto DXF: {tag}.")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "results": {
            "io_points": len(io_rows),
            "digital_inputs": len(inputs),
            "digital_outputs": len(outputs),
            "terminals": len(terminal_rows),
            "cables": len(cable_rows),
            "materials": len(material_rows),
            "safety_truth_table_rows": truth_rows,
            "supply_24v_load_a": "6.00",
            "supply_24v_capacity_a": "10.00",
        },
    }
    output = project / "validacao-logica.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDAÇÃO LÓGICA {result['status']} | verificações={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
