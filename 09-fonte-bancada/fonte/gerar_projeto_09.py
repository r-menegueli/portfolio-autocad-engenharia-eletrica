"""Gera as seis pranchas DXF do Projeto 09 de forma determinística."""

from __future__ import annotations

import argparse
import csv
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


PROJECT_SLUG = "09-fonte-bancada"
PROJECT_DATE = "2026-09-09"
REVISION = "00"


@dataclass(frozen=True)
class SheetSpec:
    number: int
    filename: str
    title: str
    subtitle: str
    notes: str
    legend: str


SHEETS = (
    SheetSpec(
        1,
        "01_diagrama_blocos.dxf",
        "DIAGRAMA DE BLOCOS",
        "Fonte acadêmica 0-30 Vcc / 0-5 A / 150 W com saída isolada e flutuante",
        "Blocos PS1, REG1, PS2 e M1 são especificações funcionais fictícias.\\P"
        "A arquitetura não comprova isolação, segurança, EMC, precisão ou desempenho.",
        "Vermelho: potência | Verde: comando/PE | Magenta: medição | Azul: bornes",
    ),
    SheetSpec(
        2,
        "02_diagrama_eletrico.dxf",
        "DIAGRAMA ELÉTRICO",
        "Entrada, proteção, conversão, regulação, medição e comando térmico",
        "PE é permanente e não passa por chave ou fusível. Saída CC sem ligação interna ao PE.\\P"
        "Valores de proteção são propostas; Icn, isolação, inrush e coordenação estão pendentes.",
        "F: fusível | S: chave/comando | PS: fonte | REG: regulador | K: relé | X: borne",
    ),
    SheetSpec(
        3,
        "03_painel_frontal.dxf",
        "PAINEL FRONTAL",
        "Interface 320 x 150 mm com medição, ajustes, comando e bornes",
        "Cotas são interfaces acadêmicas. Conferir recortes, tolerâncias e antirotação nos fabricantes.\\P"
        "O borne PE é de chassi e não é ligado internamente ao negativo da saída.",
        "Branco: geometria | Magenta: medição | Verde/âmbar: estados | Azul: conectores",
    ),
    SheetSpec(
        4,
        "04_layout_interno.dxf",
        "LAYOUT INTERNO",
        "Zonas segregadas, fluxo de ar, PE dedicado e rotas de cabos",
        "Posições e folgas não são instruções de montagem. Cobrir a zona primária.\\P"
        "Validar escoamento, isolação, EMC, temperatura, vibração, manutenção e acesso.",
        "Cinza: gabinete | Vermelho: rede/potência | Laranja: CC | Verde: PE/ar | Tracejado: zona",
    ),
    SheetSpec(
        5,
        "05_detalhes_mecanicos.dxf",
        "DETALHES MECÂNICOS",
        "Recortes frontal e traseiro, ventilação e envelope do gabinete",
        "Dimensões nominais não incluem tolerâncias, raios, tratamento ou ferramental.\\P"
        "Arquivos não devem ser enviados diretamente a corte ou fabricação.",
        "D: diâmetro | X/Y: origem no canto inferior esquerdo | PNL: painel | FAN: ventilador",
    ),
    SheetSpec(
        6,
        "06_interligacoes.dxf",
        "INTERLIGAÇÕES",
        "Conectividade de rede, barramentos, saída, Kelvin, comandos e PE",
        "A lista W01-W25 define intenção de ligação, não chicote liberado.\\P"
        "Confirmar terminais, crimpagem, torque, isolação, cores, proteção e alívio mecânico.",
        "Preto/azul: L/N | Verde-amarelo: PE | Vermelho/preto: CC | Branco: comando",
    ),
)


def read_rows(project: Path, filename: str) -> list[dict[str, str]]:
    with (project / filename).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def line(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    add_line(layout, start, end, layer)


def centered(
    layout,
    value: str,
    point: tuple[float, float],
    height: float = 1.45,
    layer: str = "02_TEXTO",
) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def left(
    layout,
    value: str,
    point: tuple[float, float],
    height: float = 1.3,
    layer: str = "02_TEXTO",
) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_LEFT)


def orthogonal(layout, points: tuple[tuple[float, float], ...], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def arrow(
    layout,
    start: tuple[float, float],
    end: tuple[float, float],
    layer: str,
    label: str = "",
    label_offset: tuple[float, float] = (0.0, 4.0),
) -> None:
    line(layout, start, end, layer)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base = (end[0] - 4.0 * ux, end[1] - 4.0 * uy)
    layout.add_lwpolyline(
        [end, (base[0] + 1.6 * px, base[1] + 1.6 * py), (base[0] - 1.6 * px, base[1] - 1.6 * py)],
        close=True,
        dxfattribs={"layer": layer},
    )
    if label:
        centered(
            layout,
            label,
            ((start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1]),
            1.05,
            layer,
        )


def component(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    detail: str,
    layer: str = "04_EQUIPAMENTOS",
    detail_layer: str = "02_TEXTO",
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5.0), 1.55, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4.0), 0.95, detail_layer)


