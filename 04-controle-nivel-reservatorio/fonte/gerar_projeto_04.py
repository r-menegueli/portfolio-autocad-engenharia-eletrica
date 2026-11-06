"""Gera as sete pranchas DXF do Projeto 04 de forma determinística."""

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


PROJECT_SLUG = "04-controle-nivel-reservatorio"
PROJECT_DATE = "2026-11-06"
REVISION = "03"


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
        "01_fluxograma_processo.dxf",
        "FLUXOGRAMA DO PROCESSO",
        "Enchimento de TK-101 por P-101; origem a montante não especificada",
        "TK-101: 10 m³ (premissa). Operação normal: 30–80%; SP inicial: 60%.\\P"
        "Origem e equipamento a montante não definidos.\\P"
        "A vazão de consumo é a perturbação principal da malha de nível.",
        "Tubulação: linha grossa | Sinal: linha fina | HV-102: válvula manual (premissa)",
    ),
    SheetSpec(
        2,
        "02_pid_instrumentacao.dxf",
        "P&ID E INSTRUMENTAÇÃO",
        "Identificação funcional dos instrumentos e sinais da malha 101",
        "Simbologia orientada por ANSI/ISA-5.1 e IEC 62424. Confirmar tecnologia, contatos,\\P"
        "conexões ao processo e requisitos de instalação no projeto executivo.",
        "LT: transmissor | LIC: controlador | LSL/LSH/LSHH: chaves | FY: conversão/comando",
    ),
    SheetSpec(
        3,
        "03_malha_controle.dxf",
        "MALHA DE CONTROLE LIC-101",
        "Variável controlada, manipulada, perturbações e estratégia PI",
        "Aumentar frequência quando PV < SP. Confirmar o sentido no equipamento real.\\P"
        "Kc e Ti são valores iniciais conservadores, sujeitos a comissionamento.",
        "SP: setpoint | PV: nível | MV: frequência | Kc: ganho | Ti: integral | Td: derivativa",
    ),
    SheetSpec(
        4,
        "04_diagrama_eletrico.dxf",
        "DIAGRAMA ELÉTRICO",
        "Potência 220 V 3~ e comando/instrumentação em 24 Vcc",
        "Proteções e bitolas são preliminares. LSHH-101 participa do bloqueio de STO fora\\P"
        "da rotina PID; não se declara categoria, PL ou SIL sem análise de risco.",
        "QF: disjuntor | PS: fonte | KSR: relé | STO: torque seguro desligado | PE: proteção",
    ),
    SheetSpec(
        5,
        "05_interligacoes_instrumentos.dxf",
        "INTERLIGAÇÕES DOS INSTRUMENTOS",
        "Bornes, cabos, sinais analógicos e discretos da malha 101",
        "Segregar cabos analógicos dos cabos do VFD. Aterrar blindagem em um ponto no painel.\\P"
        "Polaridade, contato e terminação dependem das folhas de dados selecionadas.",
        "AI/AO: analógico | DI/DO: digital | SH: blindagem | X2/X3/X4: réguas de bornes",
    ),
    SheetSpec(
        6,
        "06_layout_sistema.dxf",
        "LAYOUT DO SISTEMA",
        "Arranjo conceitual do reservatório, bomba, painel e rotas",
        "Dimensões são indicativas e não representam levantamento de campo. Verificar acesso,\\P"
        "manutenção, NPSH, ventilação do painel, EMC, drenagem e segurança.",
        "P: potência | I: instrumentação | C: controle | E: eletrocalha | Área hachurada: acesso",
    ),
    SheetSpec(
        7,
        "07_sequencia_operacao_causa_efeito.dxf",
        "SEQUÊNCIA DE OPERAÇÃO E CAUSA–EFEITO",
        "Partida, controle de nível, permissivos e resposta a falhas",
        "Sequência conceitual; ação operacional de LA-L/LA-H permanece pendente.\\P"
        "Sem classificação SIL/PL. Retenção após falta de energia depende do PLC selecionado.",
        "PV/SP: nível/setpoint | LA-L/LA-H: alarmes em 15%/85% | ACK: reconhecimento/rearme | LSHH: alto-alto",
    ),
)


