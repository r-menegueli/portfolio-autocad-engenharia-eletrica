"""Gera tres pranchas conceituais de alimentacao ferroviaria em 750 Vcc."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "20-tracao-ferroviaria-cc-750v"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gerar_template_a3 import (  # noqa: E402
    TITLE_BLOCK_NAME,
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
BOX_BLOCK = "P20_CAIXA_EQUIPAMENTO"
BOX_WIDTH = 57.0
BOX_HEIGHT = 37.0


def text(layout, value: str, x: float, y: float, h: float = 1.35,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(layout, value, (x, y), h, layer=layer,
             align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
             style=TITLE_STYLE if bold else TEXT_STYLE)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def rect(layout, x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)


def arrow(layout, a: tuple[float, float], b: tuple[float, float], layer: str,
          size: float = 1.6) -> None:
    line(layout, a, b, layer)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout, (b[0] - ux * size + side * px * size * 0.55,
                      b[1] - uy * size + side * py * size * 0.55), b, layer)


def equipment(layout, x: float, y: float, tag: str, title: str, detail: str,
              *, layer: str = "04_EQUIPAMENTOS") -> None:
    insert = layout.add_blockref(BOX_BLOCK, (x, y), dxfattribs={"layer": layer})
    insert.add_auto_attribs({"TAG": tag, "TITULO": title, "DADOS": detail})


def box(layout, x0: float, y0: float, x1: float, y1: float, title: str,
        detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.3, detail_height: float = 1.0) -> None:
    rect(layout, x0, y0, x1, y1, layer)
    text(layout, title, (x0 + x1) / 2, (y0 + y1) / 2 + (1.5 if detail else 0),
         title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, (x0 + x1) / 2, (y0 + y1) / 2 - 2,
             detail_height, "02_TEXTO", centered=True)


def make_component_block(doc) -> None:
    if BOX_BLOCK in doc.blocks:
        return
    block = doc.blocks.new(name=BOX_BLOCK)
    block.add_lwpolyline([(0, 0), (BOX_WIDTH, 0), (BOX_WIDTH, BOX_HEIGHT), (0, BOX_HEIGHT)],
                         close=True, dxfattribs={"layer": "0"})
    block.add_line((0, 27), (BOX_WIDTH, 27), dxfattribs={"layer": "0"})
    for tag, point, height in (("TAG", (2.0, 31.5), 1.12),
                               ("TITULO", (2.0, 18.3), 1.3),
                               ("DADOS", (2.0, 7.2), 1.0)):
        block.add_attdef(tag, insert=point, text="",
                         dxfattribs={"height": height, "style": TEXT_STYLE, "layer": "0"})


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 2.65, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.45, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 1.8, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.45, "13_NOTAS")
    rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66, 1.65, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.2, "13_NOTAS")
    rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90, 1.65, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.17, "12_LEGENDA")
    rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for label, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, label, x, 89.5, 1.25, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.2, "02_TEXTO", centered=True)


def draw_single_line(layout) -> None:
    text(layout, "TRACAO FERROVIARIA CC | 750 Vcc* | Pdc=1,0 MW* | PCC 13,8 kV AC*", 24, 252, 1.42, "05_POTENCIA", bold=True)
    top_x = (20, 83, 146, 209, 272)
    top_units = (
        ("PCC-01", "REDE AC", "13,8 kV | 60 Hz*"),
        ("QMT-01", "ENTRADA MT", "protecao a definir"),
        ("TR-TR-01", "TRAFO TRACAO", "dados de placa pendentes"),
        ("R-01", "RETIFICADOR", "diodos | fluxo unidirecional"),
        ("QDC-01", "QUADRO CC", "750 Vcc* | CB-DC"),
    )
    for x, values in zip(top_x, top_units):
        equipment(layout, x, 210, *values)
    for left, right in zip(top_x, top_x[1:]):
        arrow(layout, (left + BOX_WIDTH, 228.5), (right, 228.5), "05_POTENCIA", 1.2)

    bottom_x = (83, 146, 209, 272, 335)
    bottom_units = (
        ("NB-01", "BARRA NEGATIVA", "retorno de corrente"),
        ("TRK-RET", "TRILHO DE ROLAMENTO", "retorno CC*"),
        ("VEH-01", "VEICULO", "carga de tracao"),
        ("TRK-01", "TERCEIRO TRILHO", "alimentacao positiva"),
        ("FDR-01/PB+", "ALIMENTADOR +", "CB e isolacao a definir"),
    )
    for x, values in zip(bottom_x, bottom_units):
        equipment(layout, x, 150, *values, layer="04_EQUIPAMENTOS")
    # Corrente convencional: barra positiva -> trilho de contato -> veículo -> retorno.
    for left, right in zip(bottom_x[::-1], bottom_x[-2::-1]):
        arrow(layout, (left, 168.5), (right + BOX_WIDTH, 168.5), "05_POTENCIA", 1.15)
    # Ligação de saída positiva e retorno negativo ao retificador.
    line(layout, (300.5, 210), (300.5, 194), "05_POTENCIA")
    line(layout, (300.5, 194), (363.5, 194), "05_POTENCIA")
    arrow(layout, (363.5, 194), (363.5, 187), "05_POTENCIA", 1.0)
    line(layout, (111.5, 150), (111.5, 137), "05_POTENCIA")
    line(layout, (111.5, 137), (143, 137), "05_POTENCIA")
    line(layout, (143, 137), (143, 194), "05_POTENCIA")
    line(layout, (143, 194), (237.5, 194), "05_POTENCIA")
    arrow(layout, (237.5, 194), (237.5, 210), "05_POTENCIA", 1.0)
    line(layout, (224, 150), (224, 136), "08_CABOS")
    line(layout, (252, 150), (252, 136), "08_CABOS")
    text(layout, "Idc = Pdc/Vdc = 1333 A para 1,0 MW e 750 Vcc ideais; nao inclui ondulacao, perdas ou regime de pico.", 23, 122, 1.0, "13_NOTAS")
    text(layout, "Retorno pelos trilhos e terra sao funcoes distintas; ligacoes, potenciais e correntes vagantes exigem estudo especifico.", 23, 112, 1.0, "13_NOTAS")


def draw_network(layout) -> None:
    text(layout, "ZONAS DE ALIMENTACAO E CAMINHO CONCEITUAL DA CORRENTE", 24, 251, 1.35, "05_POTENCIA", bold=True)
    box(layout, 22, 211, 95, 245, "SE-TR-01", "13,8 kV AC / 750 Vcc*", layer="04_EQUIPAMENTOS")
    box(layout, 325, 211, 398, 245, "SE-TR-02", "13,8 kV AC / 750 Vcc*", layer="04_EQUIPAMENTOS")

    # Terceiro trilho dividido em zonas; o arranjo real de secionamento nao e definido.
    line(layout, (46, 190), (188, 190), "05_POTENCIA")
    line(layout, (232, 190), (374, 190), "05_POTENCIA")
    text(layout, "ZONA A | TERCEIRO TRILHO +", 59, 198, 1.05, "05_POTENCIA")
    text(layout, "ZONA B | TERCEIRO TRILHO +", 245, 198, 1.05, "05_POTENCIA")
    arrow(layout, (64, 190), (115, 190), "05_POTENCIA", 1.1)
    arrow(layout, (355, 190), (304, 190), "05_POTENCIA", 1.1)
    # Alimentadores conceituais de cada subestacao para sua zona.
    line(layout, (58.5, 211), (58.5, 190), "05_POTENCIA")
    arrow(layout, (361.5, 211), (361.5, 190), "05_POTENCIA", 1.1)

    # Isolacao de zona ilustrativa, sem especificar manobra ou intertravamento.
    rect(layout, 187, 184, 193, 196, "04_EQUIPAMENTOS")
    rect(layout, 227, 184, 233, 196, "04_EQUIPAMENTOS")
    text(layout, "PONTO DE SEPARACAO / SECCIONAMENTO A ESTUDAR", 128, 178, 0.95, "13_NOTAS")

    # Veiculo e trilhos de retorno, representados sem dimensao ou escala.
    box(layout, 139, 149, 281, 170, "VEH-01 | SAPATAS DE CAPTACAO", "posicao ilustrativa; sem geometria veicular", layer="04_EQUIPAMENTOS", title_height=1.12, detail_height=0.9)
    line(layout, (38, 131), (382, 131), "08_CABOS")
    line(layout, (38, 136), (382, 136), "08_CABOS")
    text(layout, "TRILHOS DE ROLAMENTO — CAMINHO DE RETORNO CC*", 121, 119, 1.0, "08_CABOS", centered=True)
    arrow(layout, (303, 131), (250, 131), "08_CABOS", 1.0)
    arrow(layout, (117, 131), (64, 131), "08_CABOS", 1.0)

    box(layout, 22, 150, 95, 175, "NB-01", "retorno da SE-TR-01", layer="07_INSTRUMENTACAO", title_height=1.1, detail_height=0.9)
    box(layout, 325, 150, 398, 175, "NB-02", "retorno da SE-TR-02", layer="07_INSTRUMENTACAO", title_height=1.1, detail_height=0.9)
    line(layout, (58.5, 150), (58.5, 136), "08_CABOS")
    line(layout, (361.5, 150), (361.5, 136), "08_CABOS")
    text(layout, "Esquema qualitativo: zonas, cruzamentos, seccionamento, retorno e operacao paralela precisam de estudo de alimentacao e protecao.", 24, 108, 1.0, "13_NOTAS")


def draw_protection(layout) -> None:
    text(layout, "PROTECAO, MEDICAO E INTERFACES — FUNCOES PROPOSTAS, SEM AJUSTES", 24, 251, 1.32, "13_NOTAS", bold=True)
    box(layout, 23, 209, 102, 240, "TC-DC / TV-DC", "medicao isolada", layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=0.92)
    box(layout, 132, 209, 211, 240, "PR-DC-01", "protecao e controle", layer="06_COMANDO", title_height=1.15, detail_height=0.92)
    box(layout, 218, 209, 297, 240, "CB-DC-01", "disjuntor de alimentador", layer="04_EQUIPAMENTOS", title_height=1.1, detail_height=0.92)
    box(layout, 304, 209, 397, 240, "SCADA-TR", "supervisao operacional", layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=0.92)
    arrow(layout, (102, 224.5), (132, 224.5), "07_INSTRUMENTACAO", 1.2)
    arrow(layout, (211, 224.5), (218, 224.5), "06_COMANDO", 1.0)
    arrow(layout, (297, 224.5), (304, 224.5), "07_INSTRUMENTACAO", 1.0)

    x0, x1 = 22.0, 398.0
    columns = ((x0, 105, "EVENTO / GRANDEZA"), (105, 210, "FUNCAO A ESTUDAR"), (210, 330, "EVIDENCIA NECESSARIA"), (330, x1, "ESTADO"))
    top, head_bottom, row_h = 193.0, 183.0, 10.0
    for left, right, label in columns:
        rect(layout, left, head_bottom, right, top, "12_LEGENDA")
        text(layout, label, (left + right) / 2, 188, 1.0, "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("Curto no alimentador CC", "protecao e abertura do CB-DC", "curvas, capacidade e seletividade", "A VALIDAR"),
        ("Sobrecorrente / sobrecarga", "deteccao seletiva", "perfil de carga e coordenacao", "A VALIDAR"),
        ("Conversor / diodos", "supervisao de falha e temperatura", "dados e limites do fabricante", "A VALIDAR"),
        ("Tensao trilho/retorno", "avaliar risco eletrico e tensao de toque", "IEC 62128-1 e estudos do local", "A VALIDAR"),
        ("Correntes vagantes", "controle de corrosao e retorno", "IEC 62128-2 e levantamento", "A VALIDAR"),
    )
    for index, values in enumerate(rows):
        y_top = head_bottom - index * row_h
        y_bottom = y_top - row_h
        for (left, right, _), value in zip(columns, values):
            rect(layout, left, y_bottom, right, y_top, "02_TEXTO")
            text(layout, value, left + 2, (y_top + y_bottom) / 2, 1.0, "02_TEXTO")

    box(layout, 22, 105, 202, 128, "NAO DEFINIDO", "curto-circuito, ajustes, tensoes de toque, limites de corrente vagante, redundancia e modos de operacao", layer="13_NOTAS", title_height=1.1, detail_height=0.92)
    box(layout, 211, 105, 398, 128, "NAO EXECUTADO", "estudos eletricos, simulacao de tracao, coordenacao, validacao de retorno e testes de protecao", layer="13_NOTAS", title_height=1.1, detail_height=0.92)


SHEETS = (
    {
        "filename": "01_unifilar_subestacao_tracao.dxf",
        "title": "SUBESTACAO DE TRACAO FERROVIARIA EM CORRENTE CONTINUA",
        "subtitle": "Rede de MT, transformador/retificador, quadro CC e caminho de retorno pelos trilhos",
        "scale": "S/ESC.",
        "notes": "Caso didatico: rede 13,8 kV AC, barramento de tracao 750 Vcc e demanda 1,0 MW.\\P"
                "Topologia, dados de placa, protecao, retorno e arranjo de contato nao dimensionados.",
        "legend": "MT: media tensao | CC: corrente continua | CB: disjuntor | TRK: trilho | NB: barra negativa | Pdc: potencia CC assumida",
        "draw": draw_single_line,
    },
    {
        "filename": "02_zonas_alimentacao_retorno_tracao.dxf",
        "title": "ZONAS DE ALIMENTACAO E RETORNO DE CORRENTE",
        "subtitle": "Duas fontes conceituais, terceiro trilho, separacao de zonas e trilhos de retorno",
        "scale": "S/ESC.",
        "notes": "Esquema sem escala; zonas e alimentadores servem apenas para explicar interfaces.\\P"
                "Nao comprova tensoes, correntes, retorno, protecao, secionamento ou paralelismo.",
        "legend": "SE-TR: subestacao de tracao | zona A/B: setores didaticos | NB: barra negativa | linhas: trajetos qualitativos",
        "draw": draw_network,
    },
    {
        "filename": "03_matriz_protecao_supervisao_tracao_cc.dxf",
        "title": "FUNCOES DE PROTECAO E SUPERVISAO DA REDE DE TRACAO CC",
        "subtitle": "Matriz de estudos requeridos para alimentadores, conversor, retorno e correntes vagantes",
        "scale": "S/ESC.",
        "notes": "Funcoes listadas nao constituem ajustes, seletividade ou configuracao executavel.\\P"
                "Toda verificacao esta pendente; nenhum estudo ou ensaio de sistema foi realizado.",
        "legend": "TC-DC/TV-DC: medicao isolada | PR-DC: protecao | SCADA: supervisao | A VALIDAR: sem evidencia de campo",
        "draw": draw_protection,
    },
)


def make_sheet(root: Path, config: dict, number: int, spec: dict) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    make_component_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    spec["draw"](layout)
    footer(layout, spec, config["portfolio"]["warning"])
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs({
        "TITULO": spec["title"], "AUTOR": config["portfolio"]["author"],
        "DATA": DATE, "REVISAO": REVISION, "PRANCHA": f"{number:02d}/03",
        "ARQUIVO": spec["filename"], "UNIDADES": "mm", "ESCALA": spec["scale"],
        "FOLHA": "A3", "STATUS": "CONCEIT.",
    })
    output = root / SLUG / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


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