def table(
    layout,
    x: float,
    top: float,
    widths: tuple[float, ...],
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    *,
    row_height: float,
    text_height: float = 0.9,
    layer: str = "12_LEGENDA",
) -> None:
    total_width = sum(widths)
    total_height = row_height * (len(rows) + 1)
    add_rect(layout, x, top - total_height, x + total_width, top, layer)
    cursor = x
    centers: list[float] = []
    for width in widths:
        centers.append(cursor + width / 2)
        cursor += width
        if cursor < x + total_width - 0.001:
            line(layout, (cursor, top - total_height), (cursor, top), layer)
    for index in range(1, len(rows) + 1):
        y = top - row_height * index
        line(layout, (x, y), (x + total_width, y), layer)
    for value, cx in zip(headers, centers):
        centered(layout, value, (cx, top - row_height / 2), text_height, layer)
    for row_index, row in enumerate(rows):
        cy = top - row_height * (row_index + 1.5)
        for value, cx in zip(row, centers):
            centered(layout, value, (cx, cy), text_height, "02_TEXTO")


def dimension_h(layout, x0: float, x1: float, y: float, label: str) -> None:
    line(layout, (x0, y), (x1, y), "03_COTAS")
    line(layout, (x0, y - 2.5), (x0, y + 2.5), "03_COTAS")
    line(layout, (x1, y - 2.5), (x1, y + 2.5), "03_COTAS")
    centered(layout, label, ((x0 + x1) / 2, y + 3.3), 1.1, "03_COTAS")


def dimension_v(layout, x: float, y0: float, y1: float, label: str) -> None:
    line(layout, (x, y0), (x, y1), "03_COTAS")
    line(layout, (x - 2.5, y0), (x + 2.5, y0), "03_COTAS")
    line(layout, (x - 2.5, y1), (x + 2.5, y1), "03_COTAS")
    add_text(
        layout,
        label,
        (x - 4.0, (y0 + y1) / 2),
        1.1,
        layer="03_COTAS",
        align=TextEntityAlignment.MIDDLE_CENTER,
        rotation=90.0,
    )


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    fuse = doc.blocks.new("P09_FUSIVEL", base_point=(0.0, 0.0))
    line(fuse, (-6.0, 0.0), (-3.5, 0.0), "05_POTENCIA")
    add_rect(fuse, -3.5, -1.8, 3.5, 1.8, "05_POTENCIA")
    line(fuse, (-2.5, -1.1), (2.5, 1.1), "05_POTENCIA")
    line(fuse, (3.5, 0.0), (6.0, 0.0), "05_POTENCIA")

    switch = doc.blocks.new("P09_CHAVE", base_point=(0.0, 0.0))
    line(switch, (-6.0, 0.0), (-2.0, 0.0), "05_POTENCIA")
    line(switch, (-2.0, 0.0), (2.8, 3.0), "05_POTENCIA")
    line(switch, (2.0, 0.0), (6.0, 0.0), "05_POTENCIA")

    meter = doc.blocks.new("P09_MEDIDOR", base_point=(0.0, 0.0))
    add_rect(meter, -13.0, -6.5, 13.0, 6.5, "07_INSTRUMENTACAO")
    centered(meter, "V / A", (0.0, 0.0), 2.0, "07_INSTRUMENTACAO")

    potentiometer = doc.blocks.new("P09_POT", base_point=(0.0, 0.0))
    potentiometer.add_circle((0.0, 0.0), 4.0, dxfattribs={"layer": "06_COMANDO"})
    line(potentiometer, (-4.0, 0.0), (4.0, 0.0), "06_COMANDO")
    line(potentiometer, (0.0, -4.0), (0.0, 4.0), "06_COMANDO")

    led = doc.blocks.new("P09_LED", base_point=(0.0, 0.0))
    led.add_circle((0.0, 0.0), 2.5, dxfattribs={"layer": "07_INSTRUMENTACAO"})

    fan = doc.blocks.new("P09_FAN", base_point=(0.0, 0.0))
    fan.add_circle((0.0, 0.0), 12.0, dxfattribs={"layer": "10_ELETROCALHAS"})
    line(fan, (-8.0, -8.0), (8.0, 8.0), "10_ELETROCALHAS")
    line(fan, (-8.0, 8.0), (8.0, -8.0), "10_ELETROCALHAS")

    terminal = doc.blocks.new("P09_BORNE", base_point=(0.0, 0.0))
    terminal.add_circle((0.0, 0.0), 3.5, dxfattribs={"layer": "09_BORNES"})
    terminal.add_circle((0.0, 0.0), 1.3, dxfattribs={"layer": "09_BORNES"})


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("EMISSAO INICIAL DO PROJETO 09", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.45, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATORIO", (22, 42), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.42, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.42, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/06",
        "ARQUIVO": spec.filename,
        "UNIDADES": "mm",
        "ESCALA": "S/ESC.",
        "FOLHA": "A3",
        "STATUS": "CONCEIT.",
    }
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(values)


