"""Gera as nove pranchas DXF do Projeto 07 de forma determinística."""

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


PROJECT_SLUG = "07-arquitetura-veiculo-eletrico"
PROJECT_DATE = "2026-11-05"
REVISION = "02"


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
        "01_arquitetura_geral.dxf",
        "ARQUITETURA GERAL DO VEÍCULO ELÉTRICO",
        "EV-07: domínios de energia, controle e comunicação",
        "Setas mostram fluxo funcional, não posição física nem chicote executivo.\\P"
        "Regeneração é conceitual e depende dos limites de INV-701, BMS-701 e bateria.",
        "Vermelho: HV | Azul: LV | Verde: comando/CAN | Ciano: sinais | Tracejado: limite funcional",
    ),
    SheetSpec(
        2,
        "02_circuito_alta_tensao.dxf",
        "CIRCUITO DE ALTA TENSÃO",
        "Bateria 400 Vcc nominal, proteção, pré-carga e distribuição",
        "Polos HV isolados do chassi; carcaças recebem equipotencialização conceitual.\\P"
        "Fusíveis, contatores e cabos exigem coordenação, ensaio e seleção automotiva.",
        "F: fusível | KM: contator | MSD: desconector | IMD: monitor de isolação | PDU: distribuição",
    ),
    SheetSpec(
        3,
        "03_circuito_baixa_tensao.dxf",
        "CIRCUITO DE BAIXA TENSÃO",
        "Bateria auxiliar, CC-CC, controles e cadeia física de habilitação",
        "A bateria de 12 V inicia controles e contatores antes da disponibilidade do CC-CC.\\P"
        "Perda de emergência, HVIL ou colisão remove habilitação; CAN não substitui esse caminho.",
        "LV: baixa tensão | DRV: driver | NF: contato normalmente fechado | ECU: unidade eletrônica",
    ),
    SheetSpec(
        4,
        "04_pre_carga_contatores.dxf",
        "PRÉ-CARGA E CONTATORES",
        "Sequência monitorada por tensão para energização do elo CC",
        "Limiar de 90% e timeout de 1,5 s são propostas acadêmicas.\\P"
        "Falha exige contatores abertos, descarga controlada e novo ciclo de chave.",
        "0: aberto | 1: fechado | VDC: elo CC | VBAT: bateria | tau: constante de tempo RC",
    ),
    SheetSpec(
        5,
        "05_inversor_motor.dxf",
        "INVERSOR E MOTOR DE INDUÇÃO",
        "Estágio trifásico e arquiteturas conceituais V/f e FOC",
        "Os blocos representam funções, não firmware, ganhos ou parâmetros identificados.\\P"
        "Não há curvas, eficiência medida ou resultado experimental atribuído ao TCC.",
        "V/f: controle escalar | FOC: controle vetorial | PWM: modulação | d-q: referencial síncrono",
    ),
    SheetSpec(
        6,
        "06_sensores_controle.dxf",
        "SENSORES E CONTROLE",
        "Aquisição, plausibilidade, limites e reação conceitual a falhas",
        "Faixas, redundâncias e reações são propostas; confirmar requisitos de segurança.\\P"
        "Falha crítica leva a torque zero e bloqueio/abertura HV conforme análise real.",
        "AI: analógico | DI: digital | ISO: isolado | NTC: temperatura | RES: resolver",
    ),
    SheetSpec(
        7,
        "07_rede_comunicacao.dxf",
        "REDE DE COMUNICAÇÃO",
        "CAN-PT linear, gateway de diagnóstico e matriz de mensagens",
        "IDs, períodos e timeouts são premissas de arquitetura, não software validado.\\P"
        "O backbone requer duas terminações e ramais curtos, sujeitos a projeto EMC.",
        "RT: 120 ohm | CAN-H/L: par diferencial | GW: gateway | SOBD: diagnóstico",
    ),
    SheetSpec(
        8,
        "08_layout_componentes.dxf",
        "LAYOUT DOS COMPONENTES",
        "Implantação conceitual em vista superior e segregação de rotas",
        "Envelope, massas, fixações, proteção IP, crash e refrigeração não dimensionados.\\P"
        "Rotas devem ser revistas por isolamento, EMC, abrasão e acesso de serviço.",
        "Laranja/vermelho: HV | Azul: LV | Verde: CAN | Cinza: envelope | CH: chassi",
    ),
    SheetSpec(
        9,
        "09_interfaces_resposta_falhas.dxf",
        "INTERFACES E RESPOSTA CONCEITUAL A FALHAS",
        "Rastreabilidade entre sinais, estados e ações propostas do EV-07",
        "Respostas são propostas didáticas; não definem função de segurança nem desligamento real.\\P"
        "Detecção de contato soldado, diagnóstico, latência e rearme dependem de hardware e análise ainda não definidos.",
        "DI: entrada digital | APPS: pedal do acelerador | BPS: pedal de freio | HV: alta tensão | PWM: modulação",
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
            1.15,
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
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5.0), 1.65, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4.0), 1.05, detail_layer)