CAUSE_EFFECTS = (
    ("E01", "STOP / emergência", "STOP ou emergência atuada", "Retira comando de marcha", "Alarme retido", "Causa removida + ACK consciente"),
    ("E02", "LSHH-101", "Nível ≥ 95%", "Bloqueia permissivo e solicita parada fora do PI", "LA-HH-101 retido", "Condição normal + ACK"),
    ("E03", "LT-101 inválido", "Sinal < 3,6 mA ou > 21 mA", "Desabilita PI e solicita parada", "UA-101 retido", "Sinal válido + ACK"),
    ("E04", "Falha do VFD", "VFD indica falha", "Retira marcha e bloqueia partida", "YA-101 retido", "VFD pronto + ACK"),
    ("E05", "Tempo excedido", "Máx. 60 min (premissa)", "Retira marcha e bloqueia partida", "TA-101 retido", "Causa removida + ACK"),
    ("E06", "Perda de energia", "Alimentação ausente", "Saídas desenergizadas", "Retenção depende do PLC", "Sem repartida automática"),
    ("E07", "LT / chaves divergentes", "Divergência persistente", "Diagnóstico; bloqueia AUTO", "Diagnóstico indicado", "Causa removida + ACK"),
    ("E08", "LA-L-101", "LT-101 ≤ 15%", "Alarme; ação de processo pendente", "LA-L-101 retido", "Causa removida + ACK"),
    ("E09", "LA-H-101", "LT-101 ≥ 85%", "Alarme; ação de processo pendente", "LA-H-101 retido", "Causa removida + ACK"),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered(
    layout,
    value: str,
    point: tuple[float, float],
    height: float = 1.7,
    layer: str = "02_TEXTO",
) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def box(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    description: str,
    layer: str = "04_EQUIPAMENTOS",
    *,
    text_height: float = 1.45,
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5.0), 2.0, layer)
    centered(layout, description, ((x0 + x1) / 2, y0 + 5.0), text_height, "02_TEXTO")


