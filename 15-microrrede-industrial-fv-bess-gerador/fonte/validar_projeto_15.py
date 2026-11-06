"""Verifica aritmetica, rastreabilidade e integridade CAD do Projeto 15."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "15-microrrede-industrial-fv-bess-gerador"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402

SHEETS = (
    "01_unifilar_microrrede.dxf",
    "02_layout_fontes_cargas.dxf",
    "03_operacao_balanco_energia.dxf",
)
WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação "
    "ou execução de serviços sem revisão, dimensionamento e responsabilidade de "
    "profissional legalmente habilitado."
)


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

    calculations = (
        ("carga total", 800 + 200, 1000),
        ("modo conectado", 600 + 400, 1000),
        ("ilha FV alta", 600 + 400 + 0, 1000),
        ("ilha FV baixa", 200 + 500 + 300, 1000),
        ("ilha sem FV", 0 + 500 + 500, 1000),
        ("GE indisponível", 300 + 0 + 500, 800),
        ("duração BESS ideal", 1000 / 500, 2),
        ("capacidade TR ativa", 1500 * 0.95, 1425),
        ("margem TR", 1500 * 0.95 - 1000, 425),
    )
    for label, actual, expected in calculations:
        checks += 1
        if round(actual, 2) != expected:
            errors.append(f"Cálculo divergente ({label}): {actual} != {expected}")

    with (project_dir / "lista-materiais.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        materials = list(csv.DictReader(stream))
    checks += 1
    if not materials or not {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"}.issubset(materials[0]):
        errors.append("Cabeçalho ou conteúdo da lista de materiais inválido.")
    refs = " ".join(row.get("referencia", "") for row in materials)
    for tag in ("PCC-01", "TR-01", "QGBT-MG", "FV-01", "BESS-01", "BAT-01", "GE-01", "CARGA-CRIT", "CARGA-NCRIT"):
        checks += 1
        if tag not in refs:
            errors.append(f"Tag {tag} não rastreada na lista de materiais.")

    with (project_dir / "lista-sinais.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        signals = list(csv.DictReader(stream))
    checks += 1
    if not signals or not {"sinal", "origem", "destino", "funcao", "dado_esperado", "interface", "estado"}.issubset(signals[0]):
        errors.append("Cabeçalho ou conteúdo da lista de sinais inválido.")

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
        if tuple(doc.header.get("$LIMMIN", ()))[:2] != (0.0, 0.0) or tuple(doc.header.get("$LIMMAX", ()))[:2] != (420.0, 297.0):
            errors.append(f"Limites A3 divergentes em {filename}")
        values = []
        for entity in doc.modelspace().query("TEXT MTEXT ATTRIB"):
            value = entity.dxf.get("text", "") if entity.dxftype() != "MTEXT" else entity.plain_text()
            values.append(value.replace("\\P", " "))
        for insert in doc.modelspace().query("INSERT"):
            values.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any("AVISO OBRIGATORIO" in value for value in values):
            errors.append(f"Chamada do aviso ausente em {filename}")
        checks += 1
        if not any(WARNING in value for value in values):
            errors.append(f"Texto literal do aviso ausente em {filename}")
        checks += 1
        if not any(f"{index:02d}/03" in value for value in values):
            errors.append(f"Número de prancha {index:02d}/03 ausente em {filename}")

    result = {
        "project": "P15",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Validação aritmética e estrutural; não é verificação de conformidade normativa.",
            "Não modela estabilidade, proteção, interconexão, autonomia ou degradação.",
            "Auditoria independente do AutoCAD deve ser registrada separadamente.",
        ],
    }
    report = project_dir / "validacao-projeto-15.json"
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
