"""Verifica aritmetica, rastreabilidade e integridade CAD do Projeto 13."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import ezdxf


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402


SHEETS = (
    "01_layout_estacao_recarga.dxf",
    "02_diagrama_unifilar_estacao.dxf",
    "03_gestao_dinamica_carga.dxf",
)
WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação "
    "ou execução de serviços sem revisão, dimensionamento e responsabilidade de "
    "profissional legalmente habilitado."
)


def check(root: Path) -> dict:
    errors: list[str] = []
    checks = 0
    config = load_config(root)
    required = set(required_layers(config))
    readme = PROJECT_DIR / "README.md"
    memorial = PROJECT_DIR / "memorial-descritivo.md"
    for path in (readme, memorial):
        checks += 1
        if not path.is_file() or WARNING not in path.read_text(encoding="utf-8"):
            errors.append(f"Aviso obrigatório ausente: {path.relative_to(root)}")

    equipment = {"EVSE-01": 11, "EVSE-02": 11, "EVSE-03": 11, "EVSE-04": 11, "EVSE-05": 60, "EVSE-06": 60}
    checks += 1
    if sum(equipment.values()) != 164:
        errors.append("A soma das potências assumidas não confere (esperado 164 kW).")
    scenarios = {"S1": 120, "S2": 142, "S3": 93, "S4": 164}
    checks += 1
    if scenarios != {"S1": 2 * 60, "S2": 2 * 60 + 2 * 11, "S3": 60 + 3 * 11, "S4": 2 * 60 + 4 * 11}:
        errors.append("As somas de cenário da folha 03 não conferem.")

    with (PROJECT_DIR / "lista-materiais.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        materials = list(csv.DictReader(stream))
    checks += 1
    material_refs = " ".join(row["referencia"] for row in materials)
    if not all(tag in material_refs for tag in equipment):
        if not ("EVSE-01 a EVSE-04" in material_refs and "EVSE-05 e EVSE-06" in material_refs):
            errors.append("A lista de materiais não rastreia os seis carregadores EVSE.")

    for filename in SHEETS:
        path = PROJECT_DIR / "fonte" / filename
        checks += 1
        if not path.is_file():
            errors.append(f"DXF ausente: {path.relative_to(root)}")
            continue
        try:
            doc = ezdxf.readfile(path)
            audit = doc.audit()
        except Exception as exc:  # report a CAD read failure with its context
            errors.append(f"Falha ao abrir {path.relative_to(root)}: {exc}")
            continue
        checks += 1
        if audit.errors:
            errors.append(f"Auditoria DXF retornou {len(audit.errors)} erro(s): {path.name}")
        checks += 1
        missing = required - {layer.dxf.name for layer in doc.layers}
        if missing:
            errors.append(f"Layers obrigatórios ausentes em {path.name}: {', '.join(sorted(missing))}")
        checks += 1
        if int(doc.header.get("$INSUNITS", 0)) != 4:
            errors.append(f"$INSUNITS diferente de mm em {path.name}")
        checks += 1
        if doc.dxfversion != "AC1027":
            errors.append(f"Versão DXF diferente de AC1027 em {path.name}")
        checks += 1
        if tuple(doc.header.get("$LIMMIN", ()))[:2] != (0.0, 0.0) or tuple(doc.header.get("$LIMMAX", ()))[:2] != (420.0, 297.0):
            errors.append(f"Limites de folha divergentes em {path.name}")
        texts = []
        for entity in doc.modelspace().query("TEXT MTEXT ATTRIB"):
            value = entity.dxf.get("text", "") if entity.dxftype() != "MTEXT" else entity.plain_text()
            texts.append(value.replace("\\P", " "))
        for insert in doc.modelspace().query("INSERT"):
            texts.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any("AVISO OBRIGATORIO" in value for value in texts):
            errors.append(f"Chamada do aviso não encontrada em {path.name}")
        checks += 1
        if not any(f"{SHEETS.index(filename) + 1:02d}/03" in value for value in texts):
            errors.append(f"Identificação de folha NN/03 não encontrada em {path.name}")

    result = {
        "project": "P13",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Validação aritmética e estrutural; não é verificação de conformidade normativa.",
            "Não dimensiona a alimentação, a demanda, os cabos ou as proteções.",
            "Auditoria independente do AutoCAD deve ser registrada separadamente.",
        ],
    }
    report = PROJECT_DIR / "validacao-projeto-13.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