def small_component(
    layout,
    center: tuple[float, float],
    width: float,
    height: float,
    tag: str,
    layer: str,
) -> None:
    x, y = center
    add_rect(layout, x - width / 2, y - height / 2, x + width / 2, y + height / 2, layer)
    centered(layout, tag, center, 1.2, layer)


def fuse(layout, point: tuple[float, float], tag: str, *, vertical: bool = False) -> None:
    rotation = 90.0 if vertical else 0.0
    layout.add_blockref("P07_FUSIVEL", point, dxfattribs={"layer": "05_POTENCIA", "rotation": rotation})
    centered(layout, tag, (point[0], point[1] + (9.0 if not vertical else 0.0)), 1.15, "05_POTENCIA")


def contactor(layout, point: tuple[float, float], tag: str, *, vertical: bool = False) -> None:
    rotation = 90.0 if vertical else 0.0
    layout.add_blockref("P07_CONTATOR", point, dxfattribs={"layer": "05_POTENCIA", "rotation": rotation})
    centered(layout, tag, (point[0], point[1] + (9.0 if not vertical else 0.0)), 1.15, "05_POTENCIA")


def chassis(layout, point: tuple[float, float], tag: str = "CHASSI") -> None:
    layout.add_blockref("P07_CHASSI", point, dxfattribs={"layer": "05_POTENCIA"})
    left(layout, tag, (point[0] + 7.0, point[1] - 1.0), 1.05, "05_POTENCIA")


