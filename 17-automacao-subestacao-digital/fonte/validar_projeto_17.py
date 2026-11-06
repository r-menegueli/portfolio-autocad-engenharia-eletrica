"""Verifica estrutura, rastreabilidade e tabelas da automacao conceitual P17."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "17-automacao-subestacao-digital"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402

WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação "
    "ou execução de serviços sem revisão, dimensionamento e responsabilidade de "
    "profissional legalmente habilitado."
)
SHEETS = (
    "01_unifilar_sas_ied.dxf",
    "02_rede_iec61850.dxf",
    "03_matriz_goose_testes.dxf",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check(root: Path) -> dict:
    project_dir = root / SLUG
    errors: list[str] = []
    checks = 0
    config = load_config(root)
    required = set(required_layers(config))

    for relative in ("README.md", "memorial-descritivo.md"):
        checks += 1
        path = project_dir / relative
        if not path.is_file() or WARNING not in path.read_text(encoding="utf-8"):
            errors.append(f"Aviso obrigatório ausente: {relative}")

    tables = {
        "lista-ieds.csv": {"tag", "funcao", "interfaces", "rede", "observacoes"},
        "matriz-goose.csv": {"id", "publisher", "subscriber", "dataset", "funcao", "acao_por_perda", "estado"},
        "lista-sinais.csv": {"sinal", "origem", "destino", "funcao", "dado_esperado", "interface", "estado"},
        "plano-verificacao.csv": {"id", "etapa", "verificacao", "evidencia", "precondicao", "estado"},
        "lista-materiais.csv": {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"},
    }
    loaded: dict[str, list[dict[str, str]]] = {}
    for filename, required_columns in tables.items():
        rows = read_csv(project_dir / filename)
        loaded[filename] = rows
        checks += 1
        if not rows or not required_columns.issubset(rows[0]):
            errors.append(f"Cabeçalho ou conteúdo inválido: {filename}")

    ied_tags = {row.get("tag", "") for row in loaded["lista-ieds.csv"]}
    for tag in ("IED-L01", "IED-L02", "IED-T01", "IED-87B", "IED-F01", "IED-F02", "IED-BAY-L01", "IED-BAY-T01", "MU-L01", "MU-T01", "MU-B01", "MU-F01", "MU-F02", "SW-PROC-01", "SW-STA-01", "GW-01", "HMI-01", "ENG-01", "TS-01"):
        checks += 1
        if tag not in ied_tags:
            errors.append(f"Equipamento sem registro no inventário: {tag}")

    for row in loaded["matriz-goose.csv"]:
        for column in ("publisher", "subscriber"):
            checks += 1
            if row.get(column, "") not in ied_tags:
                errors.append(f"{column} não cadastrado no inventário GOOSE: {row.get(column, '')}")

    goose_ids = {row.get("id", "") for row in loaded["matriz-goose.csv"]}
    for signal in ("G-TR-L01", "G-BF-F01", "G-ILK-L02", "G-BF-F02", "G-TR-T01"):
        checks += 1
        if signal not in goose_ids:
            errors.append(f"Evento GOOSE ausente: {signal}")

    for index, filename in enumerate(SHEETS, 1):
        path = project_dir / "fonte" / filename
        checks += 1
        if not path.is_file():
            errors.append(f"DXF ausente: {path.relative_to(root)}")
            continue
        try:
            doc = ezdxf.readfile(path)
            audit = doc.audit()
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        checks += 1
        if audit.errors:
            errors.append(f"Auditoria DXF retornou {len(audit.errors)} erro(s): {filename}")
        checks += 1
        missing = required - {layer.dxf.name for layer in doc.layers}
        if missing:
            errors.append(f"Layers ausentes em {filename}: {', '.join(sorted(missing))}")
        checks += 1
        if int(doc.header.get("$INSUNITS", 0)) != 4:
            errors.append(f"$INSUNITS diferente de mm em {filename}")
        checks += 1
        if doc.dxfversion != "AC1027":
            errors.append(f"Versão DXF diferente de AC1027 em {filename}")
        checks += 1
        limits_min = tuple(doc.header.get("$LIMMIN", ()))[:2]
        limits_max = tuple(doc.header.get("$LIMMAX", ()))[:2]
        if limits_min != (0.0, 0.0) or limits_max != (420.0, 297.0):
            errors.append(f"Limites A3 divergentes em {filename}")
        values: list[str] = []
        for entity in doc.modelspace().query("TEXT MTEXT ATTRIB"):
            value = entity.dxf.get("text", "") if entity.dxftype() != "MTEXT" else entity.plain_text()
            values.append(value.replace("\\P", " "))
        for insert in doc.modelspace().query("INSERT"):
            values.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any(WARNING in value for value in values):
            errors.append(f"Texto literal do aviso ausente em {filename}")
        checks += 1
        if not any(f"{index:02d}/03" in value for value in values):
            errors.append(f"Número de prancha {index:02d}/03 ausente em {filename}")

    result = {
        "project": "P17",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Verificacoes estruturais e de rastreabilidade; nao simulam comunicacao IEC 61850 ou atuacao real.",
            "Nao incluem ajustes de protecao, configuracoes SCL de fabricante, latencia ou ensaios FAT/SAT executados.",
            "A auditoria independente pelo AutoCAD deve ser registrada separadamente.",
        ],
    }
    report = project_dir / "validacao-projeto-17.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
