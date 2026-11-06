"""Gera tres pranchas conceituais de uma microrrede industrial."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment


DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "15-microrrede-industrial-fv-bess-gerador"
ROOT = DEFAULT_ROOT
SCRIPTS_DIR = ROOT / "scripts"
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
WARNING_FALLBACK = (
    "Projeto academico e conceitual. Nao deve ser utilizado para fabricacao, "
    "instalacao ou execucao de servicos sem revisao, dimensionamento e "
    "responsabilidade de profissional legalmente habilitado."
)


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
        detail_height: float = 1.3) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    midx = (x0 + x1) / 2
    midy = (y0 + y1) / 2
    if detail:
        if "\n" in detail:
            text(layout, title, midx, y1 - 5, 1.7, layer, centered=True, bold=True)
            add_mtext(
                layout,
                detail.replace("\n", "\\P"),
                (x0 + 2, y1 - 8),
                x1 - x0 - 4,
                detail_height,
                "02_TEXTO",
            )
        else:
            text(layout, title, midx, midy + 2, 1.7, layer, centered=True, bold=True)
            text(layout, detail, midx, midy - 2, detail_height, "02_TEXTO", centered=True)
    else:
        text(layout, title, midx, midy, 1.7, layer, centered=True, bold=True)


def arrow(layout, start: tuple[float, float], end: tuple[float, float],
          layer: str, size: float = 2.3) -> None:
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
    text(layout, title, 20, 275, 3.2, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.65, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66.5, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.42, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90.5, 2.0, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.38, "12_LEGENDA")

    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, value, x, 89.5, 1.55, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.45, "02_TEXTO", centered=True)


def make_sheet(root: Path, config: dict, number: int, spec: dict, draw) -> None:
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
    draw(layout)
    warning = config["portfolio"].get("warning", WARNING_FALLBACK)
    footer(layout, spec, warning)
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
    # PCC, transformer and primary AC bus.
    boxes = (
        (24, 70, "REDE MT", "13.8 kV*"),
        (82, 132, "PCC-01", "interconexao / QF*"),
        (144, 194, "TR-01", "1.5 MVA*"),
        (206, 270, "QGBT-MG", "380/220 V*"),
    )
    for x0, x1, title, detail in boxes:
        box(layout, x0, 213, x1, 249, title, detail, detail_height=1.2)
    for left, right in zip(boxes, boxes[1:]):
        arrow(layout, (left[1], 231), (right[0], 231), "05_POTENCIA", 1.7)

    # Grid-forming/storage resources and grid-following PV join the common AC bus.
    line(layout, (27, 190), (393, 190), "05_POTENCIA")
    text(layout, "BARRAMENTO CA DA MICRORREDE - PROTECAO E AJUSTES A DEFINIR", 207, 195, 1.35, "05_POTENCIA", centered=True, bold=True)
    arrow(layout, (238, 212), (238, 190), "05_POTENCIA", 1.7)
    sources = (
        ((28, 137, 101, 171), "FV-01", "inversores 600 kW*", 64.5),
        ((123, 137, 207, 171), "BESS-01 / PCS", "500 kW / 1.0 MWh*", 165),
        ((228, 137, 300, 171), "GE-01", "500 kW* / FP 0.80", 264),
    )
    for (x0, y0, x1, y1), title, detail, cx in sources:
        box(layout, x0, y0, x1, y1, title, detail, detail_height=1.15)
        arrow(layout, (cx, y1), (cx, 190), "05_POTENCIA", 1.6)
    box(layout, 322, 213, 398, 249, "CARGA-MG", "1.0 MW* / 800 kW criticos", detail_height=1.15)
    arrow(layout, (360, 190), (360, 212), "05_POTENCIA", 1.6)
    box(layout, 138, 104, 192, 126, "BAT-01", "1.0 MWh nominal*", layer="04_EQUIPAMENTOS", detail_height=1.1)
    arrow(layout, (165, 127), (165, 136), "08_CABOS", 1.4)

    text(layout, "Carga nao critica: 200 kW*; total da instalacao: 1.0 MW*.", 27, 118, 1.28, "13_NOTAS")
    text(layout, "* Valores de potencia, tensao e configuracao sao hipoteses; nao representam especificacao de equipamento.", 27, 110, 1.2, "13_NOTAS")


def draw_layout(layout) -> None:
    """Conceptual industrial site with generation, storage, PCC and loads."""
    add_rect(layout, 24, 108, 296, 257, "11_ARQUITETURA")
    text(layout, "AREA INDUSTRIAL - IMPLANTACAO SEM ESCALA", 29, 249, 1.8, "11_ARQUITETURA", bold=True)

    # PV field symbolized as a repeated panel array; no site geometry is implied.
    text(layout, "CAMPO FV-01", 84, 243, 1.5, "04_EQUIPAMENTOS", centered=True, bold=True)
    for row_y in (219, 230):
        for i in range(4):
            x = 43 + i * 21
            add_rect(layout, x, row_y, x + 16, row_y + 7, "04_EQUIPAMENTOS")
            line(layout, (x + 8, row_y), (x + 8, row_y + 7), "03_COTAS")

    box(layout, 165, 211, 218, 242, "BESS-01", "PCS 500 kW / BAT 1.0 MWh", detail_height=1.2)
    box(layout, 232, 211, 284, 242, "GE-01", "500 kW / fuel pendente", detail_height=1.15)
    # Shared AC corridor shown as an indicative route, then separate load groups.
    line(layout, (40, 192), (279, 192), "10_ELETROCALHAS")
    text(layout, "BARRAMENTO / ROTA PRINCIPAL - POSICAO A CONFIRMAR", 159, 197, 1.15, "10_ELETROCALHAS", centered=True)
    arrow(layout, (84, 211), (84, 192), "05_POTENCIA", 1.5)
    arrow(layout, (191, 210), (191, 192), "05_POTENCIA", 1.5)
    arrow(layout, (258, 210), (258, 192), "05_POTENCIA", 1.5)

    box(layout, 126, 146, 204, 181, "QGBT-MG", "PCC-01 / protecao pendente", detail_height=1.15)
    arrow(layout, (165, 191), (165, 182), "05_POTENCIA", 1.5)
    box(layout, 35, 146, 113, 181, "CARGA-CRIT", "800 kW*", detail_height=1.15)
    box(layout, 217, 146, 285, 181, "CARGA-NCRIT", "200 kW*", detail_height=1.15)
    arrow(layout, (73, 191), (73, 182), "05_POTENCIA", 1.4)
    arrow(layout, (251, 191), (251, 182), "05_POTENCIA", 1.4)
    text(layout, "Separacao de cargas e rotas depende de levantamento e coordenacao de campo.", 29, 119, 1.2, "13_NOTAS")

    add_rect(layout, 304, 108, 400, 257, "12_LEGENDA")
    text(layout, "CADASTRO DE POTENCIAS", 309, 248, 1.8, "12_LEGENDA", bold=True)
    line(layout, (308, 241), (396, 241), "12_LEGENDA")
    entries = (
        ("FV-01", "600 kWac*"),
        ("BESS-01", "500 kW / 1 MWh*"),
        ("GE-01", "500 kW*"),
        ("TR-01", "1,500 kVA*"),
        ("CARGA CRITICA", "800 kW*"),
        ("CARGA NAO CRITICA", "200 kW*"),
    )
    for i, (tag, value) in enumerate(entries):
        y = 226 - i * 17
        text(layout, tag, 310, y, 1.25, "02_TEXTO", bold=True)
        text(layout, value, 390, y, 1.25, "02_TEXTO", centered=True)
    text(layout, "* Dados hipoteticos, sem fichas de fabricante.", 309, 119, 1.12, "13_NOTAS")


def draw_operation_and_balance(layout) -> None:
    """Power balances and microgrid operating modes under stated assumptions."""
    add_rect(layout, 22, 169, 198, 257, "12_LEGENDA")
    text(layout, "CAPACIDADES E ENVELOPE", 27, 248, 1.8, "12_LEGENDA", bold=True)
    line(layout, (26, 242), (194, 242), "12_LEGENDA")
    capacity_rows = (
        ("Carga critica", "800 kW"),
        ("Carga nao critica", "200 kW"),
        ("FV / GE maximos", "600 / 500 kW"),
        ("BESS PCS / energia", "500 kW / 1 MWh"),
        ("TR-01 @ FP 0.95", "1,425 kW"),
        ("Margem TR vs. 1 MW", "425 kW"),
    )
    for i, (label, value) in enumerate(capacity_rows):
        y = 233 - i * 10
        line(layout, (26, y - 4), (194, y - 4), "03_COTAS")
        text(layout, label, 29, y, 1.28, "02_TEXTO")
        text(layout, value, 190, y, 1.28, "02_TEXTO", centered=True)

    add_rect(layout, 204, 169, 398, 257, "12_LEGENDA")
    text(layout, "BALANCO DE POTENCIA POR CENARIO (kW)", 209, 248, 1.75, "12_LEGENDA", bold=True)
    line(layout, (208, 242), (394, 242), "12_LEGENDA")
    headings = ((218, "MODO"), (256, "FV"), (291, "GE"), (326, "BESS"), (358, "REDE"), (389, "CARGA"))
    for x, label in headings:
        text(layout, label, x, 237, 1.1, "12_LEGENDA", centered=True, bold=True)
    scenarios = (
        ("NORMAL", "600", "0", "0", "400", "1000"),
        ("ILHA FV ALTA", "600", "400", "0", "0", "1000"),
        ("ILHA FV BAIXA", "200", "500", "300", "0", "1000"),
        ("ILHA SEM FV", "0", "500", "500", "0", "1000"),
        ("GE INDISP.*", "300", "0", "500", "0", "800**"),
    )
    for i, row in enumerate(scenarios):
        y = 224 - i * 10
        line(layout, (208, y - 4), (394, y - 4), "03_COTAS")
        for (x, _), value in zip(headings, row):
            text(layout, value, x, y, 1.1, "02_TEXTO", centered=True)
    text(layout, "* Caso de falha do gerador. ** Mantem 800 kW criticos e corta 200 kW nao criticos.", 209, 173, 0.98, "13_NOTAS")

    add_rect(layout, 22, 104, 210, 163, "07_INSTRUMENTACAO")
    text(layout, "MODOS E TRANSICOES PROPOSTOS", 27, 154, 1.7, "07_INSTRUMENTACAO", bold=True)
    states = (
        ("CONECTADA", "PCC fechado; FV e BESS sob limite acordado."),
        ("ILHAMENTO", "Abrir PCC; BESS/GE sustentam a barra."),
        ("ILHADA", "Equilibrar FV, GE e BESS; priorizar cargas."),
        ("RESSINCRONIA", "Permissao, sincronismo e fechamento controlado."),
    )
    for i, (state, desc) in enumerate(states):
        y = 143 - i * 11
        line(layout, (26, y - 4), (206, y - 4), "03_COTAS")
        text(layout, state, 29, y, 1.05, "06_COMANDO", bold=True)
        text(layout, desc, 77, y, 0.98, "02_TEXTO")

    add_rect(layout, 216, 104, 398, 163, "13_NOTAS")
    text(layout, "PROTECAO E LIMITES", 221, 154, 1.7, "13_NOTAS", bold=True)
    limits = (
        "Anti-ilhamento, sincronismo, religamento e ajustes nao definidos.",
        "BESS: SOC minimo, reserva, eficiencia e degradacao pendentes.",
        "GE: partida, rampa, fuel, emissao e paralelismo pendentes.",
        "Interconexao depende de concessionaria e estudos especificos.",
    )
    for i, item in enumerate(limits):
        text(layout, "- " + item, 222, 142 - i * 11, 1.05, "02_TEXTO")


SHEETS = (
    {
        "filename": "01_unifilar_microrrede.dxf",
        "title": "DIAGRAMA UNIFILAR DA MICRORREDE",
        "subtitle": "Rede, FV, armazenamento e geracao local em barramento CA comum",
        "scale": "S/ESC.",
        "notes": "13,8 kV, 380/220 V, cargas e capacidades sao hipoteses de representacao.\\P"
                "Protecao de interconexao, curto-circuito e ajustes dependem de estudos e concessionaria.",
        "legend": "PCC: ponto de acoplamento comum | FV: fotovoltaico | BESS: armazenamento | GE: grupo gerador | MG: microrrede | kW/kWh nominais assumidos",
        "draw": draw_single_line,
    },
    {
        "filename": "02_layout_fontes_cargas.dxf",
        "title": "LAYOUT CONCEITUAL DE FONTES E CARGAS",
        "subtitle": "Campo FV, BESS, GE, QGBT e grupos de carga; planta sem escala",
        "scale": "S/ESC.",
        "notes": "A implantacao nao representa levantamento, distancias, rotas ou zonas de seguranca reais.\\P"
                "A posicao de baterias, gerador, transformador e cargas requer coordenacao de campo.",
        "legend": "FV-01: campo fotovoltaico | BESS-01: conversor e bateria | GE-01: gerador | CARGA-CRIT: cargas prioritarias | CARGA-NCRIT: cargas com corte proposto",
        "draw": draw_layout,
    },
    {
        "filename": "03_operacao_balanco_energia.dxf",
        "title": "BALANCO DE ENERGIA E MODOS DE OPERACAO",
        "subtitle": "Cenarios aritmeticos, transicoes de modo e prioridades de carga propostas",
        "scale": "S/ESC.",
        "notes": "Potencias FV, GE, BESS e cargas sao nominais hipoteticas; balancos nao sao simulacao dinamica.\\P"
                "Autonomia de 2 h e apenas divisao ideal de energia por potencia, sem margem ou perdas.",
        "legend": "PCC: interligacao | SOC: estado de carga | ilha: operacao eletricamente isolada | balancos nao definem protecoes nem limites de exportacao",
        "draw": draw_operation_and_balance,
    },
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    warning = config["portfolio"]["warning"]
    if warning != WARNING_FALLBACK:
        # A configuracao central e a fonte do aviso obrigatorio.
        pass
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(root, config, index, spec, spec["draw"])
        print(f"DXF gerado: {root / SLUG / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