def table(
    layout,
    x: float,
    top: float,
    widths: tuple[float, ...],
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    *,
    row_height: float,
    text_height: float = 1.0,
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


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    fuse_block = doc.blocks.new("P07_FUSIVEL", base_point=(0.0, 0.0))
    line(fuse_block, (-7.0, 0.0), (-4.0, 0.0), "05_POTENCIA")
    add_rect(fuse_block, -4.0, -2.0, 4.0, 2.0, "05_POTENCIA")
    line(fuse_block, (-2.8, -1.3), (2.8, 1.3), "05_POTENCIA")
    line(fuse_block, (4.0, 0.0), (7.0, 0.0), "05_POTENCIA")

    contactor_block = doc.blocks.new("P07_CONTATOR", base_point=(0.0, 0.0))
    line(contactor_block, (-7.0, 0.0), (-2.0, 0.0), "05_POTENCIA")
    line(contactor_block, (-2.0, 0.0), (2.5, 3.0), "05_POTENCIA")
    line(contactor_block, (2.0, 0.0), (7.0, 0.0), "05_POTENCIA")

    chassis_block = doc.blocks.new("P07_CHASSI", base_point=(0.0, 0.0))
    line(chassis_block, (0.0, 4.0), (0.0, 0.0), "05_POTENCIA")
    line(chassis_block, (-5.0, 0.0), (5.0, 0.0), "05_POTENCIA")
    line(chassis_block, (-3.5, -1.6), (3.5, -1.6), "05_POTENCIA")
    line(chassis_block, (-2.0, -3.2), (2.0, -3.2), "05_POTENCIA")

    sensor_block = doc.blocks.new("P07_SENSOR", base_point=(0.0, 0.0))
    sensor_block.add_circle((0.0, 0.0), radius=3.0, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    line(sensor_block, (-2.1, -2.1), (2.1, 2.1), "07_INSTRUMENTACAO")


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("REVISAO VISUAL 02", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.5, "02_TEXTO")


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
        "PRANCHA": f"{spec.number:02d}/09",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/09"
    metadata["PORTFOLIO_EPISTEMIC_STATUS"] = "ACADEMIC_CONCEPT_NO_EXPERIMENTAL_RESULTS"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 3.85, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.85, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_architecture(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "DOMÍNIO DE TRAÇÃO HV - 320 A 450 Vcc (PREMISSA)", (205, 258), 1.45, "05_POTENCIA")
    component(layout, 24, 202, 70, 242, "BAT-HV-701", "400 V / 60 kWh", "05_POTENCIA")
    component(layout, 92, 202, 148, 242, "MSD + F701 + PDU", "CONTATORES / PRÉ-CARGA", "05_POTENCIA")
    component(layout, 171, 202, 221, 242, "INV-701", "CC / CA TRIFÁSICO", "04_EQUIPAMENTOS")
    layout.add_blockref("SIM_MOTOR", (254, 222), dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 3.0, "yscale": 3.0})
    centered(layout, "IM-701", (254, 207), 1.5, "04_EQUIPAMENTOS")
    centered(layout, "60 kW - INDUÇÃO", (254, 202), 1.05, "02_TEXTO")
    component(layout, 292, 202, 340, 242, "REDUÇÃO", "DIFERENCIAL", "11_ARQUITETURA")
    component(layout, 362, 202, 398, 242, "RODAS", "ENERGIA MECÂNICA", "11_ARQUITETURA")
    arrow(layout, (70, 222), (92, 222), "05_POTENCIA", "CC")
    arrow(layout, (148, 222), (171, 222), "05_POTENCIA", "CC")
    arrow(layout, (221, 222), (242, 222), "05_POTENCIA", "U/V/W")
    arrow(layout, (266, 222), (292, 222), "04_EQUIPAMENTOS", "TORQUE")
    arrow(layout, (340, 222), (362, 222), "11_ARQUITETURA")
    centered(layout, "REGENERAÇÃO CONCEITUAL", (196, 193), 1.05, "05_POTENCIA")
    arrow(layout, (250, 190), (126, 190), "05_POTENCIA")

    centered(layout, "DOMÍNIO AUXILIAR E CONTROLE - 12/14 Vcc", (200, 179), 1.45, "06_COMANDO")
    component(layout, 24, 132, 66, 166, "BAT-LV-701", "12 V / 40 Ah", "06_COMANDO")
    component(layout, 84, 132, 126, 166, "DCDC-701", "400 / 14 V - 3 kW", "04_EQUIPAMENTOS")
    component(layout, 144, 132, 186, 166, "PDU-LV-701", "FUSÍVEIS LV", "06_COMANDO")
    component(layout, 204, 132, 246, 166, "VCU-701", "ESTADOS / TORQUE", "06_COMANDO")
    component(layout, 264, 132, 306, 166, "BMS-701", "PACK / LIMITES", "06_COMANDO")
    component(layout, 324, 132, 366, 166, "SENSORES", "PEDAIS / T / I / V", "07_INSTRUMENTACAO")
    arrow(layout, (66, 149), (84, 149), "06_COMANDO")
    arrow(layout, (126, 149), (144, 149), "06_COMANDO")
    arrow(layout, (186, 149), (204, 149), "06_COMANDO")
    arrow(layout, (246, 149), (264, 149), "06_COMANDO", "CAN")
    arrow(layout, (366, 149), (306, 149), "07_INSTRUMENTACAO")
    orthogonal(layout, ((105, 166), (105, 181), (120, 181), (120, 202)), "05_POTENCIA")
    centered(layout, "HV -> LV", (105, 174), 1.05, "05_POTENCIA")
    orthogonal(layout, ((225, 166), (225, 184), (196, 184), (196, 202)), "06_COMANDO")
    centered(layout, "ENABLE / TORQUE", (233, 184), 1.0, "06_COMANDO")
    line(layout, (42, 113), (382, 113), "06_COMANDO")
    centered(layout, "CAN-PT 500 kbit/s (PROPOSTA) | BMS - VCU - INVERSOR - CC-CC", (212, 119), 1.25, "06_COMANDO")
    for x in (105, 225, 285):
        line(layout, (x, 132), (x, 113), "06_COMANDO")
    centered(layout, "FATO: funções gerais | PREMISSA: valores | PROPOSTA: topologia EV-07 | RESULTADO EXPERIMENTAL: NENHUM", (210, 103), 1.15, "13_NOTAS")


def draw_hv(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "BARRAMENTO HV ISOLADO DO CHASSI", (210, 258), 1.55, "05_POTENCIA")
    component(layout, 20, 166, 62, 240, "BAT-HV-701", "320-450 Vcc", "05_POTENCIA")
    centered(layout, "+", (58, 226), 2.0, "05_POTENCIA")
    centered(layout, "-", (58, 180), 2.0, "05_POTENCIA")
    line(layout, (62, 226), (385, 226), "05_POTENCIA")
    line(layout, (62, 180), (385, 180), "05_POTENCIA")
    fuse(layout, (84, 226), "MSD-701")
    fuse(layout, (111, 226), "F701 250 A")
    contactor(layout, (157, 226), "KMP-701")
    contactor(layout, (131, 180), "KMN-701")

    orthogonal(layout, ((139, 226), (139, 206), (174, 206), (174, 226)), "05_POTENCIA")
    contactor(layout, (150, 206), "KPR-701")
    add_rect(layout, 158, 202, 168, 210, "05_POTENCIA")
    centered(layout, "RPR", (163, 206), 1.0, "05_POTENCIA")
    centered(layout, "100 ohm", (163, 197), 1.0, "02_TEXTO")

    component(layout, 194, 199, 232, 237, "PDU-HV-701", "DISTRIBUIÇÃO", "05_POTENCIA")
    line(layout, (194, 226), (174, 226), "05_POTENCIA")
    line(layout, (194, 180), (232, 180), "05_POTENCIA")
    line(layout, (213, 199), (213, 180), "05_POTENCIA")
    fuse(layout, (254, 226), "F711")
    component(layout, 273, 199, 317, 237, "INV-701", "ELO CC + PWM", "04_EQUIPAMENTOS")
    line(layout, (232, 226), (273, 226), "05_POTENCIA")
    line(layout, (273, 180), (295, 180), "05_POTENCIA")
    line(layout, (295, 180), (295, 199), "05_POTENCIA")
    layout.add_blockref("SIM_MOTOR", (361, 218), dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 2.6, "yscale": 2.6})
    centered(layout, "IM-701", (361, 204), 1.4, "04_EQUIPAMENTOS")
    for y in (224, 218, 212):
        line(layout, (317, y), (349, y), "08_CABOS")
    centered(layout, "WHV05 U/V/W", (333, 233), 1.05, "08_CABOS")

    fuse(layout, (254, 154), "F712 15 A")
    component(layout, 273, 136, 317, 170, "DCDC-701", "400 / 14 Vcc", "04_EQUIPAMENTOS")
    orthogonal(layout, ((232, 226), (239, 226), (239, 154), (247, 154)), "05_POTENCIA")
    orthogonal(layout, ((213, 180), (239, 180), (239, 145), (273, 145)), "05_POTENCIA")
    centered(layout, "SAÍDA LV", (332, 153), 1.1, "06_COMANDO")
    arrow(layout, (317, 153), (351, 153), "06_COMANDO", "14 V")

    component(layout, 95, 115, 142, 145, "BMS-701", "CÉLULAS / I / T", "06_COMANDO")
    component(layout, 174, 115, 221, 145, "IMD-701", "ISOLAÇÃO HV-CH", "07_INSTRUMENTACAO")
    orthogonal(layout, ((118, 145), (118, 161), (42, 161), (42, 166)), "07_INSTRUMENTACAO")
    orthogonal(layout, ((197, 145), (197, 158), (250, 158), (250, 180)), "07_INSTRUMENTACAO")
    chassis(layout, (197, 106))
    line(layout, (197, 115), (197, 110), "05_POTENCIA")
    centered(layout, "CARCAÇAS -> CHASSI | POLOS HV NÃO ATERRADOS", (300, 108), 1.15, "13_NOTAS")


