"""Gera tres pranchas conceituais do sistema eletrico de um parque eolico."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment


DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "16-parque-eolico-coleta-conexao"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gerar_template_a3 import (  # noqa: E402
    TITLE_BLOCK_NAME,
    PROJECT_PRINT_LAYER_COLORS,
    TITLE_STYLE,
    TEXT_STYLE,
    add_frame,
    add_line,
    add_mtext,
    add_rect,
    add_text,
    configure_document,
    define_title_block,
    prepare_deterministic_write,
)
from portfolio_config import SheetGeometry, load_config  # noqa: E402


DATE = "2026-11-06"
REVISION = "00"


def text(layout, value: str, x: float, y: float, h: float = 1.7,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(
        layout,
        value,
        (x, y),
        h,
        layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
        style=TITLE_STYLE if bold else TEXT_STYLE,
    )


def line(layout, a: tuple[float, float], b: tuple[float, float],
         layer: str = "02_TEXTO") -> None:
    add_line(layout, a, b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float,
        title: str, detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        detail_height: float = 1.25) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    midx = (x0 + x1) / 2
    midy = (y0 + y1) / 2
    if detail:
        text(layout, title, midx, midy + 2.3, 1.55, layer, centered=True, bold=True)
        text(layout, detail, midx, midy - 2.1, detail_height, "02_TEXTO", centered=True)
    else:
        text(layout, title, midx, midy, 1.55, layer, centered=True, bold=True)


def arrow(layout, start: tuple[float, float], end: tuple[float, float],
          layer: str, size: float = 2.0) -> None:
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(
            layout,
            (end[0] - ux * size + side * px * size * 0.55,
             end[1] - uy * size + side * py * size * 0.55),
            end,
            layer,
        )


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 3.0, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.55, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66.5, 1.8, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.34, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90.5, 1.8, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.3, "12_LEGENDA")

    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, value, x, 89.5, 1.4, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.35, "02_TEXTO", centered=True)


def make_sheet(root: Path, config: dict, number: int, spec: dict) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height), layer_color_overrides=PROJECT_PRINT_LAYER_COLORS)
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    spec["draw"](layout)
    footer(layout, spec, config["portfolio"]["warning"])
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(
        {
            "TITULO": spec["title"],
            "AUTOR": config["portfolio"]["author"],
            "DATA": DATE,
            "REVISAO": REVISION,
            "PRANCHA": f"{number:02d}/03",
            "ARQUIVO": spec["filename"],
            "UNIDADES": "mm",
            "ESCALA": spec["scale"],
            "FOLHA": "A3",
            "STATUS": "CONCEIT.",
        }
    )
    output = root / SLUG / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def draw_single_line(layout) -> None:
    text(layout, "COLETA EM 34,5 kV | CINCO UNIDADES | 10 MW INSTALADOS*", 24, 250, 1.7, "05_POTENCIA", bold=True)
    # Feeder A: three turbines connected radially to the collector bus.
    feeder_a = (
        (25, 216, 70, 245, "AEROGERADOR 01", "2,0 MW | TRG 2,5 MVA*"),
        (77, 216, 122, 245, "AEROGERADOR 02", "2,0 MW | TRG 2,5 MVA*"),
        (129, 216, 174, 245, "AEROGERADOR 03", "2,0 MW | TRG 2,5 MVA*"),
    )
    for x0, y0, x1, y1, title, detail in feeder_a:
        box(layout, x0, y0, x1, y1, title, detail, detail_height=1.05)
    arrow(layout, (70, 230), (77, 230), "05_POTENCIA", 1.25)
    arrow(layout, (122, 230), (129, 230), "05_POTENCIA", 1.25)
    box(layout, 183, 216, 221, 245, "CB-F01", "34,5 kV*", detail_height=1.1)
    arrow(layout, (174, 230), (183, 230), "05_POTENCIA", 1.35)
    arrow(layout, (221, 230), (254, 230), "08_CABOS", 1.6)
    text(layout, "ALIMENTADOR F01 | WTG-01 A WTG-03", 200, 236, 1.1, "08_CABOS", centered=True)

    # Feeder B: two turbines, its breaker and a separate riser to the same bus.
    for x0, x1, title in ((25, 73, "AEROGERADOR 04"), (82, 130, "AEROGERADOR 05")):
        box(layout, x0, 151, x1, 180, title, "2,0 MW | TRG 2,5 MVA*", detail_height=1.02)
    arrow(layout, (73, 165), (82, 165), "08_CABOS", 1.35)
    box(layout, 141, 151, 179, 180, "CB-F02", "34,5 kV*", detail_height=1.1)
    arrow(layout, (130, 165), (141, 165), "08_CABOS", 1.35)
    line(layout, (179, 165), (270, 165), "08_CABOS")
    line(layout, (270, 165), (270, 201), "08_CABOS")
    arrow(layout, (270, 201), (270, 211), "08_CABOS", 1.35)
    text(layout, "ALIMENTADOR F02 | WTG-04 A WTG-05", 210, 171, 1.1, "08_CABOS", centered=True)

    box(layout, 254, 211, 291, 249, "BARRA COLETORA", "34,5 kV*", detail_height=1.2)
    box(layout, 307, 211, 351, 249, "TR-01", "12,5 MVA*\n34,5/69 kV*", detail_height=1.15)
    box(layout, 368, 211, 403, 249, "POI-01", "69 kV*", detail_height=1.15)
    arrow(layout, (291, 230), (307, 230), "05_POTENCIA", 1.45)
    arrow(layout, (351, 230), (368, 230), "05_POTENCIA", 1.45)

    box(layout, 27, 111, 111, 139, "SUPERVISAO PPC/SCADA", "P, Q, V, estados e alarmes", layer="07_INSTRUMENTACAO", detail_height=1.05)
    box(layout, 126, 111, 208, 139, "MEDICAO E PROTECAO", "TC/TP e ajustes a definir", layer="07_INSTRUMENTACAO", detail_height=1.05)
    arrow(layout, (111, 125), (126, 125), "07_INSTRUMENTACAO", 1.3)
    text(layout, "INTERFACE DE COMANDO E TELEMETRIA - ARQUITETURA FUNCIONAL, NAO LOGICA DE PROTECAO", 24, 196, 1.0, "07_INSTRUMENTACAO")
    text(layout, "* Valores de estudo; especificacao do fabricante, capacidade Q/P, curto-circuito e acesso ainda pendentes.", 24, 102, 1.12, "13_NOTAS")


def turbine_symbol(layout, x: float, y: float, tag: str) -> None:
    layout.add_circle((x, y), 4.2, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    line(layout, (x, y - 4.2), (x, y - 13), "04_EQUIPAMENTOS")
    for dx, dy in ((0, 4.0), (-3.5, -2.0), (3.5, -2.0)):
        line(layout, (x, y), (x + dx, y + dy), "04_EQUIPAMENTOS")
    text(layout, tag, x + 7.5, y + 1.0, 1.15, "04_EQUIPAMENTOS", bold=True)


def draw_layout(layout) -> None:
    add_rect(layout, 24, 108, 208, 256, "11_ARQUITETURA")
    text(layout, "POLIGONAL E POSICOES ESQUEMATICAS - SEM ESCALA", 29, 248, 1.5, "11_ARQUITETURA", bold=True)
    # Five illustrative turbine positions; neither spacing nor route length is design data.
    turbine_symbol(layout, 55, 220, "WTG-01")
    turbine_symbol(layout, 116, 231, "WTG-02")
    turbine_symbol(layout, 180, 216, "WTG-03")
    turbine_symbol(layout, 76, 160, "WTG-04")
    turbine_symbol(layout, 128, 151, "WTG-05")
    # Conceptual two-feeder routes; actual cable paths and lengths are not established.
    layout.add_lwpolyline([(55, 205), (63, 194), (112, 194), (116, 216)], dxfattribs={"layer": "05_POTENCIA"})
    layout.add_lwpolyline([(116, 216), (128, 202), (174, 202), (180, 201)], dxfattribs={"layer": "05_POTENCIA"})
    layout.add_lwpolyline([(180, 201), (194, 190), (190, 170), (184, 162)], dxfattribs={"layer": "05_POTENCIA"})
    layout.add_lwpolyline([(76, 145), (90, 134), (117, 134), (128, 136)], dxfattribs={"layer": "08_CABOS"})
    layout.add_lwpolyline([(128, 136), (139, 136), (151, 154), (160, 154)], dxfattribs={"layer": "08_CABOS"})
    text(layout, "F01 | 34,5 kV*", 119, 198, 1.05, "05_POTENCIA", centered=True)
    text(layout, "F02 | 34,5 kV*", 128, 127, 1.05, "08_CABOS", centered=True)

    box(layout, 160, 146, 207, 162, "CSE-01 / BARRA", "34,5 kV*", detail_height=1.05)
    box(layout, 160, 116, 207, 139, "TR-01", "12,5 MVA | 34,5/69 kV*", detail_height=1.0)
    line(layout, (183.5, 146), (183.5, 139), "05_POTENCIA")
    arrow(layout, (207, 127.5), (215, 127.5), "05_POTENCIA", 1.2)

    add_rect(layout, 220, 108, 400, 256, "12_LEGENDA")
    text(layout, "DADOS DA IMPLANTACAO", 225, 247, 1.7, "12_LEGENDA", bold=True)
    line(layout, (224, 240), (396, 240), "12_LEGENDA")
    entries = (
        ("WTG-01...05", "5 x 2,0 MW*"),
        ("COLETA", "34,5 kV*"),
        ("ALIMENTADORES", "F01 (3) | F02 (2)"),
        ("CSE-01", "barra e TR-01"),
        ("POI-01", "69 kV*"),
        ("ROTAS / DISTANCIAS", "nao definidas"),
    )
    for index, (label, value) in enumerate(entries):
        y = 226 - index * 13
        line(layout, (224, y - 4), (396, y - 4), "03_COTAS")
        text(layout, label, 227, y, 1.1, "02_TEXTO", bold=True)
        text(layout, value, 393, y, 1.1, "02_TEXTO", centered=True)
    text(layout, "Vento, relevo, afastamentos, acessos, servidao e restricoes ambientais nao levantados.", 225, 144, 1.05, "13_NOTAS")
    text(layout, "Os simbolos de aerogerador nao indicam modelo, fabricante ou dimensao real.", 225, 133, 1.05, "13_NOTAS")
    text(layout, "A separacao dos alimentadores e as rotas sao apenas uma proposta didatica.", 225, 122, 1.05, "13_NOTAS")


def draw_calculations(layout) -> None:
    add_rect(layout, 22, 169, 208, 257, "12_LEGENDA")
    text(layout, "BASE DE POTENCIA E TRANSFORMACAO", 27, 248, 1.55, "12_LEGENDA", bold=True)
    line(layout, (26, 242), (204, 242), "12_LEGENDA")
    rows = (
        ("Potencia instalada", "5 x 2 MW = 10 MW"),
        ("Unidade @ FP 0,95", "2,105 MVA"),
        ("TRG por unidade", "2,5 MVA*"),
        ("Envelope TRG @ FP 0,95", "2,375 MW"),
        ("Margem aritmetica / WTG", "0,375 MW"),
        ("TR-01 planta", "12,5 MVA*"),
        ("Planta @ FP 0,95", "10,526 MVA"),
        ("Margem TR-01", "1,974 MVA"),
    )
    for index, (label, value) in enumerate(rows):
        y = 233 - index * 8.5
        line(layout, (26, y - 3.5), (204, y - 3.5), "03_COTAS")
        text(layout, label, 29, y, 1.35, "02_TEXTO")
        text(layout, value, 199, y, 1.35, "02_TEXTO", centered=True)

    add_rect(layout, 216, 169, 398, 257, "12_LEGENDA")
    text(layout, "CORRENTES TRIFASICAS ESTIMADAS", 221, 248, 1.55, "12_LEGENDA", bold=True)
    line(layout, (220, 242), (394, 242), "12_LEGENDA")
    text(layout, "P = raiz(3) x V x I x FP", 225, 230, 1.55, "05_POTENCIA", bold=True)
    current_rows = (
        ("WTG, 2 MW / 34,5 kV", "35,24 A"),
        ("Parque, 10 MW / 34,5 kV", "176,20 A"),
        ("Parque, 10 MW / 69 kV", "88,10 A"),
    )
    for index, (label, value) in enumerate(current_rows):
        y = 215 - index * 14
        line(layout, (220, y - 4), (394, y - 4), "03_COTAS")
        text(layout, label, 225, y, 1.35, "02_TEXTO")
        text(layout, value, 390, y, 1.35, "02_TEXTO", centered=True)
    text(layout, "I calculada sem perdas; FP 0,95 e tensoes nominais sao hipoteses.", 225, 171, 1.0, "13_NOTAS")

    add_rect(layout, 22, 104, 208, 163, "07_INSTRUMENTACAO")
    text(layout, "INTERFACES A ESPECIFICAR", 27, 154, 1.55, "07_INSTRUMENTACAO", bold=True)
    interfaces = (
        ("PPC", "limites P/Q e tensao no POI"),
        ("PROTECAO", "funcoes, ajustes e seletividade"),
        ("MEDICAO", "TC/TP, classe e faturamento"),
        ("SCADA", "telecom, protocolos e tempo"),
    )
    for index, (tag, description) in enumerate(interfaces):
        y = 142 - index * 9
        line(layout, (26, y - 3), (204, y - 3), "03_COTAS")
        text(layout, tag, 29, y, 1.15, "07_INSTRUMENTACAO", bold=True)
        text(layout, description, 71, y, 1.15, "02_TEXTO")

    add_rect(layout, 216, 104, 398, 163, "13_NOTAS")
    text(layout, "ESTUDOS E DADOS PENDENTES", 221, 154, 1.55, "13_NOTAS", bold=True)
    pending = (
        "Recurso eolico, curva de potencia e energia anual.",
        "Fluxo de carga, curto-circuito, estabilidade e harmônicos.",
        "Cabos, ampacidade, queda de tensao e perdas da coleta.",
        "Aterramento, SPDA, protecao, telecom e requisitos do ONS/acessante.",
    )
    for index, item in enumerate(pending):
        text(layout, "- " + item, 222, 141 - index * 9, 1.12, "02_TEXTO")


SHEETS = (
    {
        "filename": "01_unifilar_coleta_conexao.dxf",
        "title": "UNIFILAR DA COLETA E CONEXAO DO PARQUE EOLICO",
        "subtitle": "Aerogeradores, alimentadores em 34,5 kV, subestacao e ponto de conexao",
        "scale": "S/ESC.",
        "notes": "Potencias, tensoes e relacoes de transformacao sao hipoteses didaticas.\\P"
                "Protecao, controle de tensao/reativos e requisitos de acesso dependem de estudos e agente de rede.",
        "legend": "WTG: aerogerador | TRG: transformador elevador unitario | CSE: subestacao coletora | POI: ponto de interconexao | PPC: controle da usina",
        "draw": draw_single_line,
    },
    {
        "filename": "02_layout_parque_eolico.dxf",
        "title": "IMPLANTACAO CONCEITUAL DO PARQUE EOLICO",
        "subtitle": "Posicoes relativas, circuitos coletores e subestacao - sem escala",
        "scale": "S/ESC.",
        "notes": "Posicoes, espacamentos, poligonal e rotas nao sao levantamento topografico.\\P"
                "Nao foram avaliados vento, acessos, servidao, geotecnia ou licenciamento.",
        "legend": "WTG: aerogerador de 2 MW assumido | F01/F02: alimentadores coletores | CSE: subestacao coletora | distancias nao indicadas",
        "draw": draw_layout,
    },
    {
        "filename": "03_base_calculo_interfaces.dxf",
        "title": "BASE DE CALCULO E INTERFACES ELETRICAS",
        "subtitle": "Envelope de potencia, correntes trifasicas e dados que exigem estudo",
        "scale": "S/ESC.",
        "notes": "Resultados limitados a aritmetica nominal; nao sao fluxo de carga ou verificacao de capacidade.\\P"
                "Corrente, FP e margem nao substituem dados OEM, curto-circuito, perdas ou estudo de acesso.",
        "legend": "FP: fator de potencia assumido | MVA: potencia aparente | PPC: power plant controller | ONS: Operador Nacional do Sistema",
        "draw": draw_calculations,
    },
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(root, config, index, spec)
        print(f"DXF gerado: {root / SLUG / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