def create_sheet(config: dict, spec: SheetSpec):
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = PROJECT_SLUG
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/06"
    metadata["PORTFOLIO_EPISTEMIC_STATUS"] = "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 3.85, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.8, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_block_diagram(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "CADEIA PRINCIPAL DE ENERGIA", (205, 258), 1.45, "05_POTENCIA")
    blocks = (
        (18, 210, 57, 240, "X1", "90-264 Vca\nL/N/PE"),
        (67, 210, 111, 240, "F1/S1/FL1", "PROTEÇÃO\nE FILTRO"),
        (121, 202, 171, 248, "PS1", "AC/DC ISOLADA\n36 V / 7 A"),
        (181, 210, 213, 240, "F2", "7,5 A CC"),
        (223, 202, 277, 248, "REG1", "BUCK CC/CV\n0-30 V / 5 A"),
        (287, 210, 325, 240, "K1/SH1", "HABILITAÇÃO\nE MEDIÇÃO"),
        (343, 202, 400, 248, "X2", "0-30 Vcc\n0-5 A / 150 W"),
    )
    for x0, y0, x1, y1, tag, detail in blocks:
        component(layout, x0, y0, x1, y1, tag, detail.replace("\n", " | "), "04_EQUIPAMENTOS")
    for start, end, label in (
        ((57, 225), (67, 225), "REDE"),
        ((111, 225), (121, 225), "L/N"),
        ((171, 225), (181, 225), "36 V"),
        ((213, 225), (223, 225), "36 V"),
        ((277, 225), (287, 225), "0-30 V"),
        ((325, 225), (343, 225), "SAÍDA"),
    ):
        arrow(layout, start, end, "05_POTENCIA", label, (0, 5))

    component(layout, 121, 140, 171, 176, "PS2", "36 -> 12 V / 1 A", "04_EQUIPAMENTOS")
    component(layout, 205, 140, 255, 176, "CTRL", "RV1/RV2/S2/TS1", "06_COMANDO")
    layout.add_blockref("P09_MEDIDOR", (300, 158), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "M1", (300, 172), 1.2, "07_INSTRUMENTACAO")
    layout.add_blockref("P09_FAN", (370, 158), dxfattribs={"layer": "10_ELETROCALHAS"})
    centered(layout, "FAN1 / TH1", (370, 139), 1.1, "10_ELETROCALHAS")
    orthogonal(layout, ((146, 202), (146, 176)), "08_CABOS")
    arrow(layout, (171, 158), (205, 158), "06_COMANDO", "12 V")
    arrow(layout, (255, 158), (287, 212), "06_COMANDO", "ENABLE", (7, 1))
    arrow(layout, (325, 217), (300, 164), "07_INSTRUMENTACAO", "KELVIN/SHUNT", (-8, 0))
    arrow(layout, (171, 150), (358, 150), "06_COMANDO", "VENTILAÇÃO", (35, 4))

    add_rect(layout, 20, 100, 400, 132, "13_NOTAS")
    centered(layout, "LIMITES DA ARQUITETURA", (210, 126), 1.2, "13_NOTAS")
    centered(
        layout,
        "PE PERMANENTE NO CHASSI | SAÍDA CC FLUTUANTE | NEGATIVO SEM VÍNCULO INTERNO AO PE",
        (210, 120),
        1.05,
        "06_COMANDO",
    )
    add_mtext(
        layout,
        "Sem PCB, seleção comercial, ensaios dielétricos, EMC, corrente de toque, falha única, calibração, térmica ou certificação.",
        (28, 113),
        360,
        1.05,
        "13_NOTAS",
    )