def draw_lv(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "BARRAMENTO AUXILIAR 12/14 Vcc", (210, 258), 1.55, "06_COMANDO")
    component(layout, 20, 211, 62, 246, "BAT-LV-701", "12 V / 40 Ah", "06_COMANDO")
    fuse(layout, (80, 228), "F721 80 A")
    component(layout, 99, 211, 143, 246, "PDU-LV-701", "DISTRIBUIÇÃO LV", "06_COMANDO")
    line(layout, (62, 228), (73, 228), "06_COMANDO")
    line(layout, (87, 228), (99, 228), "06_COMANDO")
    line(layout, (143, 228), (395, 228), "06_COMANDO")
    component(layout, 161, 238, 199, 262, "DCDC-701", "14 V / 3 kW", "04_EQUIPAMENTOS")
    line(layout, (180, 238), (180, 228), "06_COMANDO")
    line(layout, (180, 262), (180, 266), "05_POTENCIA")
    centered(layout, "ENTRADA HV", (180, 267.5), 0.9, "05_POTENCIA")

    branches = (
        (172, "F731", "BMS-701", "PACK / HV"),
        (228, "F732", "VCU-701", "ESTADOS / TORQUE"),
        (284, "F733", "CTRL-INV", "PWM / FOC"),
        (340, "F734", "IMD-701", "ISOLAÇÃO"),
        (389, "F735", "SENSORES", "5 V / SINAIS"),
    )
    for x, fuse_tag, tag, detail in branches:
        line(layout, (x, 228), (x, 204), "06_COMANDO")
        fuse(layout, (x, 198), fuse_tag, vertical=True)
        component(layout, x - 20, 151, x + 20, 188, tag, detail, "06_COMANDO")

    add_rect(layout, 20, 105, 395, 137, "13_NOTAS")
    centered(layout, "CADEIA FÍSICA DE HABILITAÇÃO DOS DRIVERS", (207, 132), 1.45, "13_NOTAS")
    items = ((45, "SDE-701", "NF"), (105, "HVIL-701", "NF"), (165, "CRASH-701", "OK"), (225, "BMS-HV-OK", "OK"), (285, "VCU-REQ", "OK"))
    previous_right = 27.0
    for x, tag, state in items:
        line(layout, (previous_right, 117), (x - 17, 117), "06_COMANDO")
        small_component(layout, (x, 117), 34, 12, tag, "06_COMANDO")
        centered(layout, state, (x, 107.5), 0.95, "02_TEXTO")
        previous_right = x + 17
    arrow(layout, (previous_right, 117), (374, 117), "06_COMANDO")
    small_component(layout, (383, 117), 18, 14, "DRV-KM", "06_COMANDO")


