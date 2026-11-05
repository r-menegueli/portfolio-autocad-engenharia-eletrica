"""Gera as dez pranchas DXF do Projeto 09 de forma determinística."""

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
PROJECT_DATE = "2026-11-05"
REVISION = "04"
SHEET_COUNT = 10


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
        "Fonte acadêmica: 0,8-30 Vcc regulados / 0-5 A / 150 W",
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
        "K1 isolado não prova tensão zero; o estudo paramétrico de descarga está na prancha 09.",
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
        "A lista W01-W31 define intenção de ligação, não chicote liberado.\\P"
        "Confirmar terminais, crimpagem, torque, isolação, cores, proteção e alívio mecânico.",
        "Preto/azul: L/N | Verde-amarelo: PE | Vermelho/preto: CC | Branco: comando",
    ),
    SheetSpec(
        7,
        "07_topologia_regulador_cc_cv.dxf",
        "TOPOLOGIA DO REGULADOR CC/CV",
        "REG1 síncrono com U1 LM5190 como candidato de arquitetura",
        "U1 regula de 0,8 a 30 V. K1 aberto desabilita a entrega de potência; sem descarga dedicada, a tensão residual nos bornes não é garantida.\\P"
        "Prancha 09 estuda os nós de descarga, sem selecionar valores ou provar estado seguro.\\P"
        "L1, RCS e redes passivas seguem pré-dimensionados; estabilidade, layout e térmica pendentes.",
        "QH/QL: chaves externas | RCS: sensor Kelvin do regulador | SH1: medição externa | 0V36 não ligado ao PE",
    ),
    SheetSpec(
        8,
        "08_predimensionamento_buck.dxf",
        "PRÉ-DIMENSIONAMENTO DO ESTÁGIO BUCK",
        "Ondulação, indutância, corrente de pico e redes de ajuste do conversor",
        "42 V é apenas um cenário paramétrico de sensibilidade, não a tolerância de PS1.\\P"
        "O datasheet usa limiar típico; tolerâncias, resposta transitória, estabilidade e perdas reais pendem de validação.",
        "DELTA IL: ondulação pico a pico | linha tracejada: alvo de 30% | valores acadêmicos, sem liberação para montagem",
    ),
    SheetSpec(
        9,
        "09_descarga_saida_parametrica.dxf",
        "ANÁLISE PARAMÉTRICA DA DESCARGA DA SAÍDA",
        "Nós internos e de borne, energia armazenada e critérios de dimensionamento",
        "C_INT_MAX, C_EXT_MAX, V0_INT_MAX, V0_PORT_MAX, V_SAFE, T_REQ e ratings de pulso: A DEFINIR; RC ideal.\\P"
        "KD2: impedir fechamento com fonte externa conectada; permissivo e intertravamento a validar.\\P"
        "Verificar tolerância, derating, energia de pulso, repetição, temperatura e estados de falha. Não garante 0 V.",
        "V_INT: saída interna do REG1 | V_PORT: bornes X2 | R: resistência | C: capacitância equivalente",
    ),
    SheetSpec(
        10,
        "10_matriz_perdas_termicas_parametrica.dxf",
        "MATRIZ PARAMÉTRICA DE PERDAS E CARGA TÉRMICA",
        "Sensibilidade em POUT = 150 W; eficiências são cenários, não dados de fabricante",
        "A matriz não prevê eficiência real nem temperatura de junção.\\P"
        "Ploss agregado não substitui perdas por componente, curva térmica ou ensaio.\\P"
        "Rtheta admissível, fluxo de ar, derating e limites térmicos seguem sem definição; sem liberação para montagem.",
        "ηPS1: eficiência da fonte isolada | ηREG1: eficiência do buck | PLOSS: potência dissipada",
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


def add_revision_table(layout, spec: SheetSpec) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    description = "DESCARGA PARAMÉTRICA" if spec.number == 9 else "TOPOLOGIA E PRE-DIMENSIONAMENTO"
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), (description, 316), ("R.E.M.M.", 381)):
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
        "PRANCHA": f"{spec.number:02d}/{SHEET_COUNT:02d}",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/{SHEET_COUNT:02d}"
    metadata["PORTFOLIO_EPISTEMIC_STATUS"] = "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 3.85, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.8, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout, spec)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_block_diagram(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "CADEIA PRINCIPAL DE ENERGIA", (205, 258), 1.45, "05_POTENCIA")
    blocks = (
        (18, 210, 57, 240, "X1", "90-264 Vca\nL/N/PE"),
        (67, 210, 111, 240, "F1/S1/FL1", "PROTEÇÃO\nE FILTRO"),
        (121, 202, 171, 248, "PS1", "AC/DC ISOLADA\n36 V / 7 A"),
        (181, 210, 213, 240, "F2", "7,5 A CC"),
        (223, 202, 277, 248, "REG1", "LM5190 CC/CV\n0.8-30 V regulado"),
        (287, 210, 325, 240, "K1/SH1", "HABILITAÇÃO\nE MEDIÇÃO"),
        (343, 202, 400, 248, "X2", "0.8-30 Vcc regulados\n0-5 A / 150 W"),
    )
    for x0, y0, x1, y1, tag, detail in blocks:
        component(layout, x0, y0, x1, y1, tag, detail.replace("\n", " | "), "04_EQUIPAMENTOS")
    for start, end, label in (
        ((57, 225), (67, 225), "REDE"),
        ((111, 225), (121, 225), "L/N"),
        ((171, 225), (181, 225), "36 V"),
        ((213, 225), (223, 225), "36 V"),
        ((277, 225), (287, 225), "0.8-30 V regulados"),
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
    component(layout, 282, 198, 330, 246, "REG1", "U1 LM5190 + QH/QL", "04_EQUIPAMENTOS")
    layout.add_blockref("P09_CHAVE", (348, 232), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "K1 NO", (348, 240), 0.9, "05_POTENCIA")
    component(layout, 362, 204, 380, 220, "SH1", "10 A / 75 mV", "07_INSTRUMENTACAO")
    centered(layout, "X2 +", (394, 232), 1.0, "09_BORNES")
    centered(layout, "X2 -", (394, 212), 1.0, "09_BORNES")
    centered(layout, "0,8-30 V REGULADOS / 0-5 A / 150 W", (335, 190), 1.0, "05_POTENCIA")
    centered(layout, "K1 ABERTO DESABILITA; TENSÃO RESIDUAL NÃO GARANTIDA", (335, 183), 0.95, "02_TEXTO")

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


def draw_regulator_topology(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "REG1 | ESTÁGIO DE POTÊNCIA SÍNCRONO", (210, 258), 1.7, "02_TEXTO")
    add_rect(layout, 24, 153, 308, 244, "11_ARQUITETURA")
    centered(layout, "CAMINHO DE ENERGIA — BARRAMENTO SECUNDÁRIO FLUTUANTE", (166, 237), 1.25, "05_POTENCIA")

    # Power stage: F2 -> half bridge -> L1 -> current-sense resistor -> output.
    centered(layout, "+36 Vcc pós-F2", (48, 230), 1.05, "08_CABOS")
    line(layout, (30, 219), (132, 219), "05_POTENCIA")
    add_rect(layout, 48, 213, 70, 225, "05_POTENCIA")
    centered(layout, "F2", (59, 219), 1.15, "05_POTENCIA")
    centered(layout, "CIN", (91, 197), 1.05, "04_EQUIPAMENTOS")
    line(layout, (91, 219), (91, 190), "05_POTENCIA")
    line(layout, (85, 190), (97, 190), "05_POTENCIA")
    line(layout, (85, 186), (97, 186), "05_POTENCIA")
    line(layout, (91, 186), (91, 161), "05_POTENCIA")

    line(layout, (132, 219), (147, 219), "05_POTENCIA")
    add_rect(layout, 137, 198, 157, 216, "05_POTENCIA")
    centered(layout, "QH", (147, 210), 1.1, "05_POTENCIA")
    centered(layout, "N-MOS", (147, 202), 0.8, "02_TEXTO")
    line(layout, (147, 219), (147, 216), "05_POTENCIA")
    line(layout, (147, 198), (147, 188), "05_POTENCIA")
    add_rect(layout, 137, 164, 157, 182, "05_POTENCIA")
    centered(layout, "QL", (147, 176), 1.1, "05_POTENCIA")
    centered(layout, "N-MOS", (147, 168), 0.8, "02_TEXTO")
    line(layout, (147, 188), (147, 182), "05_POTENCIA")
    line(layout, (147, 164), (147, 161), "05_POTENCIA")
    line(layout, (147, 188), (190, 188), "05_POTENCIA")
    centered(layout, "SW", (173, 192), 0.9, "05_POTENCIA")

    add_rect(layout, 190, 181, 221, 195, "04_EQUIPAMENTOS")
    centered(layout, "L1", (205.5, 191), 1.15, "04_EQUIPAMENTOS")
    centered(layout, "75 uH*", (205.5, 176), 0.9, "02_TEXTO")
    line(layout, (221, 188), (230, 188), "05_POTENCIA")
    add_rect(layout, 230, 181, 256, 195, "07_INSTRUMENTACAO")
    centered(layout, "RCS", (243, 191), 1.0, "07_INSTRUMENTACAO")
    centered(layout, "9.1 mOhm*", (243, 176), 0.85, "02_TEXTO")
    line(layout, (256, 188), (293, 188), "05_POTENCIA")
    centered(layout, "VOUT 0.8-30 V REGULADO", (278, 198), 0.95, "05_POTENCIA")
    centered(layout, "COUT", (296, 178), 0.9, "04_EQUIPAMENTOS")
    line(layout, (274, 188), (274, 170), "05_POTENCIA")
    line(layout, (268, 170), (280, 170), "05_POTENCIA")
    line(layout, (268, 166), (280, 166), "05_POTENCIA")
    line(layout, (274, 166), (274, 161), "05_POTENCIA")
    line(layout, (27, 161), (300, 161), "08_CABOS")
    centered(layout, "0V36 = RETORNO DO BUCK / VOUT-", (75, 156), 0.92, "08_CABOS")
    centered(layout, "K1 aberto desabilita a saída; tensão residual não garantida sem descarga dedicada.", (166, 137), 0.88, "02_TEXTO")
    centered(layout, "Retorno 0V36 flutuante; não se liga ao PE.", (166, 130), 0.88, "02_TEXTO")

    # Controller block and explicit pin-to-function cross-reference.
    add_rect(layout, 314, 205, 410, 242, "04_EQUIPAMENTOS")
    centered(layout, "U1 | LM5190 (CANDIDATO)", (362, 234), 1.25, "04_EQUIPAMENTOS")
    centered(layout, "Buck síncrono | malhas CC e CV", (362, 225), 0.95, "02_TEXTO")
    centered(layout, "QH/QL externos | fSW programável", (362, 217), 0.9, "02_TEXTO")
    centered(layout, "VIN 5-80 V | VOUT 0.8-79 V (datasheet)", (362, 210), 0.78, "02_TEXTO")
    rows = [
        ("HO / LO", "Acionamento dos gates QH / QL", "Pendente"),
        ("ISNS+ / VOUT", "Kelvin nos dois lados de RCS", "Fonte TI"),
        ("FB", "Divisor / ajuste de RV1", "Pendente"),
        ("ISET / IMON", "Ajuste RV2 / leitura de corrente", "Pendente"),
        ("COMP / RT", "Compensação / frequência", "Pendente"),
        ("EN / PGOOD", "Habilitação / estado regulado", "Pendente"),
    ]
    table(layout, 314, 196, (26, 51, 19), ("PINO(S)", "INTERFACE", "ESTADO"), rows, row_height=9, text_height=1.5)


def draw_regulator_predesign(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "ONDULAÇÃO CALCULADA PARA fSW = 100 kHz E L1 = 75 uH", (210, 258), 1.6, "02_TEXTO")
    x0, x1, y0, y1 = 43.0, 195.0, 143.0, 232.0
    line(layout, (x0, y0), (x1, y0), "03_COTAS")
    line(layout, (x0, y0), (x0, y1), "03_COTAS")
    for current in (0.0, 0.4, 0.8, 1.2, 1.6):
        y = y0 + (current / 1.6) * (y1 - y0)
        line(layout, (x0, y), (x1, y), "11_ARQUITETURA")
        centered(layout, f"{current:.1f}", (x0 - 8, y), 0.8, "03_COTAS")
    for voltage in range(0, 31, 5):
        x = x0 + (voltage / 30) * (x1 - x0)
        line(layout, (x, y0 - 2), (x, y0 + 2), "03_COTAS")
        centered(layout, str(voltage), (x, y0 - 7), 0.8, "03_COTAS")
    centered(layout, "VOUT (V)", ((x0 + x1) / 2, y0 - 14), 1.0, "03_COTAS")
    add_text(layout, "DELTA IL p-p (A)", (x0 - 14, (y0 + y1) / 2), 0.9, layer="03_COTAS", rotation=90.0, align=TextEntityAlignment.MIDDLE_CENTER)

    target_y = y0 + (1.5 / 1.6) * (y1 - y0)
    layout.add_lwpolyline([(x0, target_y), (x1, target_y)], dxfattribs={"layer": "03_COTAS", "linetype": "DASHED"})
    centered(layout, "alvo 30% de 5 A = 1.5 A", (117, target_y + 3), 0.8, "03_COTAS")
    for vin, layer in ((36.0, "05_POTENCIA"), (42.0, "08_CABOS")):
        points = []
        for tenth in range(8, 301, 2):
            vout = tenth / 10
            ripple = vout * (1.0 - vout / vin) / (75e-6 * 100_000.0)
            x = x0 + (vout / 30.0) * (x1 - x0)
            y = y0 + (ripple / 1.6) * (y1 - y0)
            points.append((x, y))
        layout.add_lwpolyline(points, dxfattribs={"layer": layer})
    centered(layout, "VIN 36 V nominal", (83, 244), 0.9, "05_POTENCIA")
    centered(layout, "VIN 42 V sensibilidade", (157, 244), 0.9, "08_CABOS")

    rows = [
        ("L requerida @36 V", "60 uH", "DERIVADO"),
        ("L requerida @42 V", "70 uH", "DERIVADO"),
        ("L1 proposta", "75 uH", "PROPOSTA"),
        ("Delta IL max @36 V", "1.20 A / 24%", "DERIVADO"),
        ("Delta IL max @42 V", "1.40 A / 28%", "DERIVADO"),
        ("I pico em 5 A @42 V", "5.70 A", "DERIVADO"),
        ("RCS proposta", "9.1 mOhm / 1%", "PROPOSTA"),
        ("Limite cíclico ideal", "6.59 A pico", "60 mV typ."),
        ("RIMON para 5 A", "8.62 kOhm", "DERIVADO"),
    ]
    table(layout, 218, 238, (58, 56, 55), ("CRITÉRIO", "VALOR", "CLASSE"), rows, row_height=9, text_height=0.78)
    centered(layout, "36 V nominal: ondulação máxima em VOUT = 18 V; 42 V é apenas sensibilidade.", (147, 108), 0.9, "02_TEXTO")


def draw_output_discharge(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "K1 ABRE O POSITIVO; ANALISAR A ENERGIA EM DOIS NÓS", (210, 251), 1.3, "05_POTENCIA")

    # Internal regulator output and external terminals are distinct discharge domains.
    component(layout, 20, 216, 72, 245, "REG1 / COUT", "NÓ INTERNO", "04_EQUIPAMENTOS")
    line(layout, (72, 231), (160, 231), "05_POTENCIA")
    layout.add_blockref("P09_CHAVE", (166, 231), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "K1", (166, 241), 1.0, "05_POTENCIA")
    centered(layout, "K1 ABRE APENAS +", (166, 222), 0.8, "02_TEXTO")
    line(layout, (172, 231), (350, 231), "05_POTENCIA")
    component(layout, 350, 216, 400, 245, "X2", "PORTA + / -", "09_BORNES")
    line(layout, (20, 205), (400, 205), "08_CABOS")
    line(layout, (375, 216), (375, 205), "08_CABOS")
    centered(layout, "0V36 / RETORNO X2-", (210, 199), 0.9, "08_CABOS")

    centered(layout, "V_INT", (91, 237), 0.9, "05_POTENCIA")
    line(layout, (91, 231), (91, 225), "05_POTENCIA")
    line(layout, (85, 225), (97, 225), "05_POTENCIA")
    line(layout, (85, 221), (97, 221), "05_POTENCIA")
    line(layout, (91, 221), (91, 205), "05_POTENCIA")
    centered(layout, "C_INT", (91, 213), 0.8, "04_EQUIPAMENTOS")

    line(layout, (122, 231), (122, 227), "05_POTENCIA")
    add_rect(layout, 111, 221, 133, 227, "06_COMANDO")
    centered(layout, "KD1", (122, 224), 0.78, "06_COMANDO")
    add_rect(layout, 111, 211, 133, 217, "04_EQUIPAMENTOS")
    centered(layout, "RD1", (122, 214), 0.8, "04_EQUIPAMENTOS")
    line(layout, (122, 221), (122, 217), "05_POTENCIA")
    line(layout, (122, 211), (122, 205), "05_POTENCIA")
    centered(layout, "RAMO INTERNO", (122, 201), 0.75, "02_TEXTO")

    centered(layout, "V_PORT", (308, 237), 0.9, "05_POTENCIA")
    line(layout, (308, 231), (308, 225), "05_POTENCIA")
    line(layout, (302, 225), (314, 225), "05_POTENCIA")
    line(layout, (302, 221), (314, 221), "05_POTENCIA")
    line(layout, (308, 221), (308, 205), "05_POTENCIA")
    centered(layout, "C_EXT", (308, 213), 0.8, "04_EQUIPAMENTOS")

    line(layout, (277, 231), (277, 227), "05_POTENCIA")
    add_rect(layout, 266, 221, 288, 227, "06_COMANDO")
    centered(layout, "KD2", (277, 224), 0.78, "06_COMANDO")
    add_rect(layout, 266, 211, 288, 217, "04_EQUIPAMENTOS")
    centered(layout, "RD2", (277, 214), 0.8, "04_EQUIPAMENTOS")
    line(layout, (277, 221), (277, 217), "05_POTENCIA")
    line(layout, (277, 211), (277, 205), "05_POTENCIA")
    centered(layout, "RAMO PORTA", (277, 201), 0.75, "02_TEXTO")

    discharge = {row["calculo"]: row for row in data["discharge"]}
    sizing_rows = [
        (
            "INTERNA",
            "C_INT_MAX",
            discharge["E_INT_MAX"]["formula"],
            f"R_INT_MIN={discharge['R_INT_MIN']['formula']} <= R <= R_INT_MAX={discharge['R_INT_MAX']['formula']}",
        ),
        (
            "PORTA X2",
            "C_EXT_MAX",
            discharge["E_EXT_MAX"]["formula"],
            f"R_PORT_MIN={discharge['R_PORT_MIN']['formula']} <= R <= R_PORT_MAX={discharge['R_PORT_MAX']['formula']}",
        ),
    ]
    table(
        layout,
        20,
        184,
        (36, 45, 100, 199),
        ("RAMO", "C_EQ", "E = 0.5*C*V0*V0", "FAIXA IDEAL DE R: MÍN. PULSO <= R <= MÁX. TEMPO"),
        sizing_rows,
        row_height=9.0,
        text_height=1.25,
    )

    state_rows = [
        ("OPERAR", "K1 fechado", "KD1 aberto", "KD2 aberto; fonte REG1 habilitada"),
        ("DESLIGAR", "REG1 inibido; abrir K1", "Confirmar abertura antes de fechar KD1", "Não descarregar com fonte externa conectada"),
        ("DESCARGA", "K1 aberto", "KD1 fecha; medir V_INT", "KD2 só com porta isolada e permissivo definido"),
        ("VERIFICAR", "K1 aberto", "Medir V_INT <= V_SAFE no tempo requerido", "Medir V_PORT <= V_SAFE no tempo requerido"),
        ("RETORNAR", "Fechar só ao final", "Abrir e confirmar KD1", "Abrir e confirmar KD2 antes de fechar K1"),
    ]
    table(
        layout,
        20,
        145,
        (36, 56, 138, 150),
        ("FASE", "K1", "NÓ INTERNO", "PORTA X2"),
        state_rows,
        row_height=8.0,
        text_height=1.15,
    )


def draw_thermal_sensitivity(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "CENÁRIOS DIDÁTICOS DE EFICIÊNCIA — NÃO REPRESENTAM CURVAS DE COMPONENTES", (210, 251), 1.25, "05_POTENCIA")

    # Cascaded power flow separates losses in the isolated source from losses in the buck.
    component(layout, 28, 218, 124, 241, "PS1", "36 V / 7 A / 252 W nominal", "04_EQUIPAMENTOS")
    component(layout, 162, 218, 258, 241, "REG1", "BUCK CC/CV / 150 W máx.", "04_EQUIPAMENTOS")
    component(layout, 286, 218, 392, 241, "X2 + CARGA", "VOUT × IOUT ≤ 150 W", "09_BORNES")
    arrow(layout, (124, 229), (162, 229), "05_POTENCIA", "PIN REG1")
    arrow(layout, (258, 229), (286, 229), "05_POTENCIA", "POUT")
    centered(layout, "PLOSS PS1 = PIN PS1 − PIN REG1", (88, 212), 0.95, "05_POTENCIA")
    centered(layout, "PLOSS REG1 = PIN REG1 − POUT", (210, 212), 0.95, "05_POTENCIA")
    centered(layout, "CALOR TOTAL = PLOSS PS1 + PLOSS REG1", (338, 212), 0.95, "05_POTENCIA")

    thermal = data["thermal"]
    loss_by_eta = {
        (row["eta_ps1"], row["eta_reg"]): row["p_loss_total_w"]
        for row in thermal
    }
    matrix_rows = []
    for eta_ps1 in ("0.88", "0.92", "0.96"):
        matrix_rows.append((
            f"{float(eta_ps1) * 100:.0f}%",
            *(f"{float(loss_by_eta[(eta_ps1, eta_reg)]):.1f} W" for eta_reg in ("0.85", "0.90", "0.95")),
        ))
    table(
        layout,
        20,
        200,
        (37, 42, 42, 42),
        ("ηPS1 \\ ηREG1", "85%", "90%", "95%"),
        matrix_rows,
        row_height=8.5,
        text_height=1.25,
    )

    case_rows = []
    for label, eta_ps1, eta_reg in (
        ("BAIXA", "0.88", "0.85"),
        ("CENTRAL", "0.92", "0.90"),
        ("ALTA", "0.96", "0.95"),
    ):
        row = next(item for item in thermal if item["eta_ps1"] == eta_ps1 and item["eta_reg"] == eta_reg)
        case_rows.append((
            label,
            f"{float(row['p_reg_in_w']):.1f}",
            f"{float(row['p_loss_reg_w']):.1f}",
            f"{float(row['p_loss_ps1_w']):.1f}",
            f"{float(row['p_loss_total_w']):.1f}",
            f"{float(row['margin_ps1_w']):.1f}",
        ))
    table(
        layout,
        204,
        200,
        (28, 32, 32, 32, 36, 38),
        ("CASO", "PIN REG", "PLOSS REG", "PLOSS PS1", "PLOSS TOTAL", "MARGEM"),
        case_rows,
        row_height=8.5,
        text_height=1.1,
    )
    centered(layout, "P em W | margem = 252 W − potência requerida na saída de PS1", (304, 158), 0.9, "02_TEXTO")

    add_rect(layout, 20, 99, 202, 152, "12_LEGENDA")
    left(layout, "RELAÇÕES DE POTÊNCIA", (24, 146), 1.25, "12_LEGENDA")
    left(layout, "PIN_REG1 = POUT / ηREG1", (25, 139), 1.1)
    left(layout, "PLOSS_REG1 = PIN_REG1 − POUT", (25, 133), 1.1)
    left(layout, "PIN_PS1 = PIN_REG1 / ηPS1", (25, 127), 1.1)
    left(layout, "PLOSS_PS1 = PIN_PS1 − PIN_REG1", (25, 121), 1.1)
    left(layout, "PLOSS_TOTAL = PIN_PS1 − POUT", (25, 115), 1.1)
    left(layout, "RθJA,req ≤ (Tj,proj − Tamb,proj) / PLOSS,componente", (25, 107), 1.0)

    add_rect(layout, 212, 99, 400, 152, "12_LEGENDA")
    left(layout, "DADOS PARA FECHAR A ANÁLISE TÉRMICA", (216, 146), 1.25, "12_LEGENDA")
    left(layout, "• Curvas de perdas de PS1 e REG1 em V/I e temperatura.", (217, 139), 1.0)
    left(layout, "• Perdas individuais em QH/QL, L1, shunt e passivos.", (217, 133), 1.0)
    left(layout, "• Tj de projeto com margem; Tc, Rθ, placa/interface e derating.", (217, 127), 1.0)
    left(layout, "• Ar interno, ambiente, ventilação e posição dos componentes.", (217, 121), 1.0)
    left(layout, "• Ensaios nos extremos de VOUT/IOUT, carga e falhas.", (217, 115), 1.0)
    left(layout, "Perda total não informa a temperatura de cada componente.", (217, 107), 1.0, "13_NOTAS")

def draw_front_panel(layout, data: dict[str, list[dict[str, str]]]) -> None:
    x0, y0, width, height = 45.0, 105.0, 320.0, 150.0
    add_rect(layout, x0, y0, x0 + width, y0 + height, "11_ARQUITETURA")
    centered(layout, "FONTE DE BANCADA 0,8-30 V REGULADOS / 0-5 A", (x0 + width / 2, y0 + height - 12), 1.8, "02_TEXTO")

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
    component(layout, 236, 202, 288, 252, "REG1", "0,8-30 V regulados / 5 A", "04_EQUIPAMENTOS")
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
            ("W13-W16", "REG1/K1/SH1", "X2", "2,5", "vermelho/preto", "0,8-30 V regulados; 5 A / 150 W máx."),
            ("W17-W18", "X2", "M1", "0,5", "par vermelho/preto", "sense Kelvin"),
            ("W19-W21", "PS2/TH1", "FAN1", "0,5", "vermelho/preto", "ventilação"),
            ("W22-W24", "PS2/TS1/S2", "K1", "0,5", "vermelho/branco", "habilitação"),
            ("W25", "X3", "PE1", "1,5", "verde-amarelo", "borne de chassi"),
            ("W26-W28", "REG1 OUT+/RET", "KD1+RD1", "A DEFINIR", "vermelho/preto", "descarga interna parametrizada"),
            ("W29-W31", "X2+/X2-", "KD2+RD2", "A DEFINIR", "vermelho/preto", "bloquear se fonte externa conectada"),
        ],
        row_height=3.2,
        text_height=1.25,
    )
    centered(layout, "LISTA COMPLETA W01-W31 EM lista-interligacoes.csv | SEÇÕES EM mm²", (210, 95), 1.0, "13_NOTAS")


DRAWERS = {
    1: draw_block_diagram,
    2: draw_electrical_diagram,
    3: draw_front_panel,
    4: draw_internal_layout,
    5: draw_mechanical_details,
    6: draw_interconnections,
    7: draw_regulator_topology,
    8: draw_regulator_predesign,
    9: draw_output_discharge,
    10: draw_thermal_sensitivity,
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
        "discharge": read_rows(project, "dimensionamento-descarga.csv"),
        "thermal": read_rows(project, "dimensionamento-termico-parametrico.csv"),
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