def draw_electrical_diagram(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "ZONA PRIMÁRIA - ACESSO RESTRITO E COBERTO", (130, 258), 1.3, "05_POTENCIA")
    add_rect(layout, 18, 178, 240, 250, "11_ARQUITETURA")
    centered(layout, "X1", (28, 240), 1.3, "09_BORNES")
    centered(layout, "L", (28, 229), 1.0, "09_BORNES")
    centered(layout, "N", (28, 217), 1.0, "09_BORNES")
    centered(layout, "PE", (28, 190), 1.0, "09_BORNES")
    line(layout, (34, 229), (190, 229), "05_POTENCIA")
    line(layout, (34, 217), (190, 217), "05_POTENCIA")
    layout.add_blockref("P09_FUSIVEL", (55, 229), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "F1 T4 A", (55, 238), 0.95, "05_POTENCIA")
    for y in (229, 217):
        layout.add_blockref("P09_CHAVE", (85, y), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "S1 2P 10 A", (85, 240), 0.95, "05_POTENCIA")
    component(layout, 105, 207, 137, 239, "FL1", "EMI 2P / 10 A", "04_EQUIPAMENTOS")
    component(layout, 148, 211, 166, 235, "MOV1", "275 Vca L-N", "05_POTENCIA")
    line(layout, (148, 229), (148, 223), "05_POTENCIA")
    line(layout, (148, 217), (148, 223), "05_POTENCIA")
    component(layout, 190, 200, 232, 244, "PS1", "36 Vcc / 7 A", "04_EQUIPAMENTOS")
    line(layout, (26, 190), (222, 190), "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (75, 190), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "PE1 CHASSI", (75, 184), 0.95, "06_COMANDO")
    line(layout, (211, 200), (211, 190), "06_COMANDO")
    centered(layout, "PE NÃO SECCIONADO", (150, 185), 1.0, "06_COMANDO")

    centered(layout, "ZONA SECUNDÁRIA ISOLADA - 36 Vcc / SAÍDA FLUTUANTE", (325, 258), 1.3, "08_CABOS")
    line(layout, (232, 232), (390, 232), "08_CABOS")
    line(layout, (232, 212), (390, 212), "08_CABOS")
    centered(layout, "+36", (238, 236), 0.9, "08_CABOS")
    centered(layout, "0V36", (238, 208), 0.9, "08_CABOS")
    layout.add_blockref("P09_FUSIVEL", (258, 232), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "F2 7,5 A", (258, 240), 0.9, "05_POTENCIA")
    component(layout, 282, 198, 330, 246, "REG1", "BUCK CC/CV 150 W", "04_EQUIPAMENTOS")
    layout.add_blockref("P09_CHAVE", (348, 232), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "K1 NO", (348, 240), 0.9, "05_POTENCIA")
    component(layout, 362, 204, 380, 220, "SH1", "10 A / 75 mV", "07_INSTRUMENTACAO")
    centered(layout, "X2 +", (394, 232), 1.0, "09_BORNES")
    centered(layout, "X2 -", (394, 212), 1.0, "09_BORNES")
    centered(layout, "0-30 Vcc / 0-5 A", (335, 190), 1.15, "05_POTENCIA")

    component(layout, 190, 132, 232, 166, "PS2", "36 -> 12 Vcc", "04_EQUIPAMENTOS")
    orthogonal(layout, ((242, 212), (242, 160), (232, 160)), "08_CABOS")
    component(layout, 252, 132, 282, 166, "TH1", "40 °C / FAN", "06_COMANDO")
    layout.add_blockref("P09_FAN", (308, 149), dxfattribs={"layer": "10_ELETROCALHAS", "xscale": 0.75, "yscale": 0.75})
    centered(layout, "FAN1", (308, 133), 0.95, "10_ELETROCALHAS")
    arrow(layout, (232, 149), (252, 149), "06_COMANDO", "12 V")
    arrow(layout, (282, 149), (299, 149), "06_COMANDO")

    component(layout, 190, 100, 222, 124, "TS1", "NF / 75 °C", "06_COMANDO")
    component(layout, 236, 100, 268, 124, "S2", "HABILITA", "06_COMANDO")
    centered(layout, "K1", (306, 112), 1.1, "06_COMANDO")
    line(layout, (300, 112), (312, 112), "06_COMANDO")
    line(layout, (306, 106), (306, 118), "06_COMANDO")
    arrow(layout, (222, 112), (236, 112), "06_COMANDO")
    arrow(layout, (268, 112), (300, 112), "06_COMANDO", "COIL")
    centered(layout, "CADEIA: +12 V -> TS1 -> S2 -> K1", (247, 128), 1.0, "06_COMANDO")

    layout.add_blockref("P09_MEDIDOR", (360, 150), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "M1", (360, 164), 1.0, "07_INSTRUMENTACAO")
    orthogonal(layout, ((350, 156), (340, 176), (390, 176), (390, 232)), "07_INSTRUMENTACAO")
    orthogonal(layout, ((370, 144), (382, 180), (382, 216)), "07_INSTRUMENTACAO")
    centered(layout, "SENSE KELVIN / SHUNT", (360, 184), 0.9, "07_INSTRUMENTACAO")
    centered(layout, "X3 PE DE CHASSI SEPARADO", (80, 106), 1.1, "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (80, 118), dxfattribs={"layer": "06_COMANDO"})


def draw_front_panel(layout, data: dict[str, list[dict[str, str]]]) -> None:
    x0, y0, width, height = 45.0, 105.0, 320.0, 150.0
    add_rect(layout, x0, y0, x0 + width, y0 + height, "11_ARQUITETURA")
    centered(layout, "FONTE DE BANCADA 0-30 V / 0-5 A", (x0 + width / 2, y0 + height - 12), 2.0, "02_TEXTO")

    # Recortes localizados pela origem inferior esquerda do painel.
    add_rect(layout, x0 + 20, y0 + 81, x0 + 50, y0 + 103, "06_COMANDO")
    centered(layout, "S1", (x0 + 35, y0 + 110), 1.2, "06_COMANDO")
    centered(layout, "REDE", (x0 + 35, y0 + 75), 1.0, "02_TEXTO")

    add_rect(layout, x0 + 69, y0 + 82, x0 + 141, y0 + 118, "07_INSTRUMENTACAO")
    centered(layout, "M1", (x0 + 105, y0 + 100), 2.4, "07_INSTRUMENTACAO")
    centered(layout, "V     A", (x0 + 105, y0 + 75), 1.0, "07_INSTRUMENTACAO")

    for x, tag, label in ((175, "RV1", "TENSÃO"), (220, "RV2", "CORRENTE")):
        layout.add_blockref("P09_POT", (x0 + x, y0 + 100), dxfattribs={"layer": "06_COMANDO"})
        centered(layout, tag, (x0 + x, y0 + 112), 1.1, "06_COMANDO")
        centered(layout, label, (x0 + x, y0 + 88), 1.0, "02_TEXTO")

    for x, tag, label in ((174, "H1", "CV"), (198, "H2", "CC")):
        layout.add_blockref("P09_LED", (x0 + x, y0 + 72), dxfattribs={"layer": "07_INSTRUMENTACAO"})
        centered(layout, label, (x0 + x, y0 + 65), 0.95, "07_INSTRUMENTACAO")
        centered(layout, tag, (x0 + x, y0 + 79), 0.8, "07_INSTRUMENTACAO")

    layout.add_circle((x0 + 270, y0 + 100), 8.0, dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "S2", (x0 + 270, y0 + 112), 1.1, "06_COMANDO")
    centered(layout, "SAÍDA", (x0 + 270, y0 + 86), 1.0, "02_TEXTO")
    layout.add_blockref("P09_LED", (x0 + 292, y0 + 100), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "H3 ON", (x0 + 292, y0 + 91), 0.85, "07_INSTRUMENTACAO")

    for x, tag, label in ((205, "X2+", "+"), (250, "X2-", "-"), (295, "X3", "PE")):
        layout.add_blockref("P09_BORNE", (x0 + x, y0 + 38), dxfattribs={"layer": "09_BORNES"})
        centered(layout, tag, (x0 + x, y0 + 49), 1.0, "09_BORNES")
        centered(layout, label, (x0 + x, y0 + 26), 1.5, "09_BORNES")
    centered(layout, "SAÍDA FLUTUANTE", (x0 + 227.5, y0 + 12), 1.05, "09_BORNES")
    centered(layout, "CHASSI", (x0 + 295, y0 + 12), 1.05, "06_COMANDO")

    dimension_h(layout, x0, x0 + width, y0 - 6, "320 mm")
    dimension_v(layout, x0 - 7, y0, y0 + height, "150 mm")
    centered(layout, "ORIGEM DOS RECORTES: CANTO INFERIOR ESQUERDO | ESPESSURA PROPOSTA: 3 mm", (205, 96.5), 1.05, "03_COTAS")


def draw_internal_layout(layout, data: dict[str, list[dict[str, str]]]) -> None:
    # Planta superior em escala gráfica aproximada de 0,62; cotas indicam valores reais.
    x0, y0, scale = 20.0, 100.0, 0.62
    width, depth = 320 * scale, 260 * scale
    add_rect(layout, x0, y0, x0 + width, y0 + depth, "11_ARQUITETURA")
    centered(layout, "FRENTE", (x0 + width / 2, y0 + 11), 1.2, "11_ARQUITETURA")
    centered(layout, "TRASEIRA", (x0 + width - 25, y0 + depth - 5), 1.2, "11_ARQUITETURA")
    line(layout, (x0 + 78, y0), (x0 + 78, y0 + depth), "11_ARQUITETURA")
    centered(layout, "ZONA PRIMÁRIA", (x0 + 39, y0 + 158.5), 1.05, "11_ARQUITETURA")
    centered(layout, "COBERTA", (x0 + 39, y0 + 155.5), 1.05, "11_ARQUITETURA")

    component(layout, x0 + 8, y0 + 132, x0 + 35, y0 + 153, "X1/F1/S1", "ENTRADA", "04_EQUIPAMENTOS")
    component(layout, x0 + 42, y0 + 125, x0 + 70, y0 + 153, "FL1", "FILTRO", "04_EQUIPAMENTOS")
    component(layout, x0 + 10, y0 + 58, x0 + 70, y0 + 115, "PS1", "36 V / 7 A", "04_EQUIPAMENTOS")
    centered(layout, "PE1", (x0 + 18, y0 + 122), 1.0, "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (x0 + 18, y0 + 117), dxfattribs={"layer": "06_COMANDO"})

    component(layout, x0 + 91, y0 + 62, x0 + 150, y0 + 118, "REG1", "BUCK / DISSIPADOR", "04_EQUIPAMENTOS")
    component(layout, x0 + 91, y0 + 124, x0 + 130, y0 + 151, "PS2", "12 V", "04_EQUIPAMENTOS")
    component(layout, x0 + 92, y0 + 13, x0 + 152, y0 + 48, "CTRL/M1", "SINAIS / KELVIN", "07_INSTRUMENTACAO")
    layout.add_blockref("P09_FAN", (x0 + 177, y0 + 132), dxfattribs={"layer": "10_ELETROCALHAS", "xscale": 1.25, "yscale": 1.25})
    centered(layout, "FAN1 80 mm", (x0 + 177, y0 + 110), 1.0, "10_ELETROCALHAS")

    orthogonal(layout, ((x0 + 35, y0 + 143), (x0 + 42, y0 + 143), (x0 + 42, y0 + 115)), "05_POTENCIA")
    orthogonal(layout, ((x0 + 70, y0 + 85), (x0 + 82, y0 + 85), (x0 + 82, y0 + 90), (x0 + 91, y0 + 90)), "08_CABOS")
    orthogonal(layout, ((x0 + 150, y0 + 90), (x0 + 168, y0 + 90), (x0 + 168, y0 + 30), (x0 + 152, y0 + 30)), "08_CABOS")
    line(layout, (x0 + 18, y0 + 117), (x0 + 18, y0 + 52), "06_COMANDO")
    line(layout, (x0 + 18, y0 + 52), (x0 + 180, y0 + 52), "06_COMANDO")
    centered(layout, "BARRA PE / CHASSI", (x0 + 55, y0 + 56), 0.9, "06_COMANDO")

    for y in (y0 + 75, y0 + 95):
        arrow(layout, (x0 + 80, y), (x0 + 188, y), "06_COMANDO", "AR", (0, 4))
    centered(layout, "ENTRADA LATERAL COM FILTRO", (x0 + 115, y0 + 158), 0.9, "10_ELETROCALHAS")

    dimension_h(layout, x0, x0 + width, y0 + 4, "320 mm REAL")
    dimension_v(layout, x0 - 5, y0, y0 + depth, "260 mm REAL")

    table(
        layout,
        230,
        252,
        (38, 42, 90),
        ("ZONA", "ITENS", "CRITÉRIO PENDENTE"),
        [
            ("PRIMÁRIA", "X1/F1/S1/FL1", "cobertura, isolação, EMC"),
            ("CONVERSÃO", "PS1", "derating, fixação, PE"),
            ("REGULAÇÃO", "REG1/F2", "dissipador e falha única"),
            ("AUXILIAR", "PS2/CTRL/M1", "ruído e calibração"),
            ("TÉRMICA", "FAN1/TH1/TS1", "pressão, ruído, ensaio"),
            ("FRONTAL", "RV/S2/X2/X3", "alívio e acesso"),
        ],
        row_height=12.0,
        text_height=0.82,
    )
    add_rect(layout, 230, 122, 400, 162, "13_NOTAS")
    centered(layout, "REGRAS DE ROTEAMENTO", (315, 154), 1.2, "13_NOTAS")
    add_mtext(
        layout,
        "Separar rede, potência CC, comando e pares Kelvin; minimizar laços; manter PE curto; impedir contato com pás e dissipadores.",
        (237, 146),
        156,
        1.15,
        "13_NOTAS",
    )
    centered(layout, "LAYOUT CONCEITUAL - NÃO UTILIZAR COMO INSTRUÇÃO DE MONTAGEM", (315, 108), 1.1, "13_NOTAS")


def draw_mechanical_details(layout, data: dict[str, list[dict[str, str]]]) -> None:
    # Painel frontal em escala 1:2.
    fx, fy, sc = 20.0, 174.0, 0.5
    add_rect(layout, fx, fy, fx + 320 * sc, fy + 150 * sc, "11_ARQUITETURA")
    centered(layout, "PAINEL FRONTAL - ESCALA GRÁFICA 1:2", (fx + 80, fy + 81), 1.2, "02_TEXTO")
    for x, y, shape, size, tag in (
        (35, 92, "R", (30, 22), "S1"),
        (105, 100, "R", (72, 36), "M1"),
        (175, 100, "C", (7, 0), "RV1"),
        (220, 100, "C", (7, 0), "RV2"),
        (270, 100, "C", (16, 0), "S2"),
        (205, 38, "C", (8, 0), "X2+"),
        (250, 38, "C", (8, 0), "X2-"),
        (295, 38, "C", (8, 0), "X3"),
    ):
        px, py = fx + x * sc, fy + y * sc
        if shape == "R":
            w, h = size[0] * sc, size[1] * sc
            add_rect(layout, px - w / 2, py - h / 2, px + w / 2, py + h / 2, "03_COTAS")
        else:
            layout.add_circle((px, py), size[0] * sc / 2, dxfattribs={"layer": "03_COTAS"})
        centered(layout, tag, (px, py + 6), 0.8, "02_TEXTO")
    dimension_h(layout, fx, fx + 160, fy + 4, "320 mm")

    # Painel traseiro em escala 1:2.
    rx, ry = 20.0, 101.0
    add_rect(layout, rx, ry, rx + 160, ry + 75, "11_ARQUITETURA")
    centered(layout, "PAINEL TRASEIRO - ESCALA GRÁFICA 1:2", (rx + 80, ry + 68), 1.2, "02_TEXTO")
    add_rect(layout, rx + 15.5, ry + 30, rx + 29.5, ry + 40, "03_COTAS")
    centered(layout, "X1 28x20", (rx + 22.5, ry + 24), 0.9, "02_TEXTO")
    layout.add_circle((rx + 122.5, ry + 37.5), 19, dxfattribs={"layer": "03_COTAS"})
    for dx, dy in ((-17.5, -17.5), (17.5, -17.5), (-17.5, 17.5), (17.5, 17.5)):
        layout.add_circle((rx + 122.5 + dx, ry + 37.5 + dy), 1, dxfattribs={"layer": "03_COTAS"})
    centered(layout, "FAN1 D76 / 4xD4", (rx + 122.5, ry + 12), 0.9, "02_TEXTO")

    # Vista lateral e envelope.
    add_rect(layout, 195, 178, 325, 253, "11_ARQUITETURA")
    centered(layout, "VISTA LATERAL 1:2", (260, 247), 1.2, "02_TEXTO")
    line(layout, (210, 190), (310, 190), "11_ARQUITETURA")
    line(layout, (210, 190), (210, 235), "11_ARQUITETURA")
    line(layout, (310, 190), (310, 235), "11_ARQUITETURA")
    line(layout, (210, 235), (310, 235), "11_ARQUITETURA")
    arrow(layout, (220, 212), (300, 212), "10_ELETROCALHAS", "FLUXO DE AR")
    dimension_h(layout, 210, 310, 184, "260 mm REAL")
    dimension_v(layout, 204, 190, 235, "150 mm REAL")

    table(
        layout,
        195,
        166,
        (35, 40, 45, 85),
        ("ITEM", "X / Y", "RECORTE", "OBSERVAÇÃO"),
        [
            ("S1", "35 / 92", "30x22", "fabricante"),
            ("M1", "105 / 100", "72x36", "moldura"),
            ("RV1/RV2", "175/220 / 100", "D7", "antirotação"),
            ("S2", "270 / 100", "D16", "comando"),
            ("X2+/X2-/X3", "205/250/295 / 38", "D8", "bornes"),
            ("X1", "45 / 70", "28x20", "traseiro"),
            ("FAN1", "245 / 75", "D76 + 4xD4", "traseiro"),
        ],
        row_height=7.5,
        text_height=0.75,
    )
    centered(layout, "SEM TOLERÂNCIAS GERAIS, RAIOS, ACABAMENTO OU PROCESSO DE CORTE", (297, 100), 1.05, "13_NOTAS")


def draw_interconnections(layout, data: dict[str, list[dict[str, str]]]) -> None:
    component(layout, 20, 210, 64, 246, "X1", "L / N / PE", "09_BORNES")
    component(layout, 86, 210, 138, 246, "ENTRADA", "F1/S1/FL1", "04_EQUIPAMENTOS")
    component(layout, 160, 202, 212, 252, "PS1", "36 V / 7 A", "04_EQUIPAMENTOS")
    component(layout, 236, 202, 288, 252, "REG1", "0-30 V / 5 A", "04_EQUIPAMENTOS")
    component(layout, 312, 210, 352, 246, "K1/SH1", "SAÍDA", "04_EQUIPAMENTOS")
    component(layout, 370, 210, 400, 246, "X2", "+ / -", "09_BORNES")
    for start, end, label in (
        ((64, 228), (86, 228), "W01-W06"),
        ((138, 228), (160, 228), "W08-W09"),
        ((212, 228), (236, 228), "W10-W12"),
        ((288, 228), (312, 228), "W13-W16"),
        ((352, 228), (370, 228), "W14/W16"),
    ):
        arrow(layout, start, end, "08_CABOS", label, (0, 6))

    component(layout, 115, 150, 155, 180, "PE1", "CHASSI", "06_COMANDO")
    component(layout, 180, 145, 225, 185, "PS2", "12 V AUX", "04_EQUIPAMENTOS")
    component(layout, 250, 145, 300, 185, "PAINEL", "RV1/RV2/S2/M1", "07_INSTRUMENTACAO")
    layout.add_blockref("P09_FAN", (345, 165), dxfattribs={"layer": "10_ELETROCALHAS", "xscale": 0.8, "yscale": 0.8})
    centered(layout, "FAN1", (345, 149), 0.95, "10_ELETROCALHAS")
    orthogonal(layout, ((42, 210), (42, 165), (115, 165)), "06_COMANDO")
    centered(layout, "W06 PE", (75, 170), 0.9, "06_COMANDO")
    arrow(layout, (155, 165), (180, 165), "06_COMANDO", "W07/W25")
    arrow(layout, (225, 165), (250, 165), "06_COMANDO", "W17-W24")
    arrow(layout, (300, 165), (335, 165), "06_COMANDO", "W19-W21")
    orthogonal(layout, ((275, 185), (275, 194), (382, 194), (382, 210)), "07_INSTRUMENTACAO")
    centered(layout, "W17/W18 SENSE KELVIN", (330, 198), 0.9, "07_INSTRUMENTACAO")

    table(
        layout,
        20,
        140,
        (38, 62, 63, 42, 75, 100),
        ("GRUPO", "ORIGEM", "DESTINO", "SEÇÃO", "IDENTIFICAÇÃO", "FUNÇÃO"),
        [
            ("W01-W05", "X1/F1/S1", "FL1", "0,75", "preto/azul", "rede L/N"),
            ("W06-W07", "X1/PE1", "chassi/PS1", "1,5", "verde-amarelo", "proteção"),
            ("W08-W09", "FL1", "PS1", "0,75", "preto/azul", "rede filtrada"),
            ("W10-W12", "PS1/F2", "REG1", "2,5", "vermelho/preto", "barramento 36 V"),
            ("W13-W16", "REG1/K1/SH1", "X2", "2,5", "vermelho/preto", "saída 0-30 V"),
            ("W17-W18", "X2", "M1", "0,5", "par vermelho/preto", "sense Kelvin"),
            ("W19-W21", "PS2/TH1", "FAN1", "0,5", "vermelho/preto", "ventilação"),
            ("W22-W24", "PS2/TS1/S2", "K1", "0,5", "vermelho/branco", "habilitação"),
            ("W25", "X3", "PE1", "1,5", "verde-amarelo", "borne de chassi"),
        ],
        row_height=3.5,
        text_height=0.68,
    )
    centered(layout, "LISTA COMPLETA W01-W25 EM lista-interligacoes.csv | SEÇÕES EM mm²", (210, 99), 1.05, "13_NOTAS")


DRAWERS = {
    1: draw_block_diagram,
    2: draw_electrical_diagram,
    3: draw_front_panel,
    4: draw_internal_layout,
    5: draw_mechanical_details,
    6: draw_interconnections,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    project = root / PROJECT_SLUG
    data = {
        "parameters": read_rows(project, "parametros.csv"),
        "equipment": read_rows(project, "lista-equipamentos.csv"),
        "protections": read_rows(project, "lista-protecoes.csv"),
        "interconnections": read_rows(project, "lista-interligacoes.csv"),
        "cutouts": read_rows(project, "lista-recortes.csv"),
        "materials": read_rows(project, "lista-materiais.csv"),
        "calculations": read_rows(project, "resultados-calculo.csv"),
    }
    source_dir = project / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        DRAWERS[spec.number](layout, data)
        output = source_dir / spec.filename
        prepare_deterministic_write(doc)
        with output.open("wt", encoding="utf-8", newline="\n") as stream:
            doc.write(stream)
        outputs.append(output)
        print(f"Gerado: {output.relative_to(root)}")
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositório")
    return parser.parse_args()


def main() -> int:
    generate(parse_args().root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