def draw_precharge(layout, data: dict[str, list[dict[str, str]]]) -> None:
    add_rect(layout, 18, 106, 198, 260, "12_LEGENDA")
    centered(layout, "CIRCUITO DE POTÊNCIA", (108, 253), 1.55, "12_LEGENDA")
    centered(layout, "VBAT+", (31, 232), 1.15, "05_POTENCIA")
    line(layout, (42, 232), (183, 232), "05_POTENCIA")
    contactor(layout, (95, 232), "KMP-701")
    orthogonal(layout, ((73, 232), (73, 207), (119, 207), (119, 232)), "05_POTENCIA")
    contactor(layout, (85, 207), "KPR-701")
    add_rect(layout, 98, 203, 112, 211, "05_POTENCIA")
    centered(layout, "RPR", (105, 207), 1.0, "05_POTENCIA")
    centered(layout, "100 ohm", (105, 198), 1.0, "02_TEXTO")
    line(layout, (183, 232), (183, 167), "05_POTENCIA")
    add_rect(layout, 176, 151, 190, 167, "05_POTENCIA")
    centered(layout, "C", (183, 159), 1.8, "05_POTENCIA")
    centered(layout, "2200 uF", (159, 159), 1.05, "02_TEXTO")
    line(layout, (42, 143), (183, 143), "05_POTENCIA")
    contactor(layout, (95, 143), "KMN-701")
    line(layout, (183, 151), (183, 143), "05_POTENCIA")
    centered(layout, "VBAT-", (31, 143), 1.15, "05_POTENCIA")
    centered(layout, "VDC/VBAT MEDIDO - NÃO SOMENTE TEMPO", (108, 127), 1.15, "07_INSTRUMENTACAO")
    centered(layout, "tau=0,22 s | t90 ideal=0,506569 s | timeout proposto=1,5 s", (108, 115), 1.05, "02_TEXTO")

    centered(layout, "MÁQUINA DE ESTADOS PROPOSTA", (301, 257), 1.55, "06_COMANDO")
    rows = [
        ("OFF", "0", "0", "0", "AGUARDAR CHAVE"),
        ("CHECK", "0", "0", "0", "VALIDAR PERMISSIVOS"),
        ("PRECHARGE", "1", "0", "1", "VDC/VBAT < 90%"),
        ("READY", "1", "1", "0", "VDC/VBAT >= 90%"),
        ("FAULT", "0", "0", "0", "NOVO CICLO"),
    ]
    table(layout, 207, 247, (44, 25, 25, 25, 73), ("ESTADO", "KMN", "KMP", "KPR", "CONDIÇÃO"), rows, row_height=13.0, text_height=1.05)

    add_rect(layout, 207, 108, 399, 165, "13_NOTAS")
    centered(layout, "PERMISSIVOS PARA ENTRAR EM PRECHARGE", (303, 158), 1.35, "13_NOTAS")
    permissives = ("12 V OK", "BMS OK", "HVIL FECHADO", "ISOLAÇÃO OK", "SEM EMERGÊNCIA", "SEM COLISÃO")
    for index, value in enumerate(permissives):
        x = 226 + (index % 3) * 58
        y = 142 - (index // 3) * 22
        small_component(layout, (x, y), 47, 13, value, "06_COMANDO")
    centered(layout, "QUALQUER FALHA -> FAULT / CONTATORES ABERTOS / TORQUE ZERO", (303, 109.5), 1.05, "13_NOTAS")


def draw_inverter_motor(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "ESTÁGIO DE POTÊNCIA CONCEITUAL", (210, 258), 1.5, "05_POTENCIA")
    centered(layout, "DC+", (25, 235), 1.2, "05_POTENCIA")
    centered(layout, "DC-", (25, 203), 1.2, "05_POTENCIA")
    line(layout, (36, 235), (190, 235), "05_POTENCIA")
    line(layout, (36, 203), (190, 203), "05_POTENCIA")
    add_rect(layout, 43, 207, 62, 231, "05_POTENCIA")
    centered(layout, "ELO CC", (52.5, 224), 1.2, "05_POTENCIA")
    centered(layout, "C=2200 uF", (52.5, 213), 0.95, "02_TEXTO")
    component(layout, 82, 207, 150, 231, "PONTE TRIFÁSICA", "6 CHAVES / PWM", "05_POTENCIA")
    line(layout, (116, 235), (116, 231), "05_POTENCIA")
    line(layout, (116, 207), (116, 203), "05_POTENCIA")
    for y, phase in ((228, "U"), (219, "V"), (210, "W")):
        line(layout, (150, y), (216, y), "08_CABOS")
        centered(layout, phase, (180, y + 2.7), 1.05, "08_CABOS")
    layout.add_blockref("SIM_MOTOR", (235, 219), dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 3.0, "yscale": 3.0})
    centered(layout, "IM-701 / 60 kW", (235, 202), 1.35, "04_EQUIPAMENTOS")
    component(layout, 278, 202, 397, 238, "MEDIÇÕES", "IU IV IW / VDC / RES / T", "07_INSTRUMENTACAO")
    arrow(layout, (262, 219), (278, 219), "07_INSTRUMENTACAO")

    add_rect(layout, 18, 106, 196, 190, "12_LEGENDA")
    centered(layout, "CADEIA V/f - ESCALAR", (107, 183), 1.55, "12_LEGENDA")
    vf_blocks = ((36, "REQ. VELOC."), (75, "RAMPA f*"), (114, "LEI V/f"), (153, "ÂNGULO / PWM"))
    for x, label in vf_blocks:
        small_component(layout, (x, 152), 31, 19, label, "06_COMANDO")
    for start, end in zip(vf_blocks, vf_blocks[1:]):
        arrow(layout, (start[0] + 16, 152), (end[0] - 16, 152), "06_COMANDO")
    centered(layout, "V/f aproximadamente constante até a frequência-base", (107, 126), 1.1, "02_TEXTO")
    centered(layout, "Fluxo e torque permanecem acoplados", (107, 116), 1.1, "13_NOTAS")

    add_rect(layout, 204, 106, 402, 190, "12_LEGENDA")
    centered(layout, "CADEIA FOC - VETORIAL", (303, 183), 1.55, "12_LEGENDA")
    small_component(layout, (248, 160), 45, 16, "FLUXO* -> id*", "06_COMANDO")
    small_component(layout, (330, 160), 49, 16, "TORQUE* -> iq*", "06_COMANDO")
    foc_bottom = ((221, "Ia Ib Ic / RES"), (263, "CLARKE/PARK"), (305, "PI id / iq"), (347, "PARK^-1"), (385, "SVPWM"))
    widths = (34, 34, 34, 34, 28)
    for (x, label), width in zip(foc_bottom, widths):
        small_component(layout, (x, 127), width, 16, label, "07_INSTRUMENTACAO")
    for ((start, _), start_width), ((end, _), end_width) in zip(zip(foc_bottom, widths), zip(foc_bottom[1:], widths[1:])):
        arrow(layout, (start + start_width / 2, 127), (end - end_width / 2, 127), "07_INSTRUMENTACAO")
    arrow(layout, (248, 152), (296, 136), "06_COMANDO")
    arrow(layout, (330, 152), (314, 136), "06_COMANDO")
    centered(layout, "Fluxo d e torque q desacoplados no modelo", (303, 109.5), 1.05, "13_NOTAS")


