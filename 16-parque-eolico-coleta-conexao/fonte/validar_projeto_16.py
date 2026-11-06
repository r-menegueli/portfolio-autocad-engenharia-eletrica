"""Confere a aritmetica, rastreabilidade e integridade CAD do Projeto 16."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "16-parque-eolico-coleta-conexao"
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
    "01_unifilar_coleta_conexao.dxf",
    "02_layout_parque_eolico.dxf",
    "03_base_calculo_interfaces.dxf",
)


def close(actual: float, expected: float, tol: float = 0.01) -> bool:
    return math.isclose(actual, expected, rel_tol=tol, abs_tol=tol)


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

    turbine_mw = 2.0
    turbine_count = 5
    total_mw = turbine_mw * turbine_count
    pf = 0.95
    calculations = (
        ("potencia total", total_mw, 10.0),
        ("aparente unitario", turbine_mw / pf, 2.105263),
        ("potencia equivalente TRG", 2.5 * pf, 2.375),
        ("margem TRG ativa", 2.5 * pf - turbine_mw, 0.375),
        ("aparente da planta", total_mw / pf, 10.526316),
        ("margem aparente TR-01", 12.5 - total_mw / pf, 1.973684),
        ("corrente WTG em 34,5 kV", turbine_mw * 1_000_000 / (math.sqrt(3) * 34_500 * pf), 35.24),
        ("corrente planta em 34,5 kV", total_mw * 1_000_000 / (math.sqrt(3) * 34_500 * pf), 176.20),
        ("corrente planta em 69 kV", total_mw * 1_000_000 / (math.sqrt(3) * 69_000 * pf), 88.10),
    )
    for label, actual, expected in calculations:
        checks += 1
        if not close(actual, expected):
            errors.append(f"Cálculo divergente ({label}): {actual:.5f} != {expected:.5f}")

    material_path = project_dir / "lista-materiais.csv"
    with material_path.open("r", encoding="utf-8-sig", newline="") as stream:
        materials = list(csv.DictReader(stream))
    checks += 1
    if not materials or not {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"}.issubset(materials[0]):
        errors.append("Cabeçalho ou conteúdo da lista de materiais inválido.")
    material_refs = " ".join(row.get("referencia", "") for row in materials)
    for tag in ("WTG-01", "WTG-02", "WTG-03", "WTG-04", "WTG-05", "TRG-01", "TRG-05", "CB-F01", "CB-F02", "CSE-01", "TR-01", "POI-01"):
        checks += 1
        if tag not in material_refs:
            errors.append(f"Tag não rastreada na lista de materiais: {tag}")

    signals_path = project_dir / "lista-sinais.csv"
    with signals_path.open("r", encoding="utf-8-sig", newline="") as stream:
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
        limits_min = tuple(doc.header.get("$LIMMIN", ()))[:2]
        limits_max = tuple(doc.header.get("$LIMMAX", ()))[:2]
        if limits_min != (0.0, 0.0) or limits_max != (420.0, 297.0):
            errors.append(f"Limites A3 divergentes em {filename}: {limits_min} / {limits_max}")

        values: list[str] = []
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
        "project": "P16",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "A validação calcula grandezas nominais com FP assumido e não verifica capacidade real de equipamentos.",
            "Não avalia recurso eólico, produção anual, perdas, curto-circuito, estabilidade, harmônicos ou conexão à rede.",
            "A auditoria independente do AutoCAD deve ser registrada separadamente.",
        ],
    }
    report = project_dir / "validacao-projeto-16.json"
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
