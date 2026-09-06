"""Gera as oito pranchas DXF do Projeto 02 de forma deterministica."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gerar_template_a3 import (  # noqa: E402
    TITLE_BLOCK_NAME,
    TITLE_STYLE,
    add_frame,
    add_line,
    add_mtext,
    add_rect,
    add_text,
    configure_document,
    define_symbols,
    define_title_block,
    prepare_deterministic_write,
)
from portfolio_config import SheetGeometry, load_config  # noqa: E402


PROJECT_SLUG = "02-projeto-eletrico-residencial"
PROJECT_DATE = "2026-09-05"
REVISION = "00"


@dataclass(frozen=True)
class SheetSpec:
    number: int
    filename: str
    title: str
    subtitle: str
    notes: str
    legend: str
    scale: str = "S/ESC."


@dataclass(frozen=True)
class Circuit:
    tag: str
    description: str
    voltage: int
    phases: str
    va: float
    current: float
    conductor: float
    breaker: int
    poles: int
    curve: str
    drop: float


CIRCUITS = (
    Circuit("C1", "Ilum. sala/quartos/circ.", 127, "A", 75.000, 0.591, 1.5, 10, 1, "B", 0.391),
    Circuit("C2", "Ilum. coz./banh./lav.", 127, "B", 73.913, 0.582, 1.5, 10, 1, "B", 0.330),
    Circuit("C3", "TUG sala/quartos/circ.", 127, "A", 1500.000, 11.811, 4.0, 16, 1, "C", 2.093),
    Circuit("C4", "TUG cozinha", 127, "B", 2100.000, 16.535, 4.0, 20, 1, "C", 2.637),
    Circuit("C5", "TUG banheiro/lav.", 127, "A", 1800.000, 14.173, 4.0, 16, 1, "C", 2.511),
    Circuit("C6", "TUE forno", 220, "AB", 3000.000, 13.636, 4.0, 20, 2, "C", 1.255),
    Circuit("C7", "TUE chuveiro", 220, "AB", 5500.000, 25.000, 6.0, 32, 2, "C", 1.705),
    Circuit("C8", "TUE lavadora", 127, "B", 1500.000, 11.811, 4.0, 16, 1, "C", 2.302),
)


SHEETS = (
    SheetSpec(
        1,
        "01_planta_arquitetonica.dxf",
        "PLANTA ARQUITETÔNICA",
        "Residência térrea fictícia de 75,00 m²",
        "Arquitetura original criada para o portfólio. Dimensões e vãos são premissas.\\P"
        "Não usar como projeto arquitetônico, estrutural ou cadastral.",
        "Linha cinza: arquitetura | Ciano: cotas | Arco: sentido de abertura",
        "1:50",
    ),
    SheetSpec(
        2,
        "02_planta_iluminacao.dxf",
        "PLANTA DE ILUMINAÇÃO",
        "Pontos de luz, interruptores e comandos C1/C2",
        "Potências LED e fator de potência 0,92 são premissas acadêmicas.\\P"
        "Confirmar iluminância, ofuscamento e fotometria em estudo específico.",
        "X em círculo: luminária | S: interruptor | Tracejado verde: comando",
        "1:50",
    ),
    SheetSpec(
        3,
        "03_planta_tomadas.dxf",
        "PLANTA DE TOMADAS",
        "TUG, TUE e identificação dos circuitos C3 a C8",
        "Tomadas 2P+T com alturas indicativas. Potências atribuídas constam na memória.\\P"
        "Confirmar zonas do banheiro, posições de equipamentos e padrão final.",
        "TUG: círculo com traços | TUE: quadrado T | QD: quadro de distribuição",
        "1:50",
    ),
    SheetSpec(
        4,
        "04_planta_eletrodutos.dxf",
        "PLANTA DE ELETRODUTOS",
        "Rotas conceituais, caixas e diâmetros assumidos",
        "Rotas não representam levantamento de obra. Verificar ocupação, curvas,\\P"
        "agrupamento, segregação, acessibilidade e comprimentos reais.",
        "Tracejado cinza: eletroduto | Caixa: derivação | DN: diâmetro nominal",
        "1:50",
    ),
    SheetSpec(
        5,
        "05_diagrama_unifilar.dxf",
        "DIAGRAMA UNIFILAR",
        "Entrada 127/220 V, QG1, DPS1, DR1 e circuitos finais",
        "Capacidade de interrupção, curto-circuito e coordenação de DPS não calculados.\\P"
        "Neutro e PE permanecem separados a jusante no esquema TN-S conceitual.",
        "QG/DJ: disjuntor | DPS: surto | DR: diferencial | N/PE: barramentos",
    ),
    SheetSpec(
        6,
        "06_quadro_distribuicao.dxf",
        "QUADRO DE DISTRIBUIÇÃO",
        "Arranjo frontal conceitual de QD1 com 24 módulos",
        "Dimensões, bornes e arranjo dependem do fabricante. Manter reserva técnica,\\P"
        "separação N/PE, identificação e acesso seguro para manutenção.",
        "Módulo: 18 mm conceitual | N: barra neutra | PE: barra de proteção",
    ),
    SheetSpec(
        7,
        "07_quadro_cargas.dxf",
        "QUADRO DE CARGAS",
        "Potências, correntes, condutores, proteção e queda de tensão",
        "Demanda adotada é didática, não regra de concessionária. As seções de C3\\P"
        "e C8 foram ajustadas para 4 mm²; quedas combinadas abaixo de 4%.",
        "VA: potência aparente | Ib: corrente | S: seção Cu | DJ: disjuntor",
    ),
    SheetSpec(
        8,
        "08_detalhes_aterramento.dxf",
        "DETALHES DE ATERRAMENTO",
        "TN-S, equipotencialização e eletrodo indicativo",
        "A haste de 2,40 m é detalhe didático. Quantidade, arranjo e desempenho dependem\\P"
        "de solo, corrosão, conexões, ensaio e projeto específico.",
        "BEP: equipotencialização | PE: proteção | N: neutro | símbolo: terra",
    ),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered(layout, value: str, point: tuple[float, float], height: float, layer: str = "02_TEXTO") -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def boxed_label(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    detail: str,
    *,
    layer: str = "04_EQUIPAMENTOS",
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2.0, y1 - 4.2), 2.1, layer)
    centered(layout, detail, ((x0 + x1) / 2.0, y0 + 3.7), 1.35, "02_TEXTO")


def draw_table(
    layout,
    x0: float,
    y_top: float,
    widths: tuple[float, ...],
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
    *,
    row_h: float = 8.0,
    text_h: float = 1.45,
) -> None:
    total_w = sum(widths)
    y_bottom = y_top - row_h * (len(rows) + 1)
    add_rect(layout, x0, y_bottom, x0 + total_w, y_top, "12_LEGENDA")
    for index in range(1, len(rows) + 1):
        y = y_top - row_h * index
        line(layout, (x0, y), (x0 + total_w, y), "12_LEGENDA")
    cursor = x0
    for width in widths[:-1]:
        cursor += width
        line(layout, (cursor, y_bottom), (cursor, y_top), "12_LEGENDA")
    values = (headers,) + rows
    for row_index, row in enumerate(values):
        cursor = x0
        y = y_top - row_h * row_index - row_h / 2.0
        for value, width in zip(row, widths):
            centered(layout, value, (cursor + width / 2.0, y), text_h, "12_LEGENDA")
            cursor += width


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    if "P02_LUMINARIA" not in doc.blocks:
        block = doc.blocks.new("P02_LUMINARIA", base_point=(0.0, 0.0))
        block.add_circle((0.0, 0.0), 3.2, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        line(block, (-2.2, -2.2), (2.2, 2.2), "04_EQUIPAMENTOS")
        line(block, (-2.2, 2.2), (2.2, -2.2), "04_EQUIPAMENTOS")

    if "P02_INTERRUPT" not in doc.blocks:
        block = doc.blocks.new("P02_INTERRUPT", base_point=(0.0, 0.0))
        block.add_circle((0.0, 0.0), 2.3, dxfattribs={"layer": "06_COMANDO"})
        centered(block, "S", (0.0, 0.0), 1.8, "06_COMANDO")

    if "P02_TUG" not in doc.blocks:
        block = doc.blocks.new("P02_TUG", base_point=(0.0, 0.0))
        block.add_circle((0.0, 0.0), 2.5, dxfattribs={"layer": "05_POTENCIA"})
        line(block, (-1.1, 0.8), (-1.1, 2.5), "05_POTENCIA")
        line(block, (1.1, 0.8), (1.1, 2.5), "05_POTENCIA")

    if "P02_TUE" not in doc.blocks:
        block = doc.blocks.new("P02_TUE", base_point=(0.0, 0.0))
        add_rect(block, -2.7, -2.7, 2.7, 2.7, "05_POTENCIA")
        centered(block, "T", (0.0, 0.0), 2.1, "05_POTENCIA")

    if "P02_CAIXA" not in doc.blocks:
        block = doc.blocks.new("P02_CAIXA", base_point=(0.0, 0.0))
        add_rect(block, -2.0, -2.0, 2.0, 2.0, "10_ELETROCALHAS")
        line(block, (-2.0, -2.0), (2.0, 2.0), "10_ELETROCALHAS")
        line(block, (-2.0, 2.0), (2.0, -2.0), "10_ELETROCALHAS")

    if "P02_QD" not in doc.blocks:
        block = doc.blocks.new("P02_QD", base_point=(0.0, 0.0))
        add_rect(block, -4.0, -6.0, 4.0, 6.0, "04_EQUIPAMENTOS")
        centered(block, "QD", (0.0, 0.0), 1.8, "04_EQUIPAMENTOS")


def add_revision_table(layout) -> None:
    add_rect(layout, 230.0, 72.0, 410.0, 94.0, "01_CARIMBO")
    line(layout, (230.0, 86.0), (410.0, 86.0), "01_CARIMBO")
    for x in (248.0, 280.0, 352.0):
        line(layout, (x, 72.0), (x, 94.0), "01_CARIMBO")
    for value, x in (("REV.", 239.0), ("DATA", 264.0), ("DESCRIÇÃO", 316.0), ("RESP.", 381.0)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239.0), (PROJECT_DATE, 264.0), ("EMISSÃO INICIAL DO PROJETO 02", 316.0), ("R.E.M.M.", 381.0)):
        centered(layout, value, (x, 78.5), 1.7, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18.0, 18.0, 224.0, 46.0, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATÓRIO", (22.0, 42.0), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22.0, 37.0), 198.0, 1.55, "13_NOTAS")
    add_rect(layout, 18.0, 50.0, 224.0, 70.0, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22.0, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22.0, 62.0), 198.0, 1.55, "13_NOTAS")
    add_rect(layout, 18.0, 74.0, 224.0, 94.0, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22.0, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22.0, 86.0), 198.0, 1.55, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/08",
        "ARQUIVO": spec.filename,
        "UNIDADES": "mm",
        "ESCALA": spec.scale,
        "FOLHA": "A3",
        "STATUS": "CONCEIT.",
    }
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230.0, 10.0), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(values)


def create_sheet(config: dict, spec: SheetSpec):
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = PROJECT_SLUG
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/08"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    msp = doc.modelspace()
    add_frame(msp, geometry)
    centered(msp, spec.title, (210.0, 277.0), 4.2)
    centered(msp, spec.subtitle, (210.0, 270.8), 2.1)
    add_bottom_information(msp, spec, config["portfolio"]["warning"])
    add_revision_table(msp)
    add_title_block(msp, spec, config)
    return doc, msp


def door(layout, hinge: tuple[float, float], radius: float, start: float, end: float) -> None:
    x, y = hinge
    import math

    end_point = (x + radius * math.cos(math.radians(end)), y + radius * math.sin(math.radians(end)))
    line(layout, hinge, end_point, "11_ARQUITETURA")
    layout.add_arc(hinge, radius, start, end, dxfattribs={"layer": "11_ARQUITETURA"})


def window(layout, a: tuple[float, float], b: tuple[float, float]) -> None:
    line(layout, a, b, "03_COTAS")
    if a[1] == b[1]:
        line(layout, (a[0], a[1] + 1.2), (b[0], b[1] + 1.2), "03_COTAS")
    else:
        line(layout, (a[0] + 1.2, a[1]), (b[0] + 1.2, b[1]), "03_COTAS")


def draw_floorplan(layout, *, dimensions: bool = False, room_details: bool = False) -> None:
    add_rect(layout, 35.0, 105.0, 235.0, 255.0, "11_ARQUITETURA")
    add_rect(layout, 37.0, 107.0, 233.0, 253.0, "11_ARQUITETURA")
    line(layout, (115.0, 105.0), (115.0, 255.0), "11_ARQUITETURA")
    line(layout, (117.0, 107.0), (117.0, 253.0), "11_ARQUITETURA")
    line(layout, (35.0, 185.0), (115.0, 185.0), "11_ARQUITETURA")
    line(layout, (37.0, 187.0), (115.0, 187.0), "11_ARQUITETURA")
    line(layout, (115.0, 165.0), (235.0, 165.0), "11_ARQUITETURA")
    line(layout, (117.0, 167.0), (233.0, 167.0), "11_ARQUITETURA")
    line(layout, (115.0, 185.0), (235.0, 185.0), "11_ARQUITETURA")
    line(layout, (117.0, 187.0), (233.0, 187.0), "11_ARQUITETURA")
    line(layout, (185.0, 105.0), (185.0, 165.0), "11_ARQUITETURA")
    line(layout, (187.0, 107.0), (187.0, 165.0), "11_ARQUITETURA")
    line(layout, (155.0, 185.0), (155.0, 255.0), "11_ARQUITETURA")
    line(layout, (157.0, 187.0), (157.0, 253.0), "11_ARQUITETURA")
    line(layout, (115.0, 231.0), (155.0, 231.0), "11_ARQUITETURA")

    door(layout, (82.0, 105.0), 14.0, 0.0, 90.0)
    door(layout, (101.0, 185.0), 12.0, 90.0, 180.0)
    door(layout, (115.0, 151.0), 12.0, -90.0, 0.0)
    door(layout, (143.0, 165.0), 12.0, 0.0, 90.0)
    door(layout, (203.0, 165.0), 12.0, 0.0, 90.0)
    door(layout, (143.0, 185.0), 12.0, 90.0, 180.0)
    door(layout, (157.0, 200.0), 12.0, 0.0, 90.0)
    door(layout, (133.0, 231.0), 10.0, 0.0, 90.0)

    window(layout, (48.0, 105.0), (70.0, 105.0))
    window(layout, (48.0, 255.0), (72.0, 255.0))
    window(layout, (186.0, 255.0), (214.0, 255.0))
    window(layout, (235.0, 122.0), (235.0, 145.0))
    window(layout, (235.0, 208.0), (235.0, 230.0))
    window(layout, (124.0, 255.0), (143.0, 255.0))

    if room_details:
        room_labels = (
            ("SALA / JANTAR", (76.0, 145.0), "4,00 x 4,00 m"),
            ("QUARTO 1", (76.0, 220.0), "4,00 x 3,50 m"),
            ("COZINHA", (151.0, 133.0), "3,50 x 3,00 m"),
            ("LAVANDERIA", (210.0, 133.0), "2,50 x 3,00 m"),
            ("CIRCULAÇÃO", (176.0, 176.0), "6,00 x 1,00 m"),
            ("BANHEIRO", (135.0, 208.0), "2,00 x 2,30 m"),
            ("HALL", (135.0, 243.0), "2,00 x 1,20 m"),
            ("QUARTO 2", (196.0, 220.0), "4,00 x 3,50 m"),
        )
        for name, point, size in room_labels:
            centered(layout, name, (point[0], point[1] + 2.6), 1.9, "02_TEXTO")
            centered(layout, size, (point[0], point[1] - 1.2), 1.35, "02_TEXTO")
    else:
        for name, point in (
            ("SALA / JANTAR", (70.0, 135.0)), ("QUARTO 1", (70.0, 210.0)),
            ("COZINHA", (145.0, 122.0)), ("LAVANDERIA", (207.0, 122.0)),
            ("CIRCULAÇÃO", (197.0, 171.0)), ("BANHEIRO", (128.0, 193.0)),
            ("HALL", (127.0, 242.0)), ("QUARTO 2", (195.0, 210.0)),
        ):
            centered(layout, name, point, 1.45, "02_TEXTO")

    if dimensions:
        line(layout, (35.0, 100.5), (235.0, 100.5), "03_COTAS")
        line(layout, (35.0, 98.8), (35.0, 103.0), "03_COTAS")
        line(layout, (235.0, 98.8), (235.0, 103.0), "03_COTAS")
        centered(layout, "10,00 m", (135.0, 101.5), 1.6, "03_COTAS")
        line(layout, (29.5, 105.0), (29.5, 255.0), "03_COTAS")
        line(layout, (27.8, 105.0), (32.0, 105.0), "03_COTAS")
        line(layout, (27.8, 255.0), (32.0, 255.0), "03_COTAS")
        add_text(layout, "7,50 m", (28.2, 180.0), 1.6, layer="03_COTAS", align=TextEntityAlignment.MIDDLE_CENTER, rotation=90.0)


def draw_architecture(layout) -> None:
    draw_floorplan(layout, dimensions=True, room_details=True)
    centered(layout, "PLANTA-BASE ORIGINAL - ÁREA 75,00 m²", (135.0, 262.0), 1.8, "02_TEXTO")
    add_rect(layout, 248.0, 105.0, 402.0, 260.0, "12_LEGENDA")
    centered(layout, "QUADRO DE AMBIENTES", (325.0, 253.0), 2.4, "12_LEGENDA")
    draw_table(
        layout,
        254.0,
        244.0,
        (70.0, 25.0, 53.0),
        ("AMBIENTE", "ÁREA", "USO"),
        (
            ("Sala / jantar", "16,00", "social"),
            ("Quarto 1", "14,00", "privativo"),
            ("Quarto 2", "14,00", "privativo"),
            ("Cozinha", "10,50", "serviço"),
            ("Lavanderia", "7,50", "serviço"),
            ("Banheiro", "4,60", "molhado"),
            ("Circulação/hall", "8,40", "circulação"),
            ("TOTAL", "75,00", "m²"),
        ),
        row_h=10.0,
        text_h=1.55,
    )
    add_text(layout, "PREMISSAS", (254.0, 145.0), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(
        layout,
        "- Paredes representadas de modo esquemático.\\P- Vãos e mobiliário não foram levantados.\\P"
        "- Escala gráfica 1:50 na folha A3.\\P- Cotas escritas prevalecem sobre medição.",
        (254.0, 139.0),
        140.0,
        1.65,
        "13_NOTAS",
    )


def command_line(layout, points: list[tuple[float, float]]) -> None:
    layout.add_lwpolyline(points, dxfattribs={"layer": "06_COMANDO", "linetype": "DASHED"})


def draw_lighting(layout) -> None:
    draw_floorplan(layout)
    lights = (
        ((63.0, 145.0), "C1", "15 W"), ((91.0, 145.0), "C1", "15 W"),
        ((76.0, 220.0), "C1", "15 W"), ((196.0, 220.0), "C1", "15 W"),
        ((176.0, 176.0), "C1", "9 W"), ((140.0, 133.0), "C2", "18 W"),
        ((164.0, 133.0), "C2", "18 W"), ((210.0, 133.0), "C2", "12 W"),
        ((135.0, 208.0), "C2", "12 W"), ((149.0, 202.0), "C2", "8 W"),
    )
    for point, circuit, power in lights:
        layout.add_blockref("P02_LUMINARIA", point, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        centered(layout, f"{circuit} / {power}", (point[0], point[1] + 5.8), 1.25, "02_TEXTO")
    switches = ((94.0, 111.0), (102.0, 191.0), (163.0, 199.0), (126.0, 160.0), (198.0, 160.0), (150.0, 191.0), (158.0, 173.0), (218.0, 173.0))
    for point in switches:
        layout.add_blockref("P02_INTERRUPT", point, dxfattribs={"layer": "06_COMANDO"})
    command_line(layout, [(94.0, 111.0), (94.0, 145.0), (63.0, 145.0), (91.0, 145.0)])
    command_line(layout, [(102.0, 191.0), (76.0, 191.0), (76.0, 220.0)])
    command_line(layout, [(163.0, 199.0), (196.0, 199.0), (196.0, 220.0)])
    command_line(layout, [(126.0, 160.0), (140.0, 160.0), (140.0, 133.0), (164.0, 133.0)])
    command_line(layout, [(198.0, 160.0), (210.0, 160.0), (210.0, 133.0)])
    command_line(layout, [(150.0, 191.0), (135.0, 191.0), (135.0, 208.0), (149.0, 202.0)])
    command_line(layout, [(158.0, 173.0), (176.0, 173.0), (176.0, 176.0), (218.0, 173.0)])
    add_rect(layout, 248.0, 105.0, 402.0, 260.0, "12_LEGENDA")
    centered(layout, "RESUMO DE ILUMINAÇÃO", (325.0, 253.0), 2.3, "12_LEGENDA")
    draw_table(
        layout, 254.0, 244.0, (20.0, 62.0, 22.0, 44.0),
        ("CIRC.", "AMBIENTES", "PONTOS", "POTÊNCIA"),
        (("C1", "sala/quartos/circ.", "5", "69 W / 75 VA"), ("C2", "coz./banh./lav.", "5", "68 W / 73,913 VA")),
        row_h=13.0, text_h=1.4,
    )
    add_text(layout, "COMANDOS", (254.0, 197.0), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, "Sala, quartos, cozinha, banheiro e lavanderia: interruptor simples.\\P"
              "Circulação: dois interruptores paralelos indicativos.\\PTotal: 10 pontos LED e 8 comandos.",
              (254.0, 191.0), 140.0, 1.65, "13_NOTAS")
    layout.add_blockref("P02_LUMINARIA", (268.0, 145.0))
    add_text(layout, "Luminária de teto", (278.0, 143.5), 1.7, layer="12_LEGENDA")
    layout.add_blockref("P02_INTERRUPT", (268.0, 132.0))
    add_text(layout, "Interruptor", (278.0, 130.5), 1.7, layer="12_LEGENDA")


def draw_socket(layout, point: tuple[float, float], circuit: str, *, tue: bool = False, offset: tuple[float, float] = (0.0, 4.5)) -> None:
    layout.add_blockref("P02_TUE" if tue else "P02_TUG", point, dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, circuit, (point[0] + offset[0], point[1] + offset[1]), 1.25, "02_TEXTO")


def draw_sockets(layout) -> None:
    draw_floorplan(layout)
    c3 = ((47.0, 111.0), (72.0, 111.0), (108.0, 111.0), (41.0, 145.0), (41.0, 177.0), (108.0, 177.0),
          (41.0, 198.0), (41.0, 242.0), (76.0, 249.0), (108.0, 230.0), (162.0, 249.0), (196.0, 249.0),
          (228.0, 235.0), (228.0, 200.0), (177.0, 181.0))
    for point in c3:
        draw_socket(layout, point, "C3")
    c4 = ((122.0, 112.0), (145.0, 112.0), (175.0, 112.0), (122.0, 142.0), (180.0, 140.0), (165.0, 160.0))
    for point in c4:
        draw_socket(layout, point, "C4")
    c5 = ((121.0, 211.0), (192.0, 112.0), (225.0, 112.0))
    for point in c5:
        draw_socket(layout, point, "C5")
    for point, circuit, offset in (((172.0, 154.0), "C6", (0.0, -5.0)), ((147.0, 220.0), "C7", (5.5, 0.0)), ((216.0, 150.0), "C8", (5.5, 0.0))):
        draw_socket(layout, point, circuit, tue=True, offset=offset)
    layout.add_blockref("P02_QD", (121.0, 175.0), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    add_rect(layout, 248.0, 105.0, 402.0, 260.0, "12_LEGENDA")
    centered(layout, "RESUMO DE TOMADAS", (325.0, 253.0), 2.3, "12_LEGENDA")
    draw_table(
        layout, 254.0, 244.0, (18.0, 58.0, 22.0, 50.0),
        ("CIRC.", "ATENDIMENTO", "QTD.", "CARGA"),
        (("C3", "sala/quartos/circ.", "15", "1 500 VA"), ("C4", "cozinha", "6", "2 100 VA"),
         ("C5", "banheiro/lav.", "3", "1 800 VA"), ("C6", "forno 220 V", "1", "3 000 VA"),
         ("C7", "chuveiro 220 V", "1", "5 500 VA"), ("C8", "lavadora 127 V", "1", "1 500 VA")),
        row_h=10.5, text_h=1.4,
    )
    add_text(layout, "ALTURAS INDICATIVAS", (254.0, 164.0), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, "TUG baixa: 0,30 m. Bancada: 1,10 m. Forno/lavadora: 0,60 m.\\P"
              "Chuveiro: conexão fixa a 2,20 m. Confirmar equipamentos e zonas.",
              (254.0, 158.0), 140.0, 1.65, "13_NOTAS")


def conduit(layout, points: list[tuple[float, float]], label: str, label_point: tuple[float, float]) -> None:
    layout.add_lwpolyline(points, dxfattribs={"layer": "10_ELETROCALHAS", "linetype": "DASHED"})
    centered(layout, label, label_point, 1.25, "08_CABOS")


def draw_conduits(layout) -> None:
    draw_floorplan(layout)
    qd = (121.0, 175.0)
    layout.add_blockref("P02_QD", qd)
    boxes = ((76.0, 145.0), (76.0, 220.0), (176.0, 176.0), (152.0, 133.0), (210.0, 133.0), (135.0, 208.0), (196.0, 220.0))
    for point in boxes:
        layout.add_blockref("P02_CAIXA", point)
    conduit(layout, [(121.0, 175.0), (100.0, 175.0), (100.0, 145.0), (76.0, 145.0)], "DN25 C1/C3", (88.0, 153.0))
    conduit(layout, [(76.0, 145.0), (76.0, 220.0)], "DN20 C1/C3", (80.0, 205.0))
    conduit(layout, [(121.0, 175.0), (176.0, 175.0), (176.0, 176.0), (196.0, 176.0), (196.0, 220.0)], "DN25 C1/C3", (196.0, 179.5))
    conduit(layout, [(121.0, 175.0), (121.0, 133.0), (152.0, 133.0)], "DN25 C2/C4/C6", (139.0, 137.0))
    conduit(layout, [(152.0, 133.0), (210.0, 133.0)], "DN25 C2/C5/C8", (201.0, 137.0))
    conduit(layout, [(121.0, 175.0), (135.0, 175.0), (135.0, 208.0)], "DN20 C2/C5/C7", (140.0, 194.0))
    conduit(layout, [(235.0, 175.0), (121.0, 175.0)], "DN32 ALIMENTADOR", (220.0, 171.0))
    centered(layout, "ENTRADA", (241.0, 175.0), 1.45, "02_TEXTO")
    add_rect(layout, 248.0, 105.0, 402.0, 260.0, "12_LEGENDA")
    centered(layout, "ROTAS E OCUPAÇÃO", (325.0, 253.0), 2.3, "12_LEGENDA")
    draw_table(
        layout, 254.0, 244.0, (25.0, 48.0, 75.0),
        ("DN", "CIRCUITOS", "CRITÉRIO"),
        (("20 mm", "ramais", "até caixa/ponto"), ("25 mm", "grupos", "troncos internos"), ("32 mm", "alimentador", "entrada a QD1")),
        row_h=12.0, text_h=1.45,
    )
    add_text(layout, "VERIFICAÇÕES PENDENTES", (254.0, 193.0), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, "- Ocupação e diâmetro interno real.\\P- Agrupamento e dissipação térmica.\\P"
              "- Número de curvas e caixas de passagem.\\P- Segregação de outros sistemas.\\P"
              "- Comprimento e queda de tensão medidos.",
              (254.0, 187.0), 140.0, 1.65, "13_NOTAS")


def draw_unifilar(layout) -> None:
    centered(layout, "REDE 2F+N+PE - 127/220 V - 60 Hz", (67.0, 252.0), 1.8)
    line(layout, (25.0, 235.0), (48.0, 235.0), "05_POTENCIA")
    boxed_label(layout, 48.0, 224.0, 83.0, 246.0, "MED1", "medição")
    line(layout, (83.0, 235.0), (94.0, 235.0), "05_POTENCIA")
    boxed_label(layout, 94.0, 224.0, 125.0, 246.0, "QG1", "2P C63 A")
    line(layout, (125.0, 235.0), (137.0, 235.0), "05_POTENCIA")
    boxed_label(layout, 137.0, 224.0, 168.0, 246.0, "DR1", "2P 63 A / 30 mA")
    line(layout, (168.0, 235.0), (185.0, 235.0), "05_POTENCIA")
    line(layout, (185.0, 112.0), (185.0, 245.0), "05_POTENCIA")
    centered(layout, "BARRAMENTO QD1", (185.0, 252.0), 1.7, "05_POTENCIA")
    line(layout, (110.0, 224.0), (110.0, 203.0), "05_POTENCIA")
    boxed_label(layout, 96.0, 184.0, 124.0, 203.0, "DPS1", "2 x 275 V")
    line(layout, (110.0, 184.0), (110.0, 169.0), "05_POTENCIA")
    line(layout, (76.0, 169.0), (145.0, 169.0), "05_POTENCIA")
    layout.add_blockref("SIM_TERRA", (78.0, 165.0), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "BEP / PE", (111.0, 174.0), 1.6, "05_POTENCIA")
    line(layout, (25.0, 158.0), (168.0, 158.0), "09_BORNES")
    line(layout, (25.0, 149.0), (168.0, 149.0), "09_BORNES")
    centered(layout, "BARRA N ISOLADA", (60.0, 161.5), 1.45, "09_BORNES")
    centered(layout, "BARRA PE", (60.0, 152.5), 1.45, "09_BORNES")
    for index, circuit in enumerate(CIRCUITS):
        y = 238.0 - index * 16.0
        line(layout, (185.0, y), (205.0, y), "05_POTENCIA")
        layout.add_blockref("SIM_DISJUNTOR", (215.0, y), dxfattribs={"layer": "05_POTENCIA"})
        line(layout, (220.0, y), (238.0, y), "05_POTENCIA")
        add_text(layout, circuit.tag, (242.0, y + 2.0), 1.7, layer="05_POTENCIA", style=TITLE_STYLE)
        add_text(layout, circuit.description, (262.0, y + 2.0), 1.55, layer="02_TEXTO")
        add_text(layout, f"{circuit.voltage} V | {circuit.poles}P {circuit.curve}{circuit.breaker} | {circuit.conductor:g} mm² + PE",
                 (262.0, y - 2.1), 1.35, layer="08_CABOS")
    add_rect(layout, 238.0, 105.0, 402.0, 252.0, "12_LEGENDA")
    add_text(layout, "PROTEÇÕES GERAIS", (25.0, 135.0), 2.0, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, "QG1: 2P 63 A curva C.\\PDR1: 2P 63 A, 30 mA, tipo A.\\P"
              "DPS1: tipo 2, Uc 275 V, Imax 20 kA.\\PCapacidade de interrupção: a calcular.",
              (25.0, 130.0), 135.0, 1.55, "13_NOTAS")


def module_box(layout, x: float, y: float, modules: int, tag: str, detail: str, layer: str = "04_EQUIPAMENTOS") -> float:
    width = modules * 13.0
    add_rect(layout, x, y, x + width, y + 30.0, layer)
    for index in range(1, modules):
        line(layout, (x + index * 13.0, y), (x + index * 13.0, y + 30.0), layer)
    centered(layout, tag, (x + width / 2.0, y + 20.0), 1.8, layer)
    centered(layout, detail, (x + width / 2.0, y + 9.0), 1.25, "02_TEXTO")
    return x + width


def draw_distribution_board(layout) -> None:
    add_rect(layout, 24.0, 105.0, 276.0, 260.0, "04_EQUIPAMENTOS")
    centered(layout, "QD1 - QUADRO DE EMBUTIR - 24 MÓDULOS", (150.0, 252.0), 2.3, "04_EQUIPAMENTOS")
    for y in (216.0, 166.0, 116.0):
        line(layout, (34.0, y), (266.0, y), "10_ELETROCALHAS")
        line(layout, (34.0, y + 32.0), (266.0, y + 32.0), "10_ELETROCALHAS")
    x = 38.0
    x = module_box(layout, x, 218.0, 2, "QG1", "2P C63") + 4.0
    x = module_box(layout, x, 218.0, 2, "DPS1", "2 x 275 V") + 4.0
    x = module_box(layout, x, 218.0, 2, "DR1", "2P 63/0,03") + 4.0
    module_box(layout, x, 218.0, 2, "RESERVA", "2 módulos")
    x = 38.0
    for circuit in CIRCUITS[:5]:
        x = module_box(layout, x, 168.0, circuit.poles, circuit.tag, f"{circuit.curve}{circuit.breaker}") + 4.0
    x = module_box(layout, x, 168.0, 2, "C6", "2P C20") + 4.0
    module_box(layout, x, 168.0, 1, "RESERVA", "1 módulo")
    x = 38.0
    x = module_box(layout, x, 118.0, 2, "C7", "2P C32") + 4.0
    x = module_box(layout, x, 118.0, 1, "C8", "C16") + 4.0
    module_box(layout, x, 118.0, 5, "RESERVA", "5 módulos")
    add_rect(layout, 177.0, 126.0, 258.0, 138.0, "09_BORNES")
    centered(layout, "BARRA N - ISOLADA", (217.5, 132.0), 1.6, "09_BORNES")
    add_rect(layout, 177.0, 144.0, 258.0, 156.0, "09_BORNES")
    centered(layout, "BARRA PE", (217.5, 150.0), 1.6, "09_BORNES")
    add_rect(layout, 286.0, 105.0, 402.0, 260.0, "12_LEGENDA")
    centered(layout, "ORGANIZAÇÃO", (344.0, 253.0), 2.3, "12_LEGENDA")
    add_mtext(layout, "TRILHO 1 - 8 MÓDULOS\\PQG1 - DPS1 - DR1 - reserva 2\\P\\PTRILHO 2 - 8 MÓDULOS\\PC1 a C6 - reserva 1\\P\\PTRILHO 3 - 8 MÓDULOS\\PC7 - C8 - reserva 5",
              (294.0, 242.0), 100.0, 1.75, "12_LEGENDA")
    add_text(layout, "REGRAS", (294.0, 176.0), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, "- Identificar todos os circuitos.\\P- Separar barras N e PE.\\P- Manter tampas cegas na reserva.\\P"
              "- Confirmar torque e terminais.\\P- Verificar dissipação e grau IP.\\P- Fabricante define dimensões finais.",
              (294.0, 170.0), 100.0, 1.55, "13_NOTAS")


def draw_load_schedule(layout) -> None:
    rows = tuple(
        (
            c.tag,
            c.description,
            str(c.voltage),
            c.phases,
            f"{c.va:.3f}",
            f"{c.current:.3f}",
            f"{c.conductor:g}",
            f"{c.poles}P {c.curve}{c.breaker}",
            f"{c.drop:.3f}%",
        )
        for c in CIRCUITS
    )
    draw_table(
        layout,
        18.0,
        257.0,
        (18.0, 105.0, 22.0, 25.0, 42.0, 35.0, 35.0, 45.0, 57.0),
        ("CIRC.", "DESCRIÇÃO", "V", "FASE", "VA", "Ib (A)", "S (mm²)", "DJ", "QUEDA"),
        rows,
        row_h=14.0,
        text_h=1.45,
    )
    add_rect(layout, 18.0, 105.0, 402.0, 125.0, "12_LEGENDA")
    centered(layout, "INSTALADA: 15 548,913 VA", (86.0, 115.0), 1.9, "12_LEGENDA")
    centered(layout, "DEMANDA ACADÊMICA: 12 592,120 VA", (226.0, 115.0), 1.9, "12_LEGENDA")
    centered(layout, "QG1: 2P 63 A | ALIM.: 16 mm²", (349.0, 115.0), 1.9, "12_LEGENDA")
    centered(layout, "QUEDA COMBINADA CONSERVADORA: C3 = 3,107% | C8 = 3,316%", (210.0, 100.0), 1.65, "13_NOTAS")


def detail_title(layout, x0: float, x1: float, value: str) -> None:
    centered(layout, value, ((x0 + x1) / 2.0, 251.0), 2.1, "12_LEGENDA")
    line(layout, (x0 + 4.0, 246.0), (x1 - 4.0, 246.0), "12_LEGENDA")


def draw_grounding_details(layout) -> None:
    panels = ((18.0, 139.0), (149.0, 270.0), (280.0, 402.0))
    for x0, x1 in panels:
        add_rect(layout, x0, 105.0, x1, 260.0, "12_LEGENDA")
    detail_title(layout, 18.0, 139.0, "1 - ORIGEM TN-S CONCEITUAL")
    detail_title(layout, 149.0, 270.0, "2 - EQUIPOTENCIALIZAÇÃO")
    detail_title(layout, 280.0, 402.0, "3 - ELETRODO INDICATIVO")

    line(layout, (33.0, 225.0), (55.0, 225.0), "05_POTENCIA")
    boxed_label(layout, 55.0, 214.0, 88.0, 236.0, "QD1", "N e PE separados")
    line(layout, (88.0, 225.0), (117.0, 225.0), "05_POTENCIA")
    centered(layout, "F1/F2/N", (103.0, 231.0), 1.5, "08_CABOS")
    line(layout, (71.5, 214.0), (71.5, 188.0), "05_POTENCIA")
    add_rect(layout, 43.0, 174.0, 100.0, 188.0, "09_BORNES")
    centered(layout, "BEP / BARRA PE", (71.5, 181.0), 1.7, "09_BORNES")
    line(layout, (71.5, 174.0), (71.5, 145.0), "05_POTENCIA")
    layout.add_blockref("SIM_TERRA", (71.5, 141.0), dxfattribs={"layer": "05_POTENCIA"})
    add_mtext(layout, "PE acompanha todos os circuitos.\\PNeutro não é unido ao PE em QD1.\\P"
              "Ponto de origem deve ser confirmado.", (26.0, 128.0), 105.0, 1.45, "13_NOTAS")

    boxed_label(layout, 175.0, 214.0, 204.0, 236.0, "C7", "chuveiro 220 V")
    boxed_label(layout, 216.0, 214.0, 250.0, 236.0, "MASSA", "parte acessível")
    line(layout, (189.5, 214.0), (189.5, 182.0), "05_POTENCIA")
    line(layout, (233.0, 214.0), (233.0, 182.0), "05_POTENCIA")
    line(layout, (174.0, 182.0), (251.0, 182.0), "05_POTENCIA")
    add_rect(layout, 179.0, 164.0, 246.0, 178.0, "09_BORNES")
    centered(layout, "LIGAÇÃO EQUIPOTENCIAL / PE", (212.5, 171.0), 1.55, "09_BORNES")
    line(layout, (212.5, 164.0), (212.5, 143.0), "05_POTENCIA")
    layout.add_blockref("SIM_TERRA", (212.5, 139.0), dxfattribs={"layer": "05_POTENCIA"})
    add_mtext(layout, "Confirmar zonas, acessórios metálicos, continuidade e seção.\\P"
              "DR de 30 mA é proteção adicional; não substitui PE.", (157.0, 128.0), 105.0, 1.45, "13_NOTAS")

    line(layout, (289.0, 208.0), (393.0, 208.0), "11_ARQUITETURA")
    centered(layout, "NÍVEL DO SOLO", (341.0, 214.0), 1.5, "11_ARQUITETURA")
    add_rect(layout, 324.0, 194.0, 358.0, 208.0, "04_EQUIPAMENTOS")
    centered(layout, "CAIXA DE INSPEÇÃO", (341.0, 201.0), 1.45, "04_EQUIPAMENTOS")
    line(layout, (341.0, 194.0), (341.0, 130.0), "05_POTENCIA")
    line(layout, (338.5, 130.0), (343.5, 130.0), "05_POTENCIA")
    add_text(layout, "HASTE COBREADA 2,40 m (ASSUMIDA)", (350.0, 160.0), 1.45, layer="02_TEXTO", rotation=90.0, align=TextEntityAlignment.MIDDLE_CENTER)
    line(layout, (341.0, 194.0), (306.0, 225.0), "08_CABOS")
    centered(layout, "Cu 16 mm² ATÉ BEP", (320.0, 228.0), 1.5, "08_CABOS")
    add_mtext(layout, "Não declarar resistência sem medição.\\PVerificar solo, corrosão e conexões.\\P"
              "Quantidade de hastes depende do projeto.\\PCaixa deve permanecer acessível.",
              (288.0, 122.0), 106.0, 1.45, "13_NOTAS")


DRAWERS = (
    draw_architecture,
    draw_lighting,
    draw_sockets,
    draw_conduits,
    draw_unifilar,
    draw_distribution_board,
    draw_load_schedule,
    draw_grounding_details,
)


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    (root / PROJECT_SLUG / "exports").mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec, drawer in zip(SHEETS, DRAWERS):
        doc, layout = create_sheet(config, spec)
        drawer(layout)
        prepare_deterministic_write(doc)
        output = source_dir / spec.filename
        doc.saveas(output)
        outputs.append(output)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositório")
    return parser.parse_args()


def main() -> int:
    root = parse_args().root.resolve()
    for output in generate(root):
        print(output.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