def draw_sensors(layout, data: dict[str, list[dict[str, str]]]) -> None:
    component(layout, 173, 204, 247, 247, "VCU-701", "PLAUSIBILIDADE / ESTADOS", "06_COMANDO")
    component(layout, 173, 143, 247, 186, "CTRL-INV", "V/f OU FOC / PWM", "06_COMANDO")
    component(layout, 173, 101, 247, 129, "BMS-701", "PACK / LIMITES HV", "06_COMANDO")
    centered(layout, "ENTRADAS DO CONDUTOR E SEGURANÇA", (88, 258), 1.4, "07_INSTRUMENTACAO")
    left_nodes = (
        (34, 235, "APPS1/2", "2 CANAIS OPOSTOS", 210),
        (34, 205, "BPS1/2", "FREIO / PLAUS.", 210),
        (34, 175, "SDE-701", "EMERGÊNCIA NF", 210),
        (34, 145, "CRASH-701", "SINAL COLISÃO", 210),
        (34, 115, "HVIL-701", "LAÇO FECHADO", 210),
    )
    line(layout, (155, 115), (155, 235), "07_INSTRUMENTACAO")
    for x, y, tag, detail, target_x in left_nodes:
        layout.add_blockref("P07_SENSOR", (x, y), dxfattribs={"layer": "07_INSTRUMENTACAO"})
        left(layout, tag, (42, y + 2), 1.15, "07_INSTRUMENTACAO")
        left(layout, detail, (42, y - 3), 0.95, "02_TEXTO")
        line(layout, (112, y), (155, y), "07_INSTRUMENTACAO")
    arrow(layout, (155, 220), (173, 220), "07_INSTRUMENTACAO")

    centered(layout, "REALIMENTAÇÕES DE TRAÇÃO E TÉRMICAS", (326, 258), 1.4, "07_INSTRUMENTACAO")
    right_nodes = (
        (386, 235, "IU / IV / IW", "CORRENTES FASE", 165),
        (386, 207, "SEN-VDC", "TENSÃO ELO CC", 165),
        (386, 179, "RES-701", "POSIÇÃO / RPM", 165),
        (386, 151, "TMOT / TINV", "TEMPERATURAS", 165),
        (386, 117, "VBAT / IDC / TBAT", "PACK HV", 115),
    )
    line(layout, (265, 151), (265, 235), "07_INSTRUMENTACAO")
    for x, y, tag, detail, target_y in right_nodes:
        layout.add_blockref("P07_SENSOR", (x, y), dxfattribs={"layer": "07_INSTRUMENTACAO"})
        centered(layout, tag, (350, y + 2), 1.1, "07_INSTRUMENTACAO")
        centered(layout, detail, (350, y - 3), 0.95, "02_TEXTO")
        if target_y == 165:
            line(layout, (337, y), (265, y), "07_INSTRUMENTACAO")
        else:
            arrow(layout, (337, y), (247, 115), "07_INSTRUMENTACAO")
    arrow(layout, (265, 165), (247, 165), "07_INSTRUMENTACAO")

    arrow(layout, (210, 204), (210, 186), "06_COMANDO", "TORQUE / ENABLE", (22, 0))
    arrow(layout, (210, 143), (210, 129), "06_COMANDO", "STATUS", (18, 0))
    centered(layout, "REAÇÃO PADRÃO PROPOSTA: SINAL CRÍTICO INVÁLIDO -> TORQUE ZERO / BLOQUEIO READY", (210, 97), 1.05, "13_NOTAS")


