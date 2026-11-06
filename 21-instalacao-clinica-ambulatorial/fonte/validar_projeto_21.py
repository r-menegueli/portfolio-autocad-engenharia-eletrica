"""Valida a rastreabilidade e integridade estrutural do Projeto 21."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "21-instalacao-clinica-ambulatorial"
BOX_BLOCK = "P21_CAIXA_EQUIPAMENTO"
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
    "01_planta_eletrica_clinica.dxf",
    "02_unifilar_fontes_quadro_clinica.dxf",
    "03_matriz_continuidade_e_transferencia.dxf",
)
REQUIRED_FILES = (
    "README.md", "memorial-descritivo.md", "criterios-premissas.md",
    "referencias-normativas.md", "inspecao-visual.md", "lista-materiais.csv",
    "lista-sinais.csv", "matriz-cargas.csv", "plano-estudos.csv",
    "fonte/gerar_projeto_21.py", "fonte/validar_projeto_21.py",
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

    for relative in REQUIRED_FILES:
        checks += 1
        if not (project_dir / relative).is_file():
            errors.append(f"Arquivo requerido ausente: {relative}")
    for relative in ("README.md", "memorial-descritivo.md"):
        checks += 1
        path = project_dir / relative
        if path.is_file() and WARNING not in path.read_text(encoding="utf-8"):
            errors.append(f"Aviso obrigatório ausente: {relative}")

    materials = read_csv(project_dir / "lista-materiais.csv")
    checks += 1
    if not materials or not {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"}.issubset(materials[0]):
        errors.append("Cabeçalho ou conteúdo da lista de materiais inválido.")
    refs = " ".join(row.get("referencia", "") for row in materials)
    for tag in ("PCC-01", "MED-01", "QGBT-CL", "QD-N", "QTA-CL", "GE-CL", "UPS-CL", "QD-U", "QD-E", "L1", "LE1", "T1", "U1"):
        checks += 1
        if tag not in refs:
            errors.append(f"Tag não rastreada na lista de materiais: {tag}")

    signals = read_csv(project_dir / "lista-sinais.csv")
    checks += 1
    if not signals or not {"sinal", "origem", "destino", "funcao", "dado_esperado", "interface", "estado"}.issubset(signals[0]):
        errors.append("Cabeçalho ou conteúdo da lista de sinais inválido.")
    checks += 1
    if len(signals) != 8:
        errors.append(f"Quantidade de sinais divergente: {len(signals)}")

    loads = read_csv(project_dir / "matriz-cargas.csv")
    checks += 1
    if not loads or not {"grupo_carga", "normal", "gerador", "ups", "decisao_evidencia"}.issubset(loads[0]):
        errors.append("Cabeçalho ou conteúdo da matriz de cargas inválido.")
    checks += 1
    if len(loads) != 6:
        errors.append(f"Quantidade de grupos de carga divergente: {len(loads)}")
    checks += 1
    if any(row.get("gerador", "").upper() not in {"A ESTUDAR", "A DEFINIR", "PROPOSTA"} for row in loads):
        errors.append("A matriz de cargas contém uma decisão de gerador não classificada como pendente/proposta.")

    studies = read_csv(project_dir / "plano-estudos.csv")
    checks += 1
    if not studies or not {"estudo", "entradas_necessarias", "saida_esperada", "responsavel_a_definir", "status"}.issubset(studies[0]):
        errors.append("Cabeçalho ou conteúdo do plano de estudos inválido.")
    checks += 1
    if len(studies) < 8:
        errors.append("Plano de estudos incompleto.")

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
            values.append(entity.plain_text() if entity.dxftype() == "MTEXT" else entity.dxf.get("text", ""))
        for insert in doc.modelspace().query("INSERT"):
            values.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any(WARNING in value for value in values):
            errors.append(f"Aviso obrigatório ausente em {filename}")
        checks += 1
        if not any(f"{index:02d}/03" in value for value in values):
            errors.append(f"Número de prancha {index:02d}/03 ausente em {filename}")
        checks += 1
        required_label = ("L1", "QTA-CL", "Iluminacao de emergencia")[index - 1]
        if not any(required_label.casefold() in value.casefold() for value in values):
            errors.append(f"Conteúdo específico ausente em {filename}: {required_label}")
        if index == 2:
            checks += 1
            if BOX_BLOCK not in doc.blocks or not any(entity.dxf.name == BOX_BLOCK for entity in doc.modelspace().query("INSERT")):
                errors.append(f"Bloco reutilizável ausente ou sem inserção em {filename}")

    result = {
        "project": "P21",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Planta, cargas, fontes e distribuicao sao ilustrativas e nao estao dimensionadas.",
            "Nenhum local medico foi classificado e nenhuma carga foi aprovada como essencial.",
            "Aprovacoes sanitarias, estudos eletricos, ensaios e auditoria CAD independente nao sao substituidos por esta validacao.",
        ],
    }
    report = project_dir / "validacao-projeto-21.json"
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
