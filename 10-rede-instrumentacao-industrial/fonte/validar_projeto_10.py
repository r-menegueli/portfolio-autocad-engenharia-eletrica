"""Validação específica, determinística e rastreável do Projeto 10."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import ezdxf
from ezdxf import bbox
from PIL import Image
from pypdf import PdfReader


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from portfolio_config import load_config  # noqa: E402


WARNING = "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado."
SHEETS = (
    "01_arquitetura_rede",
    "02_diagrama_instrumentacao",
    "03_diagrama_interligacao",
    "04_topologia_comunicacao",
    "05_painel_instrumentacao",
    "06_lista_instrumentos",
    "07_matriz_causa_efeito_sinais",
    "08_matriz_escala_analogica",
    "09_balanco_carga_24vcc",
)
CAUSE_EFFECT_COLUMNS = ("id", "evento", "deteccao_condicao", "resposta_conceitual", "alarme_indicacao", "retorno_limite")
REQUIRED_DOCS = (
    "README.md", "memorial-descritivo.md", "criterios-premissas.md",
    "memoria-calculo.md", "filosofia-sinais.md", "referencias-normativas.md",
    "inspecao-visual.md", "parametros.csv", "lista-instrumentos.csv", "lista-io.csv",
    "lista-cabos.csv", "lista-bornes.csv", "lista-redes.csv",
    "lista-alimentacao.csv", "lista-materiais.csv", "resultados-calculo.csv", "causa-efeito.csv",
)
REQUIRED_TAGS = {"TT-101", "PT-102", "FT-103", "LT-104", "LSH-105", "PSL-106"}


class Validation:
    def __init__(self):
        self.checks = 0
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def require(self, condition: bool, message: str):
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def warn(self, condition: bool, message: str):
        self.checks += 1
        if not condition:
            self.warnings.append(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def entity_text(entity) -> str:
    if entity.dxftype() in {"TEXT", "ATTRIB", "ATTDEF"}:
        return entity.dxf.text
    if entity.dxftype() == "MTEXT":
        return entity.text
    if entity.dxftype() == "INSERT":
        return " ".join(attribute.dxf.text for attribute in entity.attribs)
    return ""


def validate_documents(v: Validation, project: Path):
    for name in REQUIRED_DOCS:
        path = project / name
        v.require(path.is_file(), f"arquivo obrigatório ausente: {name}")
        if path.is_file():
            v.require(path.stat().st_size > 32, f"arquivo vazio ou insuficiente: {name}")
    for name in ("README.md", "memorial-descritivo.md"):
        path = project / name
        if path.is_file():
            v.require(WARNING in path.read_text(encoding="utf-8"), f"aviso obrigatório ausente em {name}")


def validate_tables(v: Validation, project: Path):
    instruments = read_csv(project / "lista-instrumentos.csv")
    ios = read_csv(project / "lista-io.csv")
    cables = read_csv(project / "lista-cabos.csv")
    terminals = read_csv(project / "lista-bornes.csv")
    networks = read_csv(project / "lista-redes.csv")
    power = read_csv(project / "lista-alimentacao.csv")
    results = read_csv(project / "resultados-calculo.csv")
    cause_effect = read_csv(project / "causa-efeito.csv")

    tags = {row["tag"] for row in instruments}
    v.require(tags == REQUIRED_TAGS, f"tags de instrumentos divergentes: {sorted(tags)}")
    v.require(len(ios) == 6, "lista de I/O deve conter seis canais utilizados")
    v.require({row["tag"] for row in ios} == REQUIRED_TAGS, "tags de I/O não reconciliam instrumentos")
    v.require({row["cabo"] for row in instruments}.issubset({row["cabo"] for row in cables}), "cabos dos instrumentos não reconciliam lista de cabos")
    v.require({"BE-101", "PE-101"}.issubset({row["borne"] for row in terminals}), "barras BE-101/PE-101 ausentes")
    v.require({"PLC-101", "RIO-201", "RIO-202", "SCADA-101", "SW-101"}.issubset({row["no"] for row in networks}), "nós obrigatórios ausentes")
    v.require(len({row["ip"] for row in networks}) == len(networks), "endereços IP duplicados")

    expected_events = [f"E{index:02d}" for index in range(1, 9)]
    v.require([row.get("id", "") for row in cause_effect] == expected_events, "matriz deve conter E01-E08 em ordem")
    v.require(all(set(CAUSE_EFFECT_COLUMNS).issubset(row) for row in cause_effect), "colunas obrigatórias ausentes na matriz causa-efeito")
    for index, row in enumerate(cause_effect, start=1):
        v.require(all(row.get(column, "").strip() for column in CAUSE_EFFECT_COLUMNS), f"evento E{index:02d} possui campo vazio")
    v.require(
        all(any(term in " ".join(row.values()).casefold() for term in ("pendente", "dependem", "nao especificado")) for row in cause_effect),
        "cada evento deve manter explícitos os limites de hardware/projeto",
    )

    analog_rows = [row for row in instruments if "4-20" in row["sinal"]]
    current_points = (4.0, 8.0, 12.0, 16.0, 20.0)
    v.require(len(results) == len(analog_rows) * len(current_points), "resultados de escala devem conter cinco pontos para cada malha analógica")
    for row in instruments:
        if "4-20" in row["sinal"]:
            lrv, urv = float(row["lrv"]), float(row["urv"])
            v.require(urv > lrv, f"faixa inválida em {row['tag']}")
            for step in range(16001):
                current = 4.0 + step / 1000.0
                value = lrv + ((current - 4.0) / 16.0) * (urv - lrv)
                v.require(lrv - 1e-9 <= value <= urv + 1e-9, f"escala fora da faixa em {row['tag']} a {current} mA")
            selected = [r for r in results if r["tag"] == row["tag"]]
            actual = {float(r["corrente_ma"]): float(r["valor_engenharia"]) for r in selected}
            expected = {
                current: lrv + ((current - 4.0) / 16.0) * (urv - lrv)
                for current in current_points
            }
            v.require(len(selected) == len(current_points), f"quantidade de pontos de escala divergente em {row['tag']}")
            v.require(set(actual) == set(current_points), f"correntes de escala divergentes em {row['tag']}")
            for current, value in expected.items():
                v.require(abs(actual.get(current, 1e99) - value) < 1e-6, f"resultado de escala divergente em {row['tag']} / {current} mA")
        else:
            v.require(row["unidade"] == "estado", f"entrada digital sem unidade estado: {row['tag']}")

    total_current = sum(float(row["corrente_a"]) for row in power)
    total_power = sum(float(row["potencia_w"]) for row in power)
    v.require(abs(total_current - 3.10) < 1e-9, f"corrente total 24 Vcc divergente: {total_current}")
    v.require(abs(total_power - 74.40) < 1e-9, f"potência total 24 Vcc divergente: {total_power}")
    v.require(len(power) == 7, "balanço 24 Vcc deve manter os sete grupos documentados")
    v.require(all(abs(float(row["potencia_w"]) - 24.0 * float(row["corrente_a"])) < 1e-9 for row in power), "potências da lista 24 Vcc não reconciliam tensão e corrente")
    v.require(abs(10.0 - total_current - 6.90) < 1e-9, "saldo aritmético da fonte PS1 deve ser 6,90 A")
    v.require(abs(240.0 - total_power - 165.60) < 1e-9, "saldo aritmético de potência deve ser 165,60 W")
    v.require(total_current <= 10.0 * 0.8, "fonte PS1 ultrapassa 80 % da corrente nominal")

    cable_text = " ".join(" ".join(row.values()) for row in cables).lower()
    for term in ("4-20 ma", "alimentação", "entrada digital", "comunicação", "blindagem"):
        v.require(term in cable_text, f"conceito ausente na lista de cabos: {term}")


def validate_dxf(v: Validation, root: Path, project: Path):
    config = load_config(root)
    required_layers = set(config["layers"]["required"])
    for stem in SHEETS:
        path = project / "fonte" / f"{stem}.dxf"
        v.require(path.is_file(), f"DXF ausente: {path.name}")
        if not path.is_file():
            continue
        try:
            doc = ezdxf.readfile(path)
        except Exception as exc:
            v.require(False, f"DXF ilegível {path.name}: {exc}")
            continue
        auditor = doc.audit()
        v.require(not auditor.errors, f"erros de auditoria ezdxf em {path.name}: {len(auditor.errors)}")
        v.require(doc.dxfversion == "AC1027", f"versão DXF incorreta em {path.name}: {doc.dxfversion}")
        v.require(doc.header.get("$INSUNITS") == 4, f"$INSUNITS não é mm em {path.name}")
        v.require(required_layers.issubset({layer.dxf.name for layer in doc.layers}), f"layers obrigatórios ausentes em {path.name}")
        metadata = doc.ezdxf_metadata()
        v.require(metadata.get("PORTFOLIO_PROJECT") == "10-rede-instrumentacao-industrial", f"metadado de projeto incorreto em {path.name}")
        v.require(metadata.get("PORTFOLIO_SHEET") == f"{SHEETS.index(stem) + 1:02d}/{len(SHEETS):02d}", f"metadado de prancha incorreto em {path.name}")
        text = " ".join(entity_text(entity) for entity in doc.modelspace())
        for token in (WARNING, "Rogério Eduardo Moreira Menegueli", "mm", "01", "CONCEIT."):
            v.require(token in text, f"texto obrigatório ausente em {path.name}: {token}")
        v.require("BALANCO DE CARGA" in text, f"descrição da revisão incorreta em {path.name}")
        extents = bbox.extents(doc.modelspace(), fast=True)
        v.require(extents.has_data, f"DXF sem geometria: {path.name}")
        if extents.has_data:
            v.require(extents.extmin.x >= 9.5 and extents.extmin.y >= 9.5, f"entidade abaixo da moldura em {path.name}")
            v.require(extents.extmax.x <= 410.5 and extents.extmax.y <= 287.5, f"entidade acima da moldura em {path.name}")
        for required in ("PLC-101", "RIO-201", "RIO-202", "SCADA-101", "24 Vcc"):
            if stem in {"01_arquitetura_rede", "04_topologia_comunicacao"}:
                v.require(required in text, f"conteúdo de arquitetura ausente em {path.name}: {required}")
        if stem == "07_matriz_causa_efeito_sinais":
            for required in ("MATRIZ CAUSA-EFEITO DE SINAIS", "E01", "E08", "AI-001", "RIO-201", "SCADA-101"):
                v.require(required in text, f"conteúdo da matriz ausente em {path.name}: {required}")
        if stem == "08_matriz_escala_analogica":
            for required in ("MATRIZ DE ESCALA ANALÓGICA", "TT-101", "PT-102", "FT-103", "LT-104", "112,5 °C", "1,25 m", "100 %"):
                v.require(required in text, f"conteúdo da matriz de escala ausente em {path.name}: {required}")
        if stem == "09_balanco_carga_24vcc":
            for required in ("BALANÇO DE CARGA 24 VCC", "TOTAL PREVISTO", "3,10", "74,40", "6,90", "165,60", "1,05", "69 %"):
                v.require(required in text, f"conteúdo do balanço 24 Vcc ausente em {path.name}: {required}")


def validate_exports(v: Validation, project: Path):
    for stem in SHEETS:
        for suffix in ("pdf", "svg", "png"):
            path = project / "exports" / f"{stem}.{suffix}"
            v.require(path.is_file() and path.stat().st_size > 1000, f"derivado ausente ou vazio: {path.name}")
        pdf = project / "exports" / f"{stem}.pdf"
        png = project / "exports" / f"{stem}.png"
        svg = project / "exports" / f"{stem}.svg"
        if pdf.is_file():
            reader = PdfReader(pdf)
            v.require(len(reader.pages) == 1, f"PDF deve ter uma página: {pdf.name}")
            box = reader.pages[0].mediabox
            width_mm = float(box.width) * 25.4 / 72.0
            height_mm = float(box.height) * 25.4 / 72.0
            v.require(abs(width_mm - 420.0) < 1.0 and abs(height_mm - 297.0) < 1.0, f"PDF não é A3 paisagem: {pdf.name}")
        if png.is_file():
            with Image.open(png) as image:
                v.require(image.width >= 2400, f"PNG com largura insuficiente: {png.name}")
                v.require(image.width > image.height, f"PNG não está em paisagem: {png.name}")
        if svg.is_file():
            svg_text = svg.read_text(encoding="utf-8")
            v.require("<svg" in svg_text and "viewBox" in svg_text, f"SVG inválido: {svg.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    project = root / "10-rede-instrumentacao-industrial"
    validation = Validation()
    validate_documents(validation, project)
    if all((project / name).is_file() for name in REQUIRED_DOCS):
        validate_tables(validation, project)
    validate_dxf(validation, root, project)
    validate_exports(validation, project)
    report = {
        "project": "P10",
        "date": "2026-11-05",
        "status": "PASS" if not validation.errors else "FAIL",
        "checks": validation.checks,
        "errors": validation.errors,
        "warnings": validation.warnings,
    }
    output = project / "validacao-instrumentacao.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not validation.errors else 1)


if __name__ == "__main__":
    main()