def draw_network(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "CAN-PT 500 kbit/s - BARRAMENTO LINEAR PROPOSTO", (210, 258), 1.5, "06_COMANDO")
    line(layout, (42, 220), (378, 220), "06_COMANDO")
    small_component(layout, (31, 220), 20, 18, "120 ohm", "06_COMANDO")
    small_component(layout, (389, 220), 20, 18, "120 ohm", "06_COMANDO")
    nodes = ((70, "BMS-701", "PACK"), (145, "VCU-701", "MESTRE ESTADOS"), (225, "INV-701", "TRAÇÃO"), (300, "DCDC-701", "ENERGIA LV"), (355, "GW-701", "GATEWAY"))
    for x, tag, detail in nodes:
        line(layout, (x, 220), (x, 204), "06_COMANDO")
        component(layout, x - 24, 169, x + 24, 204, tag, detail, "06_COMANDO")
    centered(layout, "RAMAL CURTO", (272, 211), 0.95, "02_TEXTO")
    centered(layout, "CAN-H / CAN-L + REFERÊNCIA", (210, 231), 1.1, "08_CABOS")

    line(layout, (280, 148), (389, 148), "06_COMANDO")
    line(layout, (355, 169), (355, 148), "06_COMANDO")
    component(layout, 285, 124, 333, 158, "CAN-DIAG", "REDE SERVIÇO", "06_COMANDO")
    component(layout, 350, 124, 398, 158, "SOBD-701", "CONECTOR", "09_BORNES")
    arrow(layout, (333, 141), (350, 141), "06_COMANDO")

    can_rows = data["can"][:5]
    rows = [(row["id_can_assumido"], row["mensagem"], row["periodo_ms_assumido"], row["timeout_ms_assumido"], row["acao_timeout"][:25]) for row in can_rows]
    table(layout, 18, 153, (24, 68, 24, 26, 108), ("ID", "MENSAGEM", "ms", "TO ms", "AÇÃO TIMEOUT"), rows, row_height=8.5, text_height=0.85)
    centered(layout, "IDs, períodos e ações são PROPOSTAS; validar carga de barramento, prioridades, E2E e diagnóstico.", (210, 98.5), 1.05, "13_NOTAS")


