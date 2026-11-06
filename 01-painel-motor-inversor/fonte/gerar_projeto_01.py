"""Gera as oito pranchas DXF do Projeto 01 de forma deterministica."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import math
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
    TEXT_STYLE,
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


PROJECT_SLUG = "01-painel-motor-inversor"
PROJECT_DATE = "2026-11-06"
REVISION = "04"


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
        "01_diagrama_unifilar.dxf",
        "DIAGRAMA UNIFILAR",
        "Arquitetura geral de potência e aterramento",
        "Rede assumida: 380 V, 3 fases, 60 Hz, TN-S. Motor M1: 7,5 kW.\\P"
        "Q0, Q1, DPS1 e VFD1 exigem seleção final por estudo de aplicação.",
        "Q: manobra/proteção | VFD: inversor | X: borne | M: motor | PE: proteção",
    ),
    SheetSpec(
        2,
        "02_diagrama_potencia.dxf",
        "DIAGRAMA DE POTÊNCIA",
        "Circuito trifásico do alimentador ao motor",
        "Não manobrar o circuito entre VFD1 e M1 com o inversor em operação.\\P"
        "Blindagem de W02 terminada em 360 graus nas duas extremidades.",
        "L1/L2/L3: fases | U/V/W: saída PWM | PE: proteção | SH: blindagem",
    ),
    SheetSpec(
        3,
        "03_diagrama_comando.dxf",
        "DIAGRAMA DE COMANDO",
        "Comandos funcionais separados, seleção local/remoto e STO",
        "S5 rearma KSR1; S4/X3:9 reiniciam falha do VFD.\\P"
        "Pinagem e categoria de segurança dependem de seleção e análise.",
        "S: botão/seletor | H: sinalizador | KSR: relé de segurança | DI/AI/RO: I/O",
    ),
    SheetSpec(
        4,
        "04_layout_interno_painel.dxf",
        "LAYOUT INTERNO DO PAINEL",
        "Arranjo conceitual do invólucro 800 x 600 x 300 mm",
        "Dimensões do painel e folgas são premissas acadêmicas. Confirmar perdas,\\P"
        "ventilação, EMC, acessibilidade, raio de curvatura e manutenção.",
        "Tracejado: trilho DIN | Cinza: canaleta | PE: barra de proteção | SH: abraçadeira",
    ),
    SheetSpec(
        5,
        "05_diagrama_bornes.dxf",
        "DIAGRAMA DE BORNES",
        "Réguas X1, X2 e X3 com cabos e funções identificados",
        "Separar fisicamente potência, comando e sinais analógicos. Identificar todos\\P"
        "os condutores nas duas extremidades e aterrar blindagens conforme projeto.",
        "X1: entrada | X2: motor/PTC | X3: comando e sinais | SH: blindagem",
    ),
    SheetSpec(
        6,
        "06_interligacoes_campo.dxf",
        "INTERLIGAÇÕES DE CAMPO",
        "Interfaces do painel com rede, motor, emergência e automação",
        "Comprimentos são premissas para documentação e orçamento conceitual.\\P"
        "Rotas, segregação, queda de tensão e EMC dependem de levantamento em campo.",
        "W01/W02: potência | W03/W04/W05/W06: comando e instrumentação",
    ),
    SheetSpec(
        7,
        "07_protecao_coordenacao.dxf",
        "PROTEÇÃO E DADOS PARA COORDENAÇÃO",
        "Mapa das premissas e evidências que ainda precisam ser obtidas",
        "Os valores atuais são didáticos e não provam seleção, capacidade de interrupção,\\P"
        "seletividade, retaguarda, proteção térmica ou coordenação entre fabricantes.",
        "Icc: curto-circuito presumido | Icu/Ics: capacidade do dispositivo | SCPD: proteção contra curto",
    ),
    SheetSpec(
        8,
        "08_plano_verificacao_evidencias.dxf",
        "PLANO DE VERIFICAÇÃO E EVIDÊNCIAS",
        "Matriz de encerramento documental e funcional — sem ensaios executados",
        "Critérios e tolerâncias devem vir dos documentos e fabricantes selecionados.\\P"
        "A matriz não registra resultados de campo nem autoriza energização ou comissionamento.",
        "ID: ponto de verificação | evidência: registro necessário | status: não executado",
    ),
    SheetSpec(
        9,
        "09_sequencia_operacional_estados.dxf",
        "SEQUÊNCIA OPERACIONAL E ESTADOS",
        "Habilitação, operação normal, parada e respostas a eventos",
        "Sequência conceitual; a implementação depende dos equipamentos, lógica e ensaios.\\P"
        "Não define tempo de parada, categoria/PL/SIL nem validação em campo.",
        "S5: rearme KSR1 | S4/X3:9: reset do VFD | H2: pronto | H3: marcha | H4: falha",
    ),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered_text(layout, value: str, point: tuple[float, float], height: float, layer: str) -> None:
    add_text(
        layout,
        value,
        point,
        height,
        layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )


def equipment_box(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    description: str,
    *,
    layer: str = "04_EQUIPAMENTOS",
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered_text(layout, tag, ((x0 + x1) / 2.0, y1 - 5.0), 2.5, layer)
    centered_text(layout, description, ((x0 + x1) / 2.0, y0 + 5.0), 1.6, "02_TEXTO")


def cable_label(layout, value: str, point: tuple[float, float]) -> None:
    centered_text(layout, value, point, 1.8, "08_CABOS")


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    if "P01_MOTOR" not in doc.blocks:
        motor = doc.blocks.new("P01_MOTOR", base_point=(0.0, 0.0))
        motor.add_circle((0.0, 0.0), 12.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        centered_text(motor, "M", (0.0, 2.0), 5.0, "04_EQUIPAMENTOS")
        centered_text(motor, "3~", (0.0, -5.0), 2.0, "04_EQUIPAMENTOS")

    if "P01_TERRA" not in doc.blocks:
        ground = doc.blocks.new("P01_TERRA", base_point=(0.0, 0.0))
        line(ground, (0.0, 4.0), (0.0, 0.0), "05_POTENCIA")
        line(ground, (-4.0, 0.0), (4.0, 0.0), "05_POTENCIA")
        line(ground, (-2.8, -1.7), (2.8, -1.7), "05_POTENCIA")
        line(ground, (-1.4, -3.4), (1.4, -3.4), "05_POTENCIA")

    for name, normally_closed in (("P01_CONTATO_NA", False), ("P01_CONTATO_NF", True)):
        if name in doc.blocks:
            continue
        block = doc.blocks.new(name, base_point=(0.0, 0.0))
        line(block, (-7.0, 0.0), (-2.0, 0.0), "06_COMANDO")
        line(block, (2.0, 0.0), (7.0, 0.0), "06_COMANDO")
        line(block, (-2.0, 0.0), (2.0, 3.0), "06_COMANDO")
        if normally_closed:
            line(block, (-2.0, 3.0), (2.0, -1.0), "06_COMANDO")

    if "P01_LAMPADA" not in doc.blocks:
        lamp = doc.blocks.new("P01_LAMPADA", base_point=(0.0, 0.0))
        lamp.add_circle((0.0, 0.0), 3.2, dxfattribs={"layer": "06_COMANDO"})
        line(lamp, (-2.2, -2.2), (2.2, 2.2), "06_COMANDO")
        line(lamp, (-2.2, 2.2), (2.2, -2.2), "06_COMANDO")

    if "P01_POT" not in doc.blocks:
        pot = doc.blocks.new("P01_POT", base_point=(0.0, 0.0))
        line(pot, (-8.0, 0.0), (8.0, 0.0), "07_INSTRUMENTACAO")
        line(pot, (-5.0, -2.0), (-3.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (-3.0, 2.0), (-1.0, -2.0), "07_INSTRUMENTACAO")
        line(pot, (-1.0, -2.0), (1.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (1.0, 2.0), (3.0, -2.0), "07_INSTRUMENTACAO")
        line(pot, (3.0, -2.0), (5.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (0.0, 7.0), (0.0, 2.5), "07_INSTRUMENTACAO")
        line(pot, (0.0, 2.5), (2.0, 4.5), "07_INSTRUMENTACAO")


def add_revision_table(layout) -> None:
    add_rect(layout, 230.0, 72.0, 410.0, 94.0, "01_CARIMBO")
    line(layout, (230.0, 86.0), (410.0, 86.0), "01_CARIMBO")
    for x in (248.0, 280.0, 352.0):
        line(layout, (x, 72.0), (x, 94.0), "01_CARIMBO")
    for value, x in (("REV.", 239.0), ("DATA", 264.0), ("DESCRIÇÃO", 316.0), ("RESP.", 381.0)):
        centered_text(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239.0), (PROJECT_DATE, 264.0), (f"REVISAO VISUAL {REVISION}", 316.0), ("R.E.M.M.", 381.0)):
        centered_text(layout, value, (x, 78.5), 1.7, "02_TEXTO")


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
        "PRANCHA": f"{spec.number:02d}/{len(SHEETS):02d}",
        "ARQUIVO": spec.filename,
        "UNIDADES": "mm",
        "ESCALA": "S/ESC.",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/{len(SHEETS):02d}"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    msp = doc.modelspace()
    add_frame(msp, geometry)
    centered_text(msp, spec.title, (210.0, 277.0), 4.2, "02_TEXTO")
    centered_text(msp, spec.subtitle, (210.0, 270.8), 2.1, "02_TEXTO")
    add_bottom_information(msp, spec, config["portfolio"]["warning"])
    add_revision_table(msp)
    add_title_block(msp, spec, config)
    return doc, msp


def draw_unifilar(layout) -> None:
    y = 191.0
    line(layout, (28.0, y), (67.0, y), "05_POTENCIA")
    equipment_box(layout, 67.0, 177.0, 101.0, 205.0, "Q0", "Seccionadora 3P 32 A")
    line(layout, (101.0, y), (116.0, y), "05_POTENCIA")
    equipment_box(layout, 116.0, 177.0, 151.0, 205.0, "Q1", "Disjuntor 3P 25 A")
    line(layout, (151.0, y), (203.0, y), "05_POTENCIA")
    equipment_box(layout, 203.0, 164.0, 267.0, 218.0, "VFD1", "11 kW / 380-480 V")
    line(layout, (267.0, y), (335.0, y), "05_POTENCIA")
    layout.add_blockref("P01_MOTOR", (351.0, y), dxfattribs={"layer": "04_EQUIPAMENTOS"})

    centered_text(layout, "REDE 3~ 380 V / 60 Hz", (46.0, 218.0), 2.2, "02_TEXTO")
    centered_text(layout, "X1", (46.0, 199.0), 2.0, "09_BORNES")
    layout.add_blockref("SIM_TERMINAL", (46.0, y), dxfattribs={"layer": "09_BORNES"})
    centered_text(layout, "X2", (295.0, 199.0), 2.0, "09_BORNES")
    layout.add_blockref("SIM_TERMINAL", (295.0, y), dxfattribs={"layer": "09_BORNES"})
    centered_text(layout, "M1", (351.0, 211.0), 2.2, "04_EQUIPAMENTOS")
    centered_text(layout, "7,5 kW / 15,5 A", (351.0, 169.0), 1.8, "02_TEXTO")
    cable_label(layout, "W01 - 4G4 mm²", (47.0, 184.0))
    cable_label(layout, "W02 - CABO VFD BLINDADO", (301.0, 181.0))

    line(layout, (170.0, y), (170.0, 157.0), "05_POTENCIA")
    equipment_box(layout, 158.0, 137.0, 182.0, 157.0, "DPS1", "Tipo 2 / 3P")
    line(layout, (170.0, 137.0), (170.0, 120.0), "05_POTENCIA")
    line(layout, (28.0, 120.0), (369.0, 120.0), "05_POTENCIA")
    layout.add_blockref("P01_TERRA", (34.0, 116.0), dxfattribs={"layer": "05_POTENCIA"})
    line(layout, (235.0, 164.0), (235.0, 120.0), "05_POTENCIA")
    line(layout, (351.0, 179.0), (351.0, 120.0), "05_POTENCIA")
    centered_text(layout, "BARRAMENTO PE", (93.0, 126.0), 2.0, "05_POTENCIA")
    centered_text(layout, "TN-S", (50.0, 108.0), 1.8, "02_TEXTO")
    centered_text(layout, "STO A/B E COMANDO 24 Vcc: VER PRANCHA 03", (273.0, 108.0), 1.8, "06_COMANDO")


def draw_power(layout) -> None:
    phases = ((224.0, "L1", "U"), (204.0, "L2", "V"), (184.0, "L3", "W"))
    for y, source_label, output_label in phases:
        line(layout, (27.0, y), (70.0, y), "05_POTENCIA")
        line(layout, (100.0, y), (117.0, y), "05_POTENCIA")
        line(layout, (147.0, y), (187.0, y), "05_POTENCIA")
        line(layout, (255.0, y), (300.0, y), "05_POTENCIA")
        motor_y = 204.0 + (y - 204.0) * 0.48
        motor_dy = motor_y - 204.0
        motor_x = 352.0 - math.sqrt(12.0**2 - motor_dy**2)
        line(layout, (304.0, y), (motor_x, motor_y), "05_POTENCIA")
        add_text(layout, source_label, (30.0, y + 2.5), 1.8, layer="02_TEXTO")
        add_text(layout, output_label, (260.0, y + 2.5), 1.8, layer="02_TEXTO")
        layout.add_blockref("SIM_TERMINAL", (302.0, y), dxfattribs={"layer": "09_BORNES"})

    equipment_box(layout, 70.0, 172.0, 100.0, 236.0, "Q0", "AC-23A / 32 A")
    equipment_box(layout, 117.0, 172.0, 147.0, 236.0, "Q1", "3P / 25 A / 10 kA")
    for y, _, _ in phases:
        line(layout, (70.0, y), (80.0, y), "05_POTENCIA")
        line(layout, (80.0, y), (92.0, y + 3.0), "05_POTENCIA")
        line(layout, (92.0, y + 3.0), (100.0, y), "05_POTENCIA")
        line(layout, (117.0, y), (127.0, y), "05_POTENCIA")
        line(layout, (127.0, y), (139.0, y + 3.0), "05_POTENCIA")
        line(layout, (139.0, y + 3.0), (147.0, y), "05_POTENCIA")
    equipment_box(layout, 187.0, 163.0, 255.0, 245.0, "VFD1", "R/S/T → U/V/W")
    centered_text(layout, "RETIFICADOR + BARRAMENTO CC + INVERSOR PWM", (221.0, 203.0), 1.7, "04_EQUIPAMENTOS")
    centered_text(layout, "X2:1...3", (302.0, 239.0), 1.8, "09_BORNES")
    layout.add_blockref("P01_MOTOR", (352.0, 204.0), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    centered_text(layout, "M1", (352.0, 224.0), 2.1, "04_EQUIPAMENTOS")

    for x in (159.0, 165.0, 171.0):
        line(layout, (x, 184.0 + (x - 159.0) / 6.0 * 40.0), (x, 157.0), "05_POTENCIA")
    equipment_box(layout, 151.0, 137.0, 179.0, 157.0, "DPS1", "T2 / 3P")
    line(layout, (165.0, 137.0), (165.0, 116.0), "05_POTENCIA")
    line(layout, (28.0, 116.0), (370.0, 116.0), "05_POTENCIA")
    layout.add_blockref("P01_TERRA", (34.0, 112.0), dxfattribs={"layer": "05_POTENCIA"})
    line(layout, (221.0, 163.0), (221.0, 116.0), "05_POTENCIA")
    line(layout, (352.0, 192.0), (352.0, 116.0), "05_POTENCIA")
    centered_text(layout, "PE", (47.0, 122.0), 1.8, "05_POTENCIA")
    cable_label(layout, "W01", (48.0, 233.0))
    cable_label(layout, "W02 - BLINDAGEM SH/PE", (284.0, 158.0))
    centered_text(layout, "Proteção térmica eletrônica: parâmetro de VFD1 = 15,5 A", (282.0, 108.0), 1.8, "13_NOTAS")


def add_contact(layout, x: float, y: float, tag: str, *, nc: bool = False, detail: str = "") -> None:
    name = "P01_CONTATO_NF" if nc else "P01_CONTATO_NA"
    layout.add_blockref(name, (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered_text(layout, tag, (x, y + 6.0), 1.8, "06_COMANDO")
    if detail:
        centered_text(layout, detail, (x, y - 5.0), 1.4, "02_TEXTO")


def draw_command(layout) -> None:
    line(layout, (25.0, 103.0), (25.0, 257.0), "06_COMANDO")
    centered_text(layout, "+24 Vcc", (25.0, 263.0), 1.9, "06_COMANDO")
    # S0/KSR1/STO: interface funcional; bornes concretos dependem dos OEMs selecionados.
    for y, tag in ((246.0, "S0A"), (234.0, "S0B")):
        line(layout, (25.0, y), (51.0, y), "06_COMANDO")
        add_contact(layout, 58.0, y, tag, nc=True)
        line(layout, (65.0, y), (135.0, y), "06_COMANDO")
        line(layout, (202.0, y), (270.0, y), "06_COMANDO")
    add_rect(layout, 135.0, 225.0, 202.0, 257.0, "06_COMANDO")
    centered_text(layout, "KSR1", (168.5, 251.0), 2.3, "06_COMANDO")
    centered_text(layout, "2 CANAIS", (168.5, 244.0), 1.5, "02_TEXTO")
    centered_text(layout, "RESET MON.", (168.5, 237.0), 1.4, "02_TEXTO")
    add_text(layout, "STO-A", (216.0, 249.0), 1.5, layer="07_INSTRUMENTACAO")
    add_text(layout, "STO-B", (216.0, 237.0), 1.5, layer="07_INSTRUMENTACAO")

    # S5 is the dedicated manual reset for KSR1. It is separate from VFD fault reset.
    line(layout, (25.0, 220.0), (53.0, 220.0), "06_COMANDO")
    add_contact(layout, 60.0, 220.0, "S5", detail="REARME KSR1")
    line(layout, (67.0, 220.0), (125.0, 220.0), "06_COMANDO")
    line(layout, (125.0, 220.0), (125.0, 229.0), "06_COMANDO")
    line(layout, (125.0, 229.0), (135.0, 229.0), "06_COMANDO")

    # Separate RUN, STOP and VFD-reset functions. S3's mutually exclusive
    # LOCAL/0/REMOTE contacts select the source; exact DI mapping is OEM-dependent.
    command_rows = (
        (204.0, "S3-L", "S1", False, "VFD1-RUN"),
        (192.0, "S3-L", "S2", True, "VFD1-STOP"),
        (180.0, "S3-R", "X3:7", False, "VFD1-RUN"),
        (168.0, "S3-R", "X3:8", True, "VFD1-STOP"),
        (156.0, "S3-L", "S4", False, "VFD1-RESET"),
        (144.0, "S3-R", "X3:9", False, "VFD1-RESET"),
    )
    for y, mode_tag, command_tag, normally_closed, function in command_rows:
        line(layout, (25.0, y), (48.0, y), "06_COMANDO")
        add_contact(layout, 55.0, y, mode_tag)
        line(layout, (62.0, y), (94.0, y), "06_COMANDO")
        add_contact(layout, 101.0, y, command_tag, nc=normally_closed)
        line(layout, (108.0, y), (177.0, y), "06_COMANDO")
        add_text(layout, function, (184.0, y + 2.0), 1.45, layer="07_INSTRUMENTACAO")

    line(layout, (25.0, 128.0), (64.0, 128.0), "07_INSTRUMENTACAO")
    layout.add_blockref("P01_POT", (72.0, 128.0), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    line(layout, (80.0, 128.0), (145.0, 128.0), "07_INSTRUMENTACAO")
    centered_text(layout, "P1 / 0-10 V LOCAL", (105.0, 130.0), 1.45, "07_INSTRUMENTACAO")
    line(layout, (25.0, 109.0), (145.0, 109.0), "07_INSTRUMENTACAO")
    centered_text(layout, "X3:10-11 / 4-20 mA REMOTO", (85.0, 115.0), 1.4, "07_INSTRUMENTACAO")
    add_rect(layout, 145.0, 104.0, 207.0, 134.0, "07_INSTRUMENTACAO")
    centered_text(layout, "S3 - FONTE DE REFERÊNCIA", (176.0, 128.0), 1.55, "07_INSTRUMENTACAO")
    centered_text(layout, "LOCAL / REMOTO", (176.0, 118.0), 1.5, "02_TEXTO")
    line(layout, (207.0, 118.0), (270.0, 118.0), "07_INSTRUMENTACAO")
    centered_text(layout, "VFD1-AI1 (OEM)", (238.5, 124.0), 1.4, "07_INSTRUMENTACAO")
    centered_text(
        layout,
        "DI/STO E PINAGEM: DEFINIR CONFORME MANUAIS DO VFD1 E KSR1",
        (210.0, 99.0),
        1.35,
        "13_NOTAS",
    )

    add_rect(layout, 292.0, 112.0, 401.0, 254.0, "12_LEGENDA")
    centered_text(layout, "SINALIZAÇÃO", (346.5, 247.0), 2.3, "12_LEGENDA")
    statuses = (("H1", "PAINEL ENERGIZADO", 224.0), ("H2", "VFD PRONTO", 196.0), ("H3", "MOTOR EM MARCHA", 168.0), ("H4", "FALHA VFD", 140.0))
    for tag, label, y in statuses:
        layout.add_blockref("P01_LAMPADA", (310.0, y), dxfattribs={"layer": "06_COMANDO"})
        add_text(layout, tag, (320.0, y + 2.0), 1.8, layer="06_COMANDO")
        add_text(layout, label, (320.0, y - 3.0), 1.55, layer="02_TEXTO")
    centered_text(layout, "H2/H3/H4 comandadas por RO/DO de VFD1", (346.5, 119.0), 1.5, "13_NOTAS")


def draw_layout(layout) -> None:
    add_rect(layout, 52.0, 105.0, 368.0, 261.0, "11_ARQUITETURA")
    centered_text(layout, "PLACA DE MONTAGEM - 800 x 600 mm", (210.0, 255.0), 2.2, "11_ARQUITETURA")

    for x0, x1 in ((62.0, 82.0), (338.0, 358.0)):
        add_rect(layout, x0, 117.0, x1, 244.0, "10_ELETROCALHAS")
        centered_text(layout, "CANALETA", ((x0 + x1) / 2.0, 180.0), 1.4, "10_ELETROCALHAS")
    for y0, y1 in ((222.0, 236.0), (174.0, 188.0), (124.0, 138.0)):
        add_rect(layout, 82.0, y0, 338.0, y1, "10_ELETROCALHAS")

    for y in (217.0, 169.0, 119.0):
        line(layout, (88.0, y), (332.0, y), "03_COTAS")

    equipment_box(layout, 92.0, 194.0, 122.0, 216.0, "Q0", "32 A")
    equipment_box(layout, 130.0, 194.0, 160.0, 216.0, "Q1", "25 A")
    equipment_box(layout, 168.0, 194.0, 198.0, 216.0, "DPS1", "T2")
    equipment_box(layout, 206.0, 194.0, 242.0, 216.0, "Q2", "2 A")
    equipment_box(layout, 250.0, 194.0, 291.0, 216.0, "PS1", "24 Vcc")
    equipment_box(layout, 299.0, 194.0, 330.0, 216.0, "KSR1", "STO", layer="06_COMANDO")

    equipment_box(layout, 125.0, 141.0, 244.0, 169.0, "VFD1", "11 kW / ventilação vertical")
    centered_text(layout, "≥100 mm LIVRE", (184.5, 179.0), 1.7, "03_COTAS")
    centered_text(layout, "≥100 mm LIVRE", (184.5, 130.0), 1.7, "03_COTAS")
    equipment_box(layout, 255.0, 145.0, 326.0, 167.0, "TB-PE", "Barra de terra", layer="05_POTENCIA")

    add_rect(layout, 92.0, 108.0, 330.0, 122.0, "09_BORNES")
    for x in range(104, 330, 14):
        line(layout, (float(x), 108.0), (float(x), 122.0), "09_BORNES")
    centered_text(layout, "X1 | X2 | X3 - RÉGUAS DE BORNES", (211.0, 115.0), 1.8, "09_BORNES")

    line(layout, (45.0, 105.0), (45.0, 261.0), "03_COTAS")
    line(layout, (41.0, 105.0), (49.0, 105.0), "03_COTAS")
    line(layout, (41.0, 261.0), (49.0, 261.0), "03_COTAS")
    centered_text(layout, "600 mm", (40.0, 183.0), 1.8, "03_COTAS")
    line(layout, (52.0, 265.0), (368.0, 265.0), "03_COTAS")
    centered_text(layout, "800 mm", (210.0, 263.0), 1.8, "03_COTAS")


def terminal_group(layout, x0: float, x1: float, y_top: float, title: str, rows: list[tuple[str, str, str]], row_h: float = 8.0) -> None:
    header_h = 12.0
    y_bottom = y_top - header_h - row_h * len(rows)
    add_rect(layout, x0, y_bottom, x1, y_top, "09_BORNES")
    line(layout, (x0, y_top - header_h), (x1, y_top - header_h), "09_BORNES")
    c1 = x0 + 17.0
    c2 = x0 + (x1 - x0) * 0.63
    line(layout, (c1, y_bottom), (c1, y_top - header_h), "09_BORNES")
    line(layout, (c2, y_bottom), (c2, y_top - header_h), "09_BORNES")
    centered_text(layout, title, ((x0 + x1) / 2.0, y_top - 6.0), 2.2, "09_BORNES")
    for index, (terminal, function, cable) in enumerate(rows):
        y1 = y_top - header_h - index * row_h
        y0 = y1 - row_h
        if index:
            line(layout, (x0, y1), (x1, y1), "09_BORNES")
        centered_text(layout, terminal, ((x0 + c1) / 2.0, (y0 + y1) / 2.0), 1.55, "09_BORNES")
        centered_text(layout, function, ((c1 + c2) / 2.0, (y0 + y1) / 2.0), 1.45, "02_TEXTO")
        centered_text(layout, cable, ((c2 + x1) / 2.0, (y0 + y1) / 2.0), 1.45, "08_CABOS")


def draw_terminals(layout) -> None:
    terminal_group(
        layout,
        18.0,
        105.0,
        257.0,
        "X1 - ENTRADA",
        [("1", "L1", "W01-1"), ("2", "L2", "W01-2"), ("3", "L3", "W01-3"), ("4", "PE", "W01-PE")],
        10.0,
    )
    terminal_group(
        layout,
        111.0,
        228.0,
        257.0,
        "X2 - MOTOR / PTC",
        [("1", "U", "W02-1"), ("2", "V", "W02-2"), ("3", "W", "W02-3"), ("4", "PE/SH", "W02-PE"), ("5", "PTC1", "W03-1"), ("6", "PTC2", "W03-2")],
        10.0,
    )
    x3_rows = [
        ("1", "+24 Vcc", "W04-1"),
        ("2", "0 V", "W04-2"),
        ("3", "E-STOP CH1", "W04-3"),
        ("4", "RET. CH1", "W04-4"),
        ("5", "E-STOP CH2", "W04-5"),
        ("6", "RET. CH2", "W04-6"),
        ("7", "RUN REMOTO", "W05-1"),
        ("8", "STOP REMOTO", "W05-2"),
        ("9", "RESET REMOTO", "W05-3"),
        ("10", "AI1 +", "W06-1"),
        ("11", "AI1 -", "W06-2"),
        ("12", "RUN NO", "W05-4"),
        ("13", "FALHA NO", "W05-5"),
        ("14", "COMUM RO", "W05-6"),
        ("15", "SHIELD", "W06-SH"),
    ]
    terminal_group(layout, 234.0, 405.0, 257.0, "X3 - COMANDO / SINAIS", x3_rows, 8.2)
    centered_text(layout, "PONTES: nenhuma ponte permanente nos canais de emergência", (123.0, 116.0), 1.6, "13_NOTAS")
    centered_text(layout, "SEGREGAÇÃO: X1/X2 potência; X3 controle e instrumentação", (123.0, 108.0), 1.6, "13_NOTAS")


def orthogonal_cable(layout, points: list[tuple[float, float]], cable: str, label_point: tuple[float, float], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)
    cable_label(layout, cable, label_point)


def draw_field(layout) -> None:
    equipment_box(layout, 149.0, 146.0, 272.0, 228.0, "PAINEL P01", "Q0/Q1/VFD1/KSR1/X1-X3")
    equipment_box(layout, 22.0, 184.0, 94.0, 224.0, "QDG", "Rede 380 V 3~ + PE")
    equipment_box(layout, 332.0, 184.0, 398.0, 224.0, "M1", "Motor 7,5 kW + PTC")
    equipment_box(layout, 23.0, 239.0, 105.0, 260.0, "S0", "Emergência 2 canais", layer="06_COMANDO")
    equipment_box(layout, 315.0, 239.0, 399.0, 260.0, "PLC REMOTO", "Comandos e estados", layer="07_INSTRUMENTACAO")
    equipment_box(layout, 26.0, 108.0, 105.0, 137.0, "MALHA PE", "TN-S / equipotencial")
    equipment_box(layout, 315.0, 108.0, 399.0, 137.0, "REFERÊNCIA", "4-20 mA remota", layer="07_INSTRUMENTACAO")

    orthogonal_cable(layout, [(94.0, 204.0), (149.0, 204.0)], "W01 - 4G4", (121.5, 210.0), "05_POTENCIA")
    orthogonal_cable(layout, [(272.0, 204.0), (332.0, 204.0)], "W02 - VFD", (302.0, 210.0), "05_POTENCIA")
    orthogonal_cable(layout, [(272.0, 181.0), (314.0, 181.0), (314.0, 192.0), (332.0, 192.0)], "W03 - PTC", (293.0, 176.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(105.0, 249.0), (128.0, 249.0), (128.0, 218.0), (149.0, 218.0)], "W04", (126.0, 255.0), "06_COMANDO")
    orthogonal_cable(layout, [(315.0, 249.0), (292.0, 249.0), (292.0, 218.0), (272.0, 218.0)], "W05", (294.0, 255.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(315.0, 122.0), (291.0, 122.0), (291.0, 158.0), (272.0, 158.0)], "W06", (294.0, 116.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(105.0, 122.0), (127.0, 122.0), (127.0, 158.0), (149.0, 158.0)], "PE", (125.0, 116.0), "05_POTENCIA")

    centered_text(layout, "X1", (143.0, 205.0), 1.8, "09_BORNES")
    centered_text(layout, "X2", (278.0, 205.0), 1.8, "09_BORNES")
    centered_text(layout, "X3:3-6", (141.0, 222.0), 1.6, "09_BORNES")
    centered_text(layout, "X3:7-14", (280.0, 222.0), 1.6, "09_BORNES")
    centered_text(layout, "X3:10-11/15", (286.0, 162.0), 1.5, "09_BORNES")
    centered_text(layout, "TB-PE", (141.0, 162.0), 1.6, "09_BORNES")


def draw_protection_coordination(layout, rows: list[dict[str, str]]) -> None:
    nodes = (
        (20.0, 68.0, "QDG", "origem"),
        (99.0, 147.0, "Q0", "secciona"),
        (178.0, 226.0, "Q1", "disjuntor"),
        (257.0, 315.0, "VFD1", "inversor"),
        (346.0, 404.0, "M1", "motor"),
    )
    for x0, x1, tag, function in nodes:
        add_rect(layout, x0, 249.0, x1, 261.0, "04_EQUIPAMENTOS")
        centered_text(layout, tag, ((x0 + x1) / 2.0, 257.0), 2.0, "04_EQUIPAMENTOS")
        centered_text(layout, function, ((x0 + x1) / 2.0, 252.0), 1.2, "02_TEXTO")
    for (_, x0_next, _, _), (x1_prev, _, _, _) in zip(nodes, nodes[1:]):
        y = 255.0
        line(layout, (x1_prev, y), (x0_next - 2.0, y), "05_POTENCIA")
        line(layout, (x0_next - 2.0, y), (x0_next - 5.0, y + 1.8), "05_POTENCIA")
        line(layout, (x0_next - 2.0, y), (x0_next - 5.0, y - 1.8), "05_POTENCIA")
    centered_text(
        layout,
        "AUXILIAR: Q2 → PS1 / 24 Vcc     |     DPS1 → PE",
        (210.0, 241.5),
        1.7,
        "02_TEXTO",
    )

    x_edges = (18.0, 60.0, 143.0, 279.0, 410.0)
    table_top = 232.0
    header_height = 10.0
    row_height = 15.0
    table_bottom = table_top - header_height - row_height * len(rows)
    add_rect(layout, x_edges[0], table_bottom, x_edges[-1], table_top, "01_CARIMBO")
    for x in x_edges[1:-1]:
        line(layout, (x, table_bottom), (x, table_top), "01_CARIMBO")
    line(layout, (x_edges[0], table_top - header_height), (x_edges[-1], table_top - header_height), "01_CARIMBO")

    headers = ("ELEMENTO", "PREMISSA ATUAL", "DADO PARA SUBSTITUIR", "O QUE AINDA NÃO ESTÁ COMPROVADO")
    for index, label in enumerate(headers):
        add_mtext(
            layout,
            label,
            (x_edges[index] + 2.0, table_top - 2.0),
            x_edges[index + 1] - x_edges[index] - 4.0,
            1.5,
            "01_CARIMBO",
            style=TITLE_STYLE,
        )

    for row_index, row in enumerate(rows):
        row_top = table_top - header_height - row_height * row_index
        row_bottom = row_top - row_height
        line(layout, (x_edges[0], row_bottom), (x_edges[-1], row_bottom), "01_CARIMBO")
        centered_text(layout, row["elemento"], ((x_edges[0] + x_edges[1]) / 2.0, (row_top + row_bottom) / 2.0), 1.7, "02_TEXTO")
        for index, key in ((1, "premissa_atual"), (2, "dado_para_substituir"), (3, "verificacao_pendente")):
            add_mtext(
                layout,
                row[key],
                (x_edges[index] + 2.0, row_top - 1.8),
                x_edges[index + 1] - x_edges[index] - 4.0,
                1.45,
                "13_NOTAS" if index == 3 else "02_TEXTO",
            )

    add_rect(layout, 18.0, 98.0, 410.0, 109.0, "13_NOTAS")
    add_mtext(
        layout,
        "Icu = 10 kA / Icc presumida = 5 kA resulta apenas em uma razão aritmética de 2:1; sem dados, curvas e tabelas do fabricante, isso não prova capacidade, seletividade, retaguarda ou coordenação.",
        (21.0, 106.5),
        386.0,
        1.45,
        "13_NOTAS",
    )


def draw_verification_plan(layout, rows: list[dict[str, str]]) -> None:
    stages = (
        ("1  BASE E REVISÕES", "documentos coerentes"),
        ("2  DADOS REAIS / OEM", "rede, placas e manuais"),
        ("3  CÁLCULO / SELEÇÃO", "critérios documentados"),
        ("4  VERIFICAÇÃO", "ensaios registrados"),
        ("5  AS-BUILT", "pendências encerradas"),
    )
    stage_x = (18.0, 98.0, 178.0, 258.0, 338.0)
    for index, ((title, subtitle), x0) in enumerate(zip(stages, stage_x)):
        add_rect(layout, x0, 247.0, x0 + 70.0, 262.0, "04_EQUIPAMENTOS")
        centered_text(layout, title, (x0 + 35.0, 257.7), 1.75, "04_EQUIPAMENTOS")
        centered_text(layout, subtitle, (x0 + 35.0, 251.1), 1.35, "02_TEXTO")
        if index < len(stages) - 1:
            x1 = x0 + 70.0
            x2 = stage_x[index + 1]
            line(layout, (x1 + 1.0, 254.5), (x2 - 2.0, 254.5), "05_POTENCIA")
            line(layout, (x2 - 2.0, 254.5), (x2 - 5.0, 256.3), "05_POTENCIA")
            line(layout, (x2 - 2.0, 254.5), (x2 - 5.0, 252.7), "05_POTENCIA")

    x_edges = (18.0, 37.0, 100.0, 235.0, 380.0, 410.0)
    table_top = 236.0
    header_height = 8.0
    row_height = 8.3
    table_bottom = table_top - header_height - row_height * len(rows)
    add_rect(layout, x_edges[0], table_bottom, x_edges[-1], table_top, "01_CARIMBO")
    for x in x_edges[1:-1]:
        line(layout, (x, table_bottom), (x, table_top), "01_CARIMBO")
    line(
        layout,
        (x_edges[0], table_top - header_height),
        (x_edges[-1], table_top - header_height),
        "01_CARIMBO",
    )
    headers = ("ID", "PONTO / ETAPA", "DADOS REQUERIDOS", "EVIDÊNCIA PARA ENCERRAR", "STATUS")
    for index, label in enumerate(headers):
        add_mtext(
            layout,
            label,
            (x_edges[index] + 1.5, table_top - 1.8),
            x_edges[index + 1] - x_edges[index] - 3.0,
            1.45,
            "01_CARIMBO",
            style=TITLE_STYLE,
        )

    for row_index, row in enumerate(rows):
        row_top = table_top - header_height - row_height * row_index
        row_bottom = row_top - row_height
        line(layout, (x_edges[0], row_bottom), (x_edges[-1], row_bottom), "01_CARIMBO")
        centered_text(
            layout,
            row["codigo"],
            ((x_edges[0] + x_edges[1]) / 2.0, (row_top + row_bottom) / 2.0),
            1.35,
            "04_EQUIPAMENTOS",
        )
        for index, key in ((1, "ponto"), (2, "dados_requeridos"), (3, "evidencia_para_encerrar")):
            add_mtext(
                layout,
                row[key],
                (x_edges[index] + 1.5, row_top - 1.2),
                x_edges[index + 1] - x_edges[index] - 3.0,
                1.4,
                "13_NOTAS" if index == 3 else "02_TEXTO",
            )
        centered_text(
            layout,
            row["status"],
            ((x_edges[4] + x_edges[5]) / 2.0, (row_top + row_bottom) / 2.0),
            1.35,
            "13_NOTAS",
        )

    add_rect(layout, 18.0, 102.0, 410.0, 111.0, "13_NOTAS")
    add_mtext(
        layout,
        "STATUS NÃO EXECUTADO: nenhum ensaio/aceite de campo foi registrado neste estudo. O status não equivale a aprovação; não energizar ou comissionar com base nesta prancha.",
        (21.0, 108.5),
        386.0,
        1.45,
        "13_NOTAS",
    )


def draw_operational_sequence(layout, rows: dict[str, list[dict[str, str]]]) -> None:
    def arrow_right(x0: float, x1: float, y: float) -> None:
        line(layout, (x0, y), (x1, y), "06_COMANDO")
        line(layout, (x1, y), (x1 - 3.0, y + 1.8), "06_COMANDO")
        line(layout, (x1, y), (x1 - 3.0, y - 1.8), "06_COMANDO")

    setup_x = (18.0, 116.0, 214.0, 312.0)
    for index, (row, x0) in enumerate(zip(rows["habilitacao"], setup_x)):
        add_rect(layout, x0, 239.0, x0 + 88.0, 262.0, "04_EQUIPAMENTOS")
        centered_text(layout, f"{row['codigo']}  {row['titulo']}", (x0 + 44.0, 256.5), 1.6, "04_EQUIPAMENTOS")
        add_mtext(layout, row["descricao"], (x0 + 4.0, 251.0), 80.0, 1.3, "02_TEXTO")
        if index < len(setup_x) - 1:
            arrow_right(x0 + 89.0, setup_x[index + 1] - 2.0, 250.5)

    operation_x = (18.0, 118.0, 218.0, 318.0)
    for index, (row, x0) in enumerate(zip(rows["operacao"], operation_x)):
        width = 90.0 if index < len(operation_x) - 1 else 92.0
        add_rect(layout, x0, 190.0, x0 + width, 220.0, "04_EQUIPAMENTOS")
        centered_text(layout, f"{row['codigo']}  {row['titulo']}", (x0 + width / 2.0, 213.5), 1.65, "04_EQUIPAMENTOS")
        add_mtext(layout, row["descricao"], (x0 + 3.0, 208.5), width - 6.0, 1.35, "02_TEXTO")
        if index < len(operation_x) - 1:
            arrow_right(x0 + width + 1.0, operation_x[index + 1] - 2.0, 205.0)

    stop_center = operation_x[-1] + 46.0
    ready_center = operation_x[0] + 45.0
    line(layout, (stop_center, 189.0), (stop_center, 178.0), "06_COMANDO")
    line(layout, (stop_center, 178.0), (ready_center, 178.0), "06_COMANDO")
    line(layout, (ready_center, 178.0), (ready_center, 187.0), "06_COMANDO")
    line(layout, (ready_center, 187.0), (ready_center - 3.0, 184.0), "06_COMANDO")
    line(layout, (ready_center, 187.0), (ready_center + 3.0, 184.0), "06_COMANDO")
    centered_text(layout, "comando inativo: retorno ao estado PRONTO", (210.0, 181.5), 1.35, "02_TEXTO")

    event_x = (18.0, 117.0, 216.0, 315.0)
    event_width = 95.0
    for row, x0 in zip(rows["evento"], event_x):
        add_rect(layout, x0, 128.0, x0 + event_width, 168.0, "01_CARIMBO")
        centered_text(layout, f"{row['codigo']}  {row['titulo']}", (x0 + event_width / 2.0, 163.0), 1.45, "13_NOTAS")
        add_mtext(layout, row["descricao"], (x0 + 3.0, 157.5), event_width - 6.0, 1.35, "02_TEXTO")

    add_rect(layout, 18.0, 104.0, 410.0, 120.0, "13_NOTAS")
    note = rows["nota"][0]
    centered_text(layout, f"{note['codigo']}  {note['titulo']}", (31.0, 113.0), 1.45, "13_NOTAS")
    add_mtext(layout, note["descricao"], (48.0, 116.0), 358.0, 1.35, "13_NOTAS")


DRAWERS = {
    1: draw_unifilar,
    2: draw_power,
    3: draw_command,
    4: draw_layout,
    5: draw_terminals,
    6: draw_field,
}


def read_coordination_rows(project_dir: Path) -> list[dict[str, str]]:
    source = project_dir / "protecao-coordenacao.csv"
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        expected_fields = (
            "elemento",
            "premissa_atual",
            "dado_para_substituir",
            "verificacao_pendente",
        )
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError(f"Cabecalho inesperado em {source}")
        rows = list(reader)
    if len(rows) != 7 or any(not all(row.get(field, "").strip() for field in expected_fields) for row in rows):
        raise ValueError(f"A matriz de protecao deve conter sete linhas completas: {source}")
    return rows


def read_verification_rows(project_dir: Path) -> list[dict[str, str]]:
    source = project_dir / "plano-verificacao.csv"
    expected_fields = (
        "codigo",
        "ponto",
        "dados_requeridos",
        "evidencia_para_encerrar",
        "status",
    )
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError(f"Cabecalho inesperado em {source}")
        rows = list(reader)
    codes = [row.get("codigo", "").strip() for row in rows]
    if (
        len(rows) != 13
        or len(set(codes)) != len(rows)
        or any(not all(row.get(field, "").strip() for field in expected_fields) for row in rows)
        or any(row["status"] != "NÃO EXECUTADO" for row in rows)
    ):
        raise ValueError(f"A matriz de verificacao deve conter treze linhas completas e nao executadas: {source}")
    return rows


def read_operational_sequence_rows(project_dir: Path) -> dict[str, list[dict[str, str]]]:
    source = project_dir / "sequencia-estados.csv"
    expected_fields = ("grupo", "ordem", "codigo", "titulo", "descricao")
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError(f"Cabecalho inesperado em {source}")
        source_rows = list(reader)

    grouped: dict[str, list[dict[str, str]]] = {"habilitacao": [], "operacao": [], "evento": [], "nota": []}
    for row in source_rows:
        if row.get("grupo") not in grouped:
            raise ValueError(f"Grupo inesperado em {source}: {row.get('grupo')}")
        if not all(row.get(field, "").strip() for field in expected_fields):
            raise ValueError(f"Linha incompleta em {source}: {row}")
        grouped[row["grupo"]].append(row)

    expected_counts = {"habilitacao": 4, "operacao": 4, "evento": 4, "nota": 1}
    for group, expected_count in expected_counts.items():
        group_rows = grouped[group]
        orders = [int(row["ordem"]) for row in group_rows]
        codes = [row["codigo"] for row in group_rows]
        if len(group_rows) != expected_count or orders != list(range(1, expected_count + 1)) or len(set(codes)) != len(codes):
            raise ValueError(f"Grupo {group} deve ter {expected_count} linhas ordenadas e codigos unicos: {source}")
    return grouped


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    coordination_rows = read_coordination_rows(root / PROJECT_SLUG)
    verification_rows = read_verification_rows(root / PROJECT_SLUG)
    sequence_rows = read_operational_sequence_rows(root / PROJECT_SLUG)
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        if spec.number == 7:
            draw_protection_coordination(layout, coordination_rows)
        elif spec.number == 8:
            draw_verification_plan(layout, verification_rows)
        elif spec.number == 9:
            draw_operational_sequence(layout, sequence_rows)
        else:
            DRAWERS[spec.number](layout)
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
    args = parse_args()
    generate(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