def orthogonal(layout, points: list[tuple[float, float]], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def arrow(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    line(layout, start, end, layer)
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = 3.0
    tip_a = (x2 - ux * size + px * size * 0.55, y2 - uy * size + py * size * 0.55)
    tip_b = (x2 - ux * size - px * size * 0.55, y2 - uy * size - py * size * 0.55)
    line(layout, tip_a, end, layer)
    line(layout, tip_b, end, layer)


def instrument(layout, point: tuple[float, float], tag: str, *, radius: float = 7.0) -> None:
    x, y = point
    layout.add_circle(point, radius, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    line(layout, (x - radius, y), (x + radius, y), "07_INSTRUMENTACAO")
    centered(layout, tag, (x, y + 2.5), 1.55, "07_INSTRUMENTACAO")


def pump(layout, point: tuple[float, float], tag: str) -> None:
    x, y = point
    layout.add_circle(point, 10, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    layout.add_lwpolyline(
        [(x - 5, y - 5), (x + 6, y), (x - 5, y + 5)],
        close=True,
        dxfattribs={"layer": "04_EQUIPAMENTOS"},
    )
    centered(layout, tag, (x, y - 15), 1.8, "04_EQUIPAMENTOS")


def motor(layout, point: tuple[float, float], tag: str) -> None:
    x, y = point
    layout.add_circle(point, 9, dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "M", (x, y + 1.6), 3.8, "05_POTENCIA")
    centered(layout, "3~", (x, y - 3.5), 1.5, "05_POTENCIA")
    centered(layout, tag, (x, y - 14), 1.7, "05_POTENCIA")


def tank(layout, x0: float, y0: float, x1: float, y1: float, level: float = 0.60) -> None:
    line(layout, (x0, y1), (x0, y0), "04_EQUIPAMENTOS")
    line(layout, (x0, y0), (x1, y0), "04_EQUIPAMENTOS")
    line(layout, (x1, y0), (x1, y1), "04_EQUIPAMENTOS")
    water_y = y0 + (y1 - y0) * level
    line(layout, (x0 + 2, water_y), (x1 - 2, water_y), "07_INSTRUMENTACAO")
    centered(layout, f"NÍVEL {int(level * 100)}%", ((x0 + x1) / 2, water_y - 5), 1.45, "07_INSTRUMENTACAO")


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRIÇÃO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("ORIGEM A MONTANTE NÃO ESPECIFICADA", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.62, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATÓRIO", (22, 42), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.50, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.50, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/07",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/07"
    define_title_block(doc)
    define_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 4.2, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 2.1, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_process(layout) -> None:
    centered(layout, "ORIGEM DE ÁGUA", (68, 203), 1.8, "02_TEXTO")
    centered(layout, "EQUIPAMENTO A MONTANTE NÃO DEFINIDO", (68, 198), 1.15, "02_TEXTO")
    arrow(layout, (24, 190), (118, 190), "05_POTENCIA")
    pump(layout, (128, 190), "P-101")
    motor(layout, (128, 224), "M-101 / 4 kW")
    line(layout, (128, 215), (128, 200), "04_EQUIPAMENTOS")
    arrow(layout, (138, 190), (208, 190), "05_POTENCIA")
    centered(layout, "VAZÃO DE ENTRADA", (172, 196), 1.5, "05_POTENCIA")
    centered(layout, "VARIÁVEL MANIPULADA", (172, 186), 1.35, "07_INSTRUMENTACAO")
    tank(layout, 208, 135, 310, 245, 0.60)
    centered(layout, "TK-101 / 10 m³", (259, 126), 2.0, "04_EQUIPAMENTOS")
    instrument(layout, (284, 204), "LT-101")
    line(layout, (284, 197), (284, 188), "07_INSTRUMENTACAO")
    centered(layout, "PV = NÍVEL", (284, 179), 1.55, "07_INSTRUMENTACAO")
    line(layout, (310, 150), (342, 150), "05_POTENCIA")
    box(layout, 342, 138, 371, 162, "HV-102", "Válvula manual", "04_EQUIPAMENTOS", text_height=1.2)
    arrow(layout, (371, 150), (402, 150), "05_POTENCIA")
    centered(layout, "CONSUMO", (386, 158), 1.55, "05_POTENCIA")
    centered(layout, "PERTURBAÇÃO d(t)", (386, 140), 1.4, "07_INSTRUMENTACAO")
    box(layout, 98, 108, 157, 142, "VFD-101", "20–60 Hz", "06_COMANDO")
    box(layout, 171, 108, 230, 142, "PLC-101", "LIC-101 / PI", "07_INSTRUMENTACAO")
    orthogonal(layout, [(200.5, 142), (200.5, 158), (284, 158), (284, 197)], "07_INSTRUMENTACAO")
    arrow(layout, (171, 125), (157, 125), "07_INSTRUMENTACAO")
    orthogonal(layout, [(127.5, 142), (127.5, 181)], "06_COMANDO")
    centered(layout, "AO 4–20 mA", (164, 130), 1.3, "07_INSTRUMENTACAO")


def draw_pid(layout) -> None:
    tank(layout, 205, 122, 305, 244, 0.60)
    centered(layout, "TK-101", (255, 113), 2.1, "04_EQUIPAMENTOS")
    levels = ((140, "LSL-101", "15%"), (217, "LSH-101", "85%"), (232, "LSHH-101", "95%"))
    for y, tag, percent in levels:
        line(layout, (205, y), (190, y), "07_INSTRUMENTACAO")
        instrument(layout, (175, y), tag, radius=7)
        centered(layout, percent, (175, y - 10), 1.3, "07_INSTRUMENTACAO")
    instrument(layout, (331, 189), "LT-101")
    line(layout, (305, 189), (324, 189), "07_INSTRUMENTACAO")
    centered(layout, "4–20 mA", (332, 178), 1.35, "07_INSTRUMENTACAO")
    instrument(layout, (365, 229), "LIC-101", radius=9)
    orthogonal(layout, [(331, 196), (331, 229), (356, 229)], "07_INSTRUMENTACAO")
    box(layout, 338, 127, 393, 160, "FY-101", "AO / VFD", "07_INSTRUMENTACAO")
    arrow(layout, (365, 220), (365, 160), "07_INSTRUMENTACAO")
    pump(layout, (111, 166), "P-101")
    motor(layout, (111, 205), "M-101")
    line(layout, (111, 196), (111, 176), "04_EQUIPAMENTOS")
    box(layout, 75, 111, 147, 139, "VFD-101", "4 kW / 220 V", "06_COMANDO")
    orthogonal(layout, [(111, 139), (111, 157)], "06_COMANDO")
    orthogonal(layout, [(338, 143.5), (147, 143.5), (147, 125), (147, 125)], "07_INSTRUMENTACAO")
    line(layout, (121, 166), (205, 166), "05_POTENCIA")
    arrow(layout, (24, 166), (101, 166), "05_POTENCIA")
    line(layout, (305, 135), (401, 135), "05_POTENCIA")
    arrow(layout, (371, 135), (401, 135), "05_POTENCIA")
    centered(layout, "ENTRADA", (48, 173), 1.5, "05_POTENCIA")
    centered(layout, "SAÍDA / CONSUMO", (364, 126), 1.5, "05_POTENCIA")
    centered(layout, "SINAL CONTÍNUO", (332, 239), 1.3, "07_INSTRUMENTACAO")
    centered(layout, "LSHH-101 → KSR-101 / STO", (113, 252), 1.55, "06_COMANDO")
    orthogonal(layout, [(168, 232), (130, 232), (130, 247)], "06_COMANDO")


def draw_control_loop(layout) -> None:
    centered(layout, "CAMINHO DIRETO", (210, 254), 2.0, "07_INSTRUMENTACAO")
    boxes = (
        (23, 198, 67, 232, "SP", "60%"),
        (83, 192, 143, 238, "LIC-101", "PI"),
        (159, 192, 219, 238, "AO / VFD", "20–60 Hz"),
        (235, 192, 295, 238, "P-101", "Vazão"),
        (311, 192, 371, 238, "TK-101", "Nível"),
    )
    for values in boxes:
        box(layout, *values, "07_INSTRUMENTACAO")
    for x0, x1 in ((67, 83), (143, 159), (219, 235), (295, 311)):
        arrow(layout, (x0, 215), (x1, 215), "07_INSTRUMENTACAO")
    centered(layout, "e(t)", (75, 221), 1.35, "07_INSTRUMENTACAO")
    centered(layout, "MV", (227, 221), 1.35, "07_INSTRUMENTACAO")
    arrow(layout, (401, 251), (341, 238), "07_INSTRUMENTACAO")
    centered(layout, "d(t): CONSUMO", (371, 257), 1.45, "07_INSTRUMENTACAO")
    box(layout, 311, 145, 371, 175, "LT-101", "PV 4–20 mA", "07_INSTRUMENTACAO")
    orthogonal(layout, [(341, 192), (341, 175)], "07_INSTRUMENTACAO")
    arrow(layout, (311, 160), (113, 160), "07_INSTRUMENTACAO")
    orthogonal(layout, [(113, 160), (113, 192)], "07_INSTRUMENTACAO")
    centered(layout, "REALIMENTAÇÃO NEGATIVA", (221, 167), 1.45, "07_INSTRUMENTACAO")

    add_rect(layout, 23, 105, 286, 132, "12_LEGENDA")
    centered(layout, "PARÂMETROS INICIAIS DE COMISSIONAMENTO", (154.5, 126), 1.8, "12_LEGENDA")
    centered(layout, "Kc = 0,8 %/%  |  Ti = 120 s  |  Td = 0 s  |  anti-windup  |  transferência sem salto", (154.5, 115), 1.45, "02_TEXTO")
    add_rect(layout, 298, 105, 401, 132, "13_NOTAS")
    centered(layout, "FALHAS / AÇÕES", (349.5, 125), 1.8, "13_NOTAS")
    centered(layout, "LT inválido / VFD falha → PARAR + ALARMAR", (349.5, 116), 1.18, "13_NOTAS")
    centered(layout, "LSHH ativo → STO + BLOQUEIO; rearme consciente", (349.5, 109), 1.18, "13_NOTAS")


def draw_electrical(layout) -> None:
    centered(layout, "POTÊNCIA 220 V 3~", (106, 255), 2.1, "05_POTENCIA")
    for x, phase in ((35, "L1"), (49, "L2"), (63, "L3")):
        line(layout, (x, 246), (x, 231), "05_POTENCIA")
        centered(layout, phase, (x, 251), 1.5, "05_POTENCIA")
    box(layout, 25, 199, 73, 231, "QF1", "3P / prelim.", "05_POTENCIA")
    for x in (35, 49, 63):
        line(layout, (x, 199), (x, 187), "05_POTENCIA")
    box(layout, 21, 143, 103, 187, "VFD-101", "4 kW / STO", "05_POTENCIA")
    for x in (40, 62, 84):
        line(layout, (x, 143), (x, 129), "05_POTENCIA")
    motor(layout, (62, 116), "M-101 / P-101")
    line(layout, (92, 105), (92, 125), "05_POTENCIA")
    line(layout, (86, 105), (98, 105), "05_POTENCIA")
    centered(layout, "PE", (103, 108), 1.5, "05_POTENCIA")

    centered(layout, "COMANDO 24 Vcc", (273, 255), 2.1, "06_COMANDO")
    box(layout, 143, 213, 191, 244, "PS1", "24 Vcc / 5 A", "04_EQUIPAMENTOS")
    box(layout, 211, 207, 282, 250, "PLC-101", "AI / AO / DI / DO", "07_INSTRUMENTACAO")
    box(layout, 306, 207, 382, 250, "KSR-101", "Emergência + LSHH", "06_COMANDO", text_height=1.25)
    line(layout, (191, 228.5), (211, 228.5), "06_COMANDO")
    line(layout, (282, 228.5), (306, 228.5), "06_COMANDO")
    centered(layout, "+24 V / 0 V", (201, 235), 1.25, "06_COMANDO")

    add_rect(layout, 143, 105, 400, 188, "09_BORNES")
    centered(layout, "INTERFACES E PERMISSIVOS", (271.5, 181), 1.9, "09_BORNES")
    rows = (
        ("AI0", "LT-101 4–20 mA", "X2:01-02"),
        ("AO0", "REF. VFD 4–20 mA", "X4:01-02"),
        ("DI2", "LSHH-101", "X3:05-06"),
        ("DI3/4/5", "VFD PRONTO/RUN/FALHA", "X4:03-10"),
        ("DO0", "RUN VFD", "X4:11-12"),
        ("KSR", "S0 + LSHH → STO A/B", "FÍSICO"),
    )
    for i, (channel, signal, terminal) in enumerate(rows):
        y = 166 - i * 10
        line(layout, (148, y - 4), (395, y - 4), "09_BORNES")
        add_text(layout, channel, (151, y), 1.35, layer="07_INSTRUMENTACAO")
        add_text(layout, signal, (195, y), 1.30, layer="02_TEXTO")
        add_text(layout, terminal, (345, y), 1.30, layer="09_BORNES")
    orthogonal(layout, [(344, 207), (344, 196), (92, 196), (92, 176)], "06_COMANDO")
    centered(layout, "STO A/B", (122, 202), 1.35, "06_COMANDO")


def table(layout, x0: float, x1: float, y_top: float, title: str, rows: tuple[tuple[str, str, str, str], ...]) -> None:
    header_h, row_h = 12.0, 12.0
    bottom = y_top - header_h - len(rows) * row_h
    add_rect(layout, x0, bottom, x1, y_top, "09_BORNES")
    line(layout, (x0, y_top - header_h), (x1, y_top - header_h), "09_BORNES")
    c1, c2, c3 = x0 + 38, x0 + 91, x1 - 55
    for x in (c1, c2, c3):
        line(layout, (x, bottom), (x, y_top - header_h), "09_BORNES")
    centered(layout, title, ((x0 + x1) / 2, y_top - 6), 1.9, "09_BORNES")
    for index, row in enumerate(rows):
        y1 = y_top - header_h - index * row_h
        y0 = y1 - row_h
        if index:
            line(layout, (x0, y1), (x1, y1), "09_BORNES")
        cy = (y0 + y1) / 2
        centers = ((x0 + c1) / 2, (c1 + c2) / 2, (c2 + c3) / 2, (c3 + x1) / 2)
        for value, x in zip(row, centers):
            centered(layout, value, (x, cy), 1.22, "02_TEXTO")


def draw_interconnections(layout) -> None:
    analog = (
        ("C-101", "LT-101", "X2:01-02 / AI0", "1P BLIND."),
        ("C-105A", "AO0 REF", "X4:01-02 / VFD", "1P BLIND."),
        ("C-105B", "VFD FB", "X4:07-08 / AI1", "1P BLIND."),
    )
    discrete = (
        ("C-102", "LSL-101", "X3:01-02 / DI0", "2x0,75"),
        ("C-103", "LSH-101", "X3:03-04 / DI1", "2x0,75"),
        ("C-104", "LSHH-101", "X3:05-06 / KSR", "2x0,75"),
        ("C-106", "VFD I/O", "X4:03-14", "8x0,75"),
    )
    table(layout, 18, 205, 258, "SINAIS ANALÓGICOS", analog)
    table(layout, 215, 402, 258, "SINAIS DISCRETOS", discrete)

    box(layout, 18, 134, 82, 175, "CAMPO", "LT / LS", "07_INSTRUMENTACAO")
    box(layout, 105, 134, 169, 175, "X2 / X3", "Bornes", "09_BORNES")
    box(layout, 192, 134, 256, 175, "PLC-101", "AI / DI", "07_INSTRUMENTACAO")
    box(layout, 279, 134, 343, 175, "X4", "AO / DI / DO", "09_BORNES")
    box(layout, 366, 134, 402, 175, "VFD", "I/O", "06_COMANDO")
    for x0, x1, tag in ((82, 105, "C-101/104"), (169, 192, "INTERNO"), (256, 279, "INTERNO"), (343, 366, "C-105/106")):
        line(layout, (x0, 154.5), (x1, 154.5), "08_CABOS")
        centered(layout, tag, ((x0 + x1) / 2, 161), 1.05, "08_CABOS")
    centered(layout, "SH", (112, 126), 1.4, "08_CABOS")
    line(layout, (112, 134), (112, 120), "08_CABOS")
    line(layout, (106, 120), (118, 120), "05_POTENCIA")
    line(layout, (108, 117), (116, 117), "05_POTENCIA")
    line(layout, (110, 114), (114, 114), "05_POTENCIA")
    centered(layout, "Blindagens em ponto único no painel; não conectar a ambas as extremidades sem estudo EMC.", (260, 112), 1.4, "13_NOTAS")


def draw_layout(layout) -> None:
    add_rect(layout, 18, 105, 402, 260, "11_ARQUITETURA")
    centered(layout, "ÁREA CONCEITUAL 12 m x 7 m", (210, 254), 2.0, "11_ARQUITETURA")
    tank(layout, 244, 146, 335, 235, 0.60)
    centered(layout, "TK-101", (289.5, 138), 2.0, "04_EQUIPAMENTOS")
    pump(layout, (159, 164), "P-101")
    motor(layout, (159, 198), "M-101")
    line(layout, (169, 164), (244, 164), "05_POTENCIA")
    arrow(layout, (93, 164), (149, 164), "05_POTENCIA")
    box(layout, 34, 207, 105, 239, "PAINEL-101", "PLC + VFD", "04_EQUIPAMENTOS")
    box(layout, 345, 211, 392, 241, "LT-101", "Campo", "07_INSTRUMENTACAO")
    line(layout, (335, 219), (345, 226), "07_INSTRUMENTACAO")
    centered(layout, "SAÍDA", (374, 130), 1.6, "05_POTENCIA")
    arrow(layout, (335, 151), (392, 151), "05_POTENCIA")

    add_rect(layout, 26, 184, 231, 197, "10_ELETROCALHAS")
    centered(layout, "E-101: ELETROCALHA P / C / I SEGREGADAS", (128.5, 190.5), 1.35, "10_ELETROCALHAS")
    orthogonal(layout, [(69.5, 207), (69.5, 197)], "08_CABOS")
    orthogonal(layout, [(159, 184), (159, 173)], "08_CABOS")
    orthogonal(layout, [(231, 190.5), (366, 190.5), (366, 211)], "08_CABOS")
    centered(layout, "C-101 / C-102 / C-103 / C-104", (299, 210), 1.3, "08_CABOS")

    add_rect(layout, 225, 122, 353, 247, "03_COTAS")
    centered(layout, "FAIXA DE ACESSO E MANUTENÇÃO", (289, 116), 1.45, "03_COTAS")
    line(layout, (18, 266), (402, 266), "03_COTAS")
    centered(layout, "12 000 mm (INDICATIVO)", (210, 263), 1.5, "03_COTAS")
    line(layout, (408, 105), (408, 260), "03_COTAS")
    centered(layout, "7 000 mm", (400, 182), 1.45, "03_COTAS")
    add_rect(layout, 34, 108, 181, 132, "13_NOTAS")
    centered(layout, "ROTAS: POTÊNCIA ≠ ANALÓGICO", (107.5, 125), 1.6, "13_NOTAS")
    centered(layout, "Confirmar drenagem, ventilação, NPSH e acesso", (107.5, 115), 1.25, "13_NOTAS")


def draw_cause_effect_table(layout) -> None:
    x0, x1, y_top = 18.0, 402.0, 178.0
    columns = (x0, 43.0, 108.0, 177.0, 267.0, 328.0, x1)
    headers = ("ID", "EVENTO", "DETECÇÃO", "AÇÃO CONCEITUAL", "ALARME / MEMÓRIA", "RETORNO")
    header_h, row_h = 9.0, 7.5
    bottom = y_top - header_h - len(CAUSE_EFFECTS) * row_h
    add_rect(layout, x0, bottom, x1, y_top, "09_BORNES")
    line(layout, (x0, y_top - header_h), (x1, y_top - header_h), "09_BORNES")
    for x in columns[1:-1]:
        line(layout, (x, bottom), (x, y_top), "09_BORNES")
    for index, title in enumerate(headers):
        centered(layout, title, ((columns[index] + columns[index + 1]) / 2, y_top - header_h / 2), 1.4, "12_LEGENDA")
    for row_index, row in enumerate(CAUSE_EFFECTS):
        top = y_top - header_h - row_index * row_h
        if row_index:
            line(layout, (x0, top), (x1, top), "09_BORNES")
        center_y = top - row_h / 2
        for col_index, value in enumerate(row):
            centered(layout, value, ((columns[col_index] + columns[col_index + 1]) / 2, center_y), 1.35, "02_TEXTO")


def draw_operating_sequence(layout) -> None:
    steps = (
        (22, 87, "01  VERIFICAR", "Emergência liberada\nKSR / VFD prontos\nLT válido; LSHH inativo"),
        (99, 164, "02  HABILITAR", "Operador seleciona AUTO\ne confirma habilitação"),
        (176, 241, "03  TRANSFERIR", "LIC assume saída rastreada\nLimites + anti-windup"),
        (253, 318, "04  CONTROLAR", "PI: PV < SP → sobe Hz\nPV > SP → reduz Hz"),
        (330, 397, "05  MONITORAR", "VFD / LT / LSHH\nFalhas → matriz abaixo"),
    )
    top, bottom = 250.0, 207.0
    for x0, x1, title, detail in steps:
        add_rect(layout, x0, bottom, x1, top, "04_EQUIPAMENTOS")
        centered(layout, title, ((x0 + x1) / 2, top - 8), 1.65, "04_EQUIPAMENTOS")
        lines = detail.splitlines()
        for line_index, value in enumerate(lines):
            centered(layout, value, ((x0 + x1) / 2, top - 20 - line_index * 8), 1.35, "02_TEXTO")
    for left, right in zip(steps, steps[1:]):
        arrow(layout, (left[1], 228.5), (right[0], 228.5), "08_CABOS")
    add_rect(layout, 22, 184, 397, 198, "13_NOTAS")
    centered(layout, "OPERAÇÃO NORMAL: PI regula a frequência; STOP, LSHH, LT inválido, falha do VFD ou tempo excedido retiram a marcha.", (209.5, 194), 1.3, "13_NOTAS")
    centered(layout, "LA-L/LA-H em 15%/85% são alarmes; a ação operacional permanece pendente nesta revisão.", (209.5, 190), 1.3, "13_NOTAS")
    centered(layout, "Após falta de energia, não há repartida automática. Aplicar permissivos e rearme consciente antes de nova partida.", (209.5, 186), 1.3, "13_NOTAS")
    draw_cause_effect_table(layout)


DRAWERS = {
    1: draw_process,
    2: draw_pid,
    3: draw_control_loop,
    4: draw_electrical,
    5: draw_interconnections,
    6: draw_layout,
    7: draw_operating_sequence,
}


def write_matrix_csv(project_dir: Path) -> Path:
    path = project_dir / "matriz-causa-efeito.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("id", "evento", "deteccao", "acao_conceitual", "alarme_memoria", "retorno"))
        writer.writerows(CAUSE_EFFECTS)
    return path


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        DRAWERS[spec.number](layout)
        output = source_dir / spec.filename
        prepare_deterministic_write(doc)
        with output.open("wt", encoding="utf-8", newline="\n") as stream:
            doc.write(stream)
        outputs.append(output)
        print(f"Gerado: {output.relative_to(root)}")
    matrix = write_matrix_csv(root / PROJECT_SLUG)
    outputs.append(matrix)
    print(f"Gerado: {matrix.relative_to(root)}")
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