def draw_layout(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "VISTA SUPERIOR CONCEITUAL - FRENTE À DIREITA", (205, 258), 1.45, "11_ARQUITETURA")
    outline = [(35, 127), (45, 116), (275, 116), (302, 137), (302, 225), (275, 246), (45, 246), (35, 235)]
    layout.add_lwpolyline(outline, close=True, dxfattribs={"layer": "11_ARQUITETURA"})
    for x in (73, 258):
        layout.add_circle((x, 120), 10, dxfattribs={"layer": "11_ARQUITETURA"})
        layout.add_circle((x, 242), 10, dxfattribs={"layer": "11_ARQUITETURA"})
    centered(layout, "TRASEIRA", (52, 181), 1.1, "11_ARQUITETURA")
    centered(layout, "FRENTE", (286, 181), 1.1, "11_ARQUITETURA")

    component(layout, 95, 145, 215, 191, "BAT-HV-701", "PACK SOB O ASSOALHO", "05_POTENCIA")
    component(layout, 50, 158, 87, 190, "PDU-HV", "CONTATORES", "05_POTENCIA")
    component(layout, 228, 158, 267, 194, "INV-701", "TRAÇÃO", "04_EQUIPAMENTOS")
    layout.add_blockref("SIM_MOTOR", (284, 175), dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 2.4, "yscale": 2.4})
    centered(layout, "IM-701", (284, 160), 1.2, "04_EQUIPAMENTOS")
    component(layout, 220, 204, 257, 233, "DCDC", "400/14 V", "04_EQUIPAMENTOS")
    component(layout, 263, 204, 294, 233, "BAT-LV", "12 V", "06_COMANDO")
    component(layout, 166, 204, 206, 233, "VCU-701", "CONTROLE", "06_COMANDO")
    component(layout, 112, 201, 152, 230, "BMS-701", "PACK", "06_COMANDO")

    orthogonal(layout, ((70, 175), (95, 175), (215, 175), (228, 175), (272, 175)), "05_POTENCIA")
    centered(layout, "ROTA HV LARANJA", (163, 182), 1.0, "05_POTENCIA")
    orthogonal(layout, ((279, 219), (238, 219), (186, 219), (132, 219)), "06_COMANDO")
    centered(layout, "LV 12/14 V", (236, 225), 0.95, "06_COMANDO")
    orthogonal(layout, ((132, 208), (186, 208), (247, 208), (247, 194)), "07_INSTRUMENTACAO")
    centered(layout, "CAN-PT", (187, 212), 0.95, "07_INSTRUMENTACAO")
    chassis(layout, (156, 132), "CHASSI / EQUIPOTENCIAL")

    add_rect(layout, 318, 112, 402, 248, "12_LEGENDA")
    centered(layout, "CRITÉRIOS DE IMPLANTAÇÃO", (360, 240), 1.35, "12_LEGENDA")
    criteria = (
        "Pack em zona protegida",
        "MSD acessível p/ serviço",
        "HV afastado de LV/CAN",
        "Cabos HV em laranja",
        "Inversor próximo ao motor",
        "Rotas sem arestas/abrasão",
        "Conectores no HVIL",
        "Carcaças ao chassi",
        "Refrigeração não modelada",
        "Crash e IP não validados",
    )
    for index, value in enumerate(criteria):
        left(layout, f"{index + 1}. {value}", (325, 226 - index * 10.7), 1.0, "02_TEXTO")


def draw_fault_interfaces(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "MATRIZ DE FALHAS E INTERFACES PROPOSTAS", (210, 258), 1.45, "06_COMANDO")
    centered(
        layout,
        "Rastreabilidade entre evento, detecção, reação, estado e dado ainda necessário",
        (210, 252),
        1.15,
        "02_TEXTO",
    )
    rows = [
        (
            row["evento"],
            row["entrada_deteccao"],
            row["reacao_proposta"],
            row["estado_resultante"],
            row["lacuna_validacao"],
        )
        for row in data["faults"]
    ]
    table(
        layout,
        20,
        246,
        (66, 62, 92, 46, 112),
        ("EVENTO", "DETECCAO", "REACAO CONCEITUAL", "ESTADO", "PENDENCIA REAL"),
        rows,
        row_height=10.0,
        text_height=1.2,
    )
    add_rect(layout, 20, 102, 400, 128, "13_NOTAS")
    centered(layout, "INTERPRETACAO E LIMITE", (210, 122), 1.2, "13_NOTAS")
    centered(
        layout,
        "A matriz nao e HARA, FMEA, ASIL, validacao de software ou prova de desligamento seguro.",
        (210, 115),
        1.05,
        "02_TEXTO",
    )
    centered(
        layout,
        "Confirmar limiares, tempos, diagnosticos, independencia, resposta e rearme com hardware escolhido.",
        (210, 108.5),
        1.0,
        "02_TEXTO",
    )


DRAWERS = {
    1: draw_architecture,
    2: draw_hv,
    3: draw_lv,
    4: draw_precharge,
    5: draw_inverter_motor,
    6: draw_sensors,
    7: draw_network,
    8: draw_layout,
    9: draw_fault_interfaces,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    project = root / PROJECT_SLUG
    data = {
        "parameters": read_rows(project, "parametros.csv"),
        "signals": read_rows(project, "lista-sinais.csv"),
        "can": read_rows(project, "rede-can.csv"),
        "faults": read_rows(project, "matriz-interfaces-falhas.csv"),
        "cables": read_rows(project, "lista-cabos.csv"),
        "materials": read_rows(project, "lista-materiais.csv"),
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
