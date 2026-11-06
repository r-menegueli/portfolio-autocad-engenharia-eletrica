"""Valida contas de FP, degraus de compensacao e integridade CAD do P18."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "18-compensacao-reativos-qualidade-energia"
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
    "01_unifilar_compensacao_reativos.dxf",
    "02_memoria_correcao_fator_potencia.dxf",
    "03_medicao_controle_harmonicos.dxf",
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

    p = 600.0
    pf0 = 0.80
    pft = 0.95
    q0 = p * math.tan(math.acos(pf0))
    qt = p * math.tan(math.acos(pft))
    qc = q0 - qt
    q_after_250 = q0 - 250.0
    s0 = p / pf0
    s250 = math.hypot(p, q_after_250)
    expected = (
        ("Q inicial", q0, 450.0),
        ("Q alvo", qt, 197.21),
        ("Qc requerido", qc, 252.79),
        ("FP com 250 kvar", p / s250, 0.948683),
        ("corrente sem banco", s0 * 1000 / (math.sqrt(3) * 400), 1082.53),
        ("corrente com 250 kvar", s250 * 1000 / (math.sqrt(3) * 400), 912.87),
        ("FP com 275 kvar", p / math.hypot(p, q0 - 275.0), 0.96),
    )
    for label, actual, value in expected:
        checks += 1
        if not math.isclose(actual, value, rel_tol=0.001, abs_tol=0.01):
            errors.append(f"Cálculo divergente ({label}): {actual:.5f} != {value:.5f}")

    curves = read_csv(project_dir / "curva-compensacao.csv")
    checks += 1
    expected_columns = {"caso", "p_kw", "fp_inicial", "q_inicial_kvar", "q_alvo_kvar", "qc_kvar", "degraus_25kvar", "fp_com_degraus", "observacoes"}
    if not curves or not expected_columns.issubset(curves[0]):
        errors.append("Cabeçalho ou dados da curva de compensação inválidos.")
    for row in curves:
        p_row = float(row["p_kw"])
        pf_row = float(row["fp_inicial"])
        q_row = p_row * math.tan(math.acos(pf_row))
        target_row = p_row * math.tan(math.acos(0.95))
        calculated = q_row - target_row
        checks += 1
        if abs(calculated - float(row["qc_kvar"])) > 0.2:
            errors.append(f"Qc divergente na curva: {row.get('caso', '')}")

    materials = read_csv(project_dir / "lista-materiais.csv")
    checks += 1
    if not materials or not {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"}.issubset(materials[0]):
        errors.append("Cabeçalho ou dados da lista de materiais inválidos.")
    refs = " ".join(row.get("referencia", "") for row in materials)
    for tag in ("BC-01", "RC-01", "PM-01", "CT-01", "QGBT-01", "TR-01", "CARGA-VFD"):
        checks += 1
        if tag not in refs:
            errors.append(f"Tag não rastreada na lista de materiais: {tag}")

    signals = read_csv(project_dir / "lista-sinais.csv")
    checks += 1
    signal_columns = {"sinal", "origem", "destino", "funcao", "dado_esperado", "interface", "estado"}
    if not signals or not signal_columns.issubset(signals[0]):
        errors.append("Cabeçalho ou dados da lista de sinais inválidos.")

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
        values: list[str] = []
        for entity in doc.modelspace().query("TEXT MTEXT ATTRIB"):
            value = entity.dxf.get("text", "") if entity.dxftype() != "MTEXT" else entity.plain_text()
            values.append(value.replace("\\P", " "))
        for insert in doc.modelspace().query("INSERT"):
            values.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any(WARNING in value for value in values):
            errors.append(f"Aviso obrigatório ausente em {filename}")
        checks += 1
        if not any(f"{index:02d}/03" in value for value in values):
            errors.append(f"Número de prancha {index:02d}/03 ausente em {filename}")

    result = {
        "project": "P18",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Contas aritmeticas com premissas; nao dimensionam equipamento ou estudo de rede.",
            "Nao incluem espectro harmonico, impedancia da fonte, ressonancia, perdas ou perfil horario medido.",
            "Auditoria independente pelo AutoCAD deve ser registrada separadamente.",
        ],
    }
    report = project_dir / "validacao-projeto-18.json"
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
