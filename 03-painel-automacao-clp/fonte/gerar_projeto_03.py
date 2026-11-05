"""Gera as nove pranchas DXF do Projeto 03 de forma determinística."""

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


PROJECT_SLUG = "03-painel-automacao-clp"
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
    SheetSpec(1, "01_arquitetura_automacao.dxf", "ARQUITETURA DE AUTOMAÇÃO",
              "Potência, controle, segurança e interfaces de processo",
              "Rede assumida 220 V 3~ 60 Hz TN-S. CLP genérico 24 Vcc, 16 DI / 16 DO.\\P"
              "A arquitetura é conceitual e exige análise de risco e dimensionamento final.",
              "QF: proteção | KM: contator | RT: sobrecarga | KSR: segurança | LS: nível"),
    SheetSpec(2, "02_alimentacao_24v.dxf", "ALIMENTAÇÃO 24 Vcc",
              "Distribuição protegida da fonte aos circuitos de automação",
              "PSU1: 10 A; carga considerada: 6 A; reserva conceitual: 4 A.\\P"
              "Confirmar corrente de energização, temperatura, seletividade e PELV no projeto real.",
              "+24V/0V: comando | QF4: CLP | QF5: sensores | QF6: relés | QF7: sinalização"),
    SheetSpec(3, "03_entradas_clp.dxf", "ENTRADAS DO CLP",
              "Mapa das 16 entradas digitais PNP e respectivos bornes",
              "Entradas NF são normalizadas no programa. Filtrar ruído e diagnosticar incoerências.\\P"
              "KSR1 e KDRY atuam fisicamente; o CLP apenas monitora seus retornos.",
              "DI: entrada digital | NF: normalmente fechado | FB: retorno | ACK: reconhecimento"),
    SheetSpec(4, "04_saidas_clp.dxf", "SAÍDAS DO CLP",
              "Mapa das 16 saídas digitais PNP, interfaces e sinalização",
              "K1/K2/KA1 usam interface com supressão de surto. Dimensionar cada canal pela folha\\P"
              "de dados do CLP; saídas reserva permanecem sem carga e identificadas.",
              "DO: saída digital | K: relé interface | H: sinalizador | BZ: buzzer | RES: reserva"),
    SheetSpec(5, "05_diagrama_comando.dxf", "DIAGRAMA DE COMANDO",
              "Cadeias 24 Vcc, permissivos físicos e comandos das bombas",
              "S0/KSR1 interrompe as bobinas sem depender do CLP. KDRY bloqueia funcionamento a seco.\\P"
              "Não se declara categoria, PL ou SIL sem análise de risco e validação específicas.",
              "S0: emergência | KSR: segurança | KDRY: nível crítico | K1/K2: interfaces | KM: contatores"),
    SheetSpec(6, "06_layout_painel.dxf", "LAYOUT DO PAINEL",
              "Arranjo conceitual em placa de montagem 800 x 600 mm",
              "Confirmar invólucro, IP, dissipação, EMC, ocupação, folgas e raio de curvatura.\\P"
              "Separar potência à esquerda, controle ao centro e sinais/bornes à direita.",
              "Tracejado: trilho DIN | cinza: canaleta | TB-PE: barra PE | X: réguas de bornes"),
    SheetSpec(7, "07_diagrama_bornes.dxf", "DIAGRAMA DE BORNES",
              "Réguas X1 a X4, potenciais, funções e cabos associados",
              "Identificar condutores nas duas extremidades. Não usar PE como condutor ativo.\\P"
              "Pontes, se necessárias, devem ser documentadas após definição do hardware real.",
              "X1: entrada | X2: motores | X3: entradas | X4: saídas | W: cabo"),
    SheetSpec(8, "08_interligacoes_campo.dxf", "INTERLIGAÇÕES DE CAMPO",
              "Painel, reservatório, bombas, emergência e supervisão remota",
              "Comprimentos de W01-W12 são premissas. Confirmar rotas, segregação, EMC, queda\\P"
              "de tensão, tipo de sensor e equipotencialização após levantamento de campo.",
              "Linha cheia: potência | tracejado funcional: controle | LS: nível | PE: proteção"),
    SheetSpec(9, "09_sequencia_operacao_intertravamentos.dxf", "SEQUÊNCIA DE OPERAÇÃO E INTERTRAVAMENTOS",
              "Estados do CLP, demanda, alternância, confirmação e resposta a falhas",
              "Lógica funcional conceitual; não é programa executável nem função de segurança validada.\\P"
              "S1 MAN usa S2/S3 e S4/S5 sob os mesmos permissivos; sensores incoerentes bloqueiam novas partidas AUTO, e a resposta para bomba em marcha segue pendente.",
              "LSL: encerra demanda | LSHH por 10 s: solicita reserva | Kx/KMx_FB: comando/retorno | S6: reconhecer e rearmar"),
)


CAUSE_EFFECTS = (
    ("EMERGÊNCIA", "S0 acionado / KSR1_OK = 0", "KSR1 abre as cadeias de KM1 e KM2; falha memorizada", "Liberar S0, confirmar retornos e reconhecer em S6"),
    ("NÍVEL CRÍTICO", "LSL_LL / KDRY_OK = 0", "KDRY bloqueia fisicamente as duas bobinas", "Nível de captação recuperado e rearme permitido"),
    ("SOBRECARGA", "RT1_OK ou RT2_OK = 0", "Remove a bomba afetada; em AUTO solicita a reserva disponível", "Rearmar RT e conferir o retorno do contator"),
    ("FALHA DE PARTIDA", "Kx_CMD sem KMx_FB em até 2 s", "Bloqueia a bomba e tenta a reserva se houver demanda", "Remover causa e reconhecer; validar KMx_FB"),
    ("RETORNO INDEVIDO", "KMx_FB ativo sem Kx_CMD", "Memoriza falha e exige intervenção", "Investigar circuito/retorno antes de S6"),
    ("SENSOR INCOERENTE", "Combinação de nível impossível", "Bloqueia nova partida AUTO; efeito sobre bomba em marcha não definido", "Decisão de projeto pendente; validar plausibilidade antes do rearme"),
    ("TEMPO / SEM BOMBA", "Demanda > 30 min ou nenhuma bomba disponível", "Para as bombas e mantém H5/BZ1 como alarme retentivo", "Remover causa, alinhar retornos e reconhecer em S6"),
    ("ACK / REARME", "S6 mantido por pelo menos 0,5 s", "Silencia BZ1; só limpa falha após remoção da causa e coerência dos retornos", "H5 permanece ativo enquanto houver falha ativa ou memorizada"),
)


INPUTS = (
    ("I0.0", "KSR1_OK", "Relé segurança saudável", "X3:1"),
    ("I0.1", "S1_AUTO", "Seletor automático", "X3:2"),
    ("I0.2", "S1_MAN", "Seletor manual", "X3:3"),
    ("I0.3", "S2_P1", "Partida manual M1", "X3:4"),
    ("I0.4", "S3_P1", "Parada manual M1 (NF)", "X3:5"),
    ("I0.5", "S4_P2", "Partida manual M2", "X3:6"),
    ("I0.6", "S5_P2", "Parada manual M2 (NF)", "X3:7"),
    ("I0.7", "LSL_LL", "Nível baixo-baixo", "X3:8"),
    ("I1.0", "LSL", "Nível baixo / parar", "X3:9"),
    ("I1.1", "LSH", "Nível alto / partir", "X3:10"),
    ("I1.2", "LSHH", "Nível alto-alto", "X3:11"),
    ("I1.3", "RT1_OK", "Sobrecarga M1 saudável", "X3:12"),
    ("I1.4", "RT2_OK", "Sobrecarga M2 saudável", "X3:13"),
    ("I1.5", "KM1_FB", "Retorno contator M1", "X3:14"),
    ("I1.6", "KM2_FB", "Retorno contator M2", "X3:15"),
    ("I1.7", "S6_ACK", "Reconhecer / rearmar", "X3:16"),
)

OUTPUTS = (
    ("Q0.0", "K1_CMD", "Relé interface bomba 1", "X4:1"),
    ("Q0.1", "K2_CMD", "Relé interface bomba 2", "X4:2"),
    ("Q0.2", "H1_PRONTO", "Lâmpada painel pronto", "X4:3"),
    ("Q0.3", "H2_AUTO", "Lâmpada modo automático", "X4:4"),
    ("Q0.4", "H3_P1", "Lâmpada bomba 1", "X4:5"),
    ("Q0.5", "H4_P2", "Lâmpada bomba 2", "X4:6"),
    ("Q0.6", "H5_ALARME", "Lâmpada alarme geral", "X4:7"),
    ("Q0.7", "H6_DEMANDA", "Lâmpada de demanda", "X4:8"),
    ("Q1.0", "BZ1", "Buzzer de alarme", "X4:9"),
    ("Q1.1", "KA1_REM", "Relé alarme remoto", "X4:10"),
    ("Q1.2", "RES_DO_01", "Saída reserva 01", "X4:11"),
    ("Q1.3", "RES_DO_02", "Saída reserva 02", "X4:12"),
    ("Q1.4", "RES_DO_03", "Saída reserva 03", "X4:13"),
    ("Q1.5", "RES_DO_04", "Saída reserva 04", "X4:14"),
    ("Q1.6", "RES_DO_05", "Saída reserva 05", "X4:15"),
    ("Q1.7", "RES_DO_06", "Saída reserva 06", "X4:16"),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str = "06_COMANDO") -> None:
    add_line(layout, a, b, layer)


def centered(layout, value: str, point: tuple[float, float], height: float = 1.7,
             layer: str = "02_TEXTO") -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def box(layout, x0: float, y0: float, x1: float, y1: float, tag: str, description: str,
        layer: str = "04_EQUIPAMENTOS", *, text_height: float = 1.55) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5.0), 2.2, layer)
    centered(layout, description, ((x0 + x1) / 2, y0 + 5.0), text_height, "02_TEXTO")


def label(layout, value: str, point: tuple[float, float], layer: str = "08_CABOS") -> None:
    centered(layout, value, point, 1.45, layer)


def orthogonal(layout, points: list[tuple[float, float]], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    if "P03_MOTOR" not in doc.blocks:
        block = doc.blocks.new("P03_MOTOR", base_point=(0, 0))
        block.add_circle((0, 0), 9, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        centered(block, "M", (0, 1.8), 4.2, "04_EQUIPAMENTOS")
        centered(block, "3~", (0, -4.0), 1.7, "04_EQUIPAMENTOS")
    if "P03_SENSOR" not in doc.blocks:
        block = doc.blocks.new("P03_SENSOR", base_point=(0, 0))
        block.add_circle((0, 0), 4, dxfattribs={"layer": "07_INSTRUMENTACAO"})
        line(block, (-4, 0), (4, 0), "07_INSTRUMENTACAO")
        line(block, (0, -4), (0, 4), "07_INSTRUMENTACAO")
    if "P03_LAMP" not in doc.blocks:
        block = doc.blocks.new("P03_LAMP", base_point=(0, 0))
        block.add_circle((0, 0), 3, dxfattribs={"layer": "06_COMANDO"})
        line(block, (-2.1, -2.1), (2.1, 2.1), "06_COMANDO")
        line(block, (-2.1, 2.1), (2.1, -2.1), "06_COMANDO")
    for name, normally_closed in (("P03_NA", False), ("P03_NF", True)):
        if name in doc.blocks:
            continue
        block = doc.blocks.new(name, base_point=(0, 0))
        line(block, (-6, 0), (-2, 0), "06_COMANDO")
        line(block, (2, 0), (6, 0), "06_COMANDO")
        line(block, (-2, 0), (2, 3), "06_COMANDO")
        if normally_closed:
            line(block, (-2, 3), (2, -1), "06_COMANDO")
    if "P03_COIL" not in doc.blocks:
        block = doc.blocks.new("P03_COIL", base_point=(0, 0))
        block.add_arc((-4, 0), 4, 270, 90, dxfattribs={"layer": "06_COMANDO"})
        block.add_arc((4, 0), 4, 90, 270, dxfattribs={"layer": "06_COMANDO"})


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRIÇÃO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("SEQUENCIA OPERACIONAL", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.65, "02_TEXTO")


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
        "PRANCHA": f"{spec.number:02d}/{len(SHEETS):02d}",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/{len(SHEETS):02d}"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 4.2, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 2.1, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_architecture(layout) -> None:
    centered(layout, "CAMADA DE POTÊNCIA", (210, 257), 2.3, "05_POTENCIA")
    box(layout, 20, 220, 75, 247, "Q0", "Rede 220 V 3~ + PE", "05_POTENCIA")
    box(layout, 95, 220, 150, 247, "QF1/KM1/RT1", "Ramal da bomba 1", "05_POTENCIA", text_height=1.35)
    box(layout, 170, 220, 225, 247, "QF2/KM2/RT2", "Ramal da bomba 2", "05_POTENCIA", text_height=1.35)
    layout.add_blockref("P03_MOTOR", (270, 233.5), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    layout.add_blockref("P03_MOTOR", (335, 233.5), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    centered(layout, "M1 / BOMBA 1", (270, 217), 1.7, "04_EQUIPAMENTOS")
    centered(layout, "M2 / BOMBA 2", (335, 217), 1.7, "04_EQUIPAMENTOS")
    for a, b in (((75, 233.5), (95, 233.5)), ((150, 233.5), (261, 233.5)), ((225, 226), (300, 226)), ((300, 226), (326, 233.5))):
        line(layout, a, b, "05_POTENCIA")

    centered(layout, "CAMADA DE CONTROLE E SEGURANÇA", (210, 203), 2.3, "06_COMANDO")
    box(layout, 20, 157, 75, 190, "PSU1", "24 Vcc / 10 A", "04_EQUIPAMENTOS")
    box(layout, 92, 151, 168, 196, "KSR1 + KDRY", "Emergência + nível crítico", "06_COMANDO", text_height=1.35)
    box(layout, 188, 145, 266, 202, "CLP1", "16 DI / 16 DO PNP", "07_INSTRUMENTACAO")
    box(layout, 286, 151, 353, 196, "K1/K2/KA1", "Relés de interface", "06_COMANDO")
    box(layout, 366, 151, 401, 196, "H/BZ", "Sinalização", "06_COMANDO", text_height=1.3)
    for a, b, layer in (((75, 173.5), (92, 173.5), "06_COMANDO"), ((168, 173.5), (188, 173.5), "06_COMANDO"),
                        ((266, 173.5), (286, 173.5), "07_INSTRUMENTACAO"), ((353, 173.5), (366, 173.5), "06_COMANDO")):
        line(layout, a, b, layer)

    centered(layout, "CAMPO / PROCESSO", (210, 134), 2.3, "07_INSTRUMENTACAO")
    sensors = ((55, "LSL-LL"), (115, "LSL"), (175, "LSH"), (235, "LSHH"))
    for x, tag in sensors:
        layout.add_blockref("P03_SENSOR", (x, 116), dxfattribs={"layer": "07_INSTRUMENTACAO"})
        centered(layout, tag, (x, 126), 1.6, "07_INSTRUMENTACAO")
        orthogonal(layout, [(x, 112), (x, 104), (227, 104), (227, 145)], "07_INSTRUMENTACAO")
    box(layout, 282, 105, 345, 132, "S0 / S1-S6", "Comandos na porta", "06_COMANDO", text_height=1.3)
    box(layout, 359, 105, 401, 132, "SUP.", "Alarme remoto", "07_INSTRUMENTACAO", text_height=1.25)
    orthogonal(layout, [(313.5, 132), (313.5, 141), (227, 141), (227, 145)], "06_COMANDO")
    orthogonal(layout, [(380, 132), (380, 142), (325, 142), (325, 151)], "07_INSTRUMENTACAO")


def draw_24v(layout) -> None:
    box(layout, 22, 207, 70, 242, "QF3", "2P / 4 A", "05_POTENCIA")
    box(layout, 92, 199, 158, 250, "PSU1", "100-240 Vca / 24 Vcc 10 A", "04_EQUIPAMENTOS", text_height=1.25)
    line(layout, (70, 224.5), (92, 224.5), "05_POTENCIA")
    centered(layout, "L1-L2 / 220 Vca", (46, 252), 1.7, "05_POTENCIA")
    line(layout, (158, 233), (388, 233), "06_COMANDO")
    line(layout, (158, 215), (388, 215), "06_COMANDO")
    centered(layout, "+24 Vcc", (177, 238), 1.7, "06_COMANDO")
    centered(layout, "0 V", (177, 210), 1.7, "06_COMANDO")
    branches = ((190, "QF4", "CLP1", "2 A"), (245, "QF5", "SENSORES", "1 A"),
                (300, "QF6", "RELÉS/KM", "2 A"), (355, "QF7", "H/BZ", "2 A"))
    for x, qf, load, rating in branches:
        line(layout, (x, 233), (x, 201), "06_COMANDO")
        box(layout, x - 17, 174, x + 17, 201, qf, rating, "06_COMANDO")
        line(layout, (x, 174), (x, 151), "06_COMANDO")
        box(layout, x - 22, 121, x + 22, 151, load, "24 Vcc", "04_EQUIPAMENTOS")
        line(layout, (x, 121), (x, 109), "06_COMANDO")
        line(layout, (x, 109), (388, 109), "06_COMANDO")
    line(layout, (158, 215), (166, 215), "06_COMANDO")
    line(layout, (166, 215), (166, 109), "06_COMANDO")
    centered(layout, "DISTRIBUIÇÃO RADIAL; 0 V COM REFERÊNCIA ÚNICA CONFORME HARDWARE", (275, 103), 1.5, "13_NOTAS")

    add_rect(layout, 22, 105, 145, 192, "12_LEGENDA")
    centered(layout, "ORÇAMENTO 24 Vcc", (83.5, 185), 2.0, "12_LEGENDA")
    rows = (("CLP/módulos", "1,20 A"), ("Sensores/comandos", "0,50 A"),
            ("Relés/segurança", "0,80 A"), ("Contatores", "0,50 A"),
            ("Sinalização/buzzer", "1,00 A"), ("Reserva", "2,00 A"), ("TOTAL", "6,00 A"))
    for i, (name, current) in enumerate(rows):
        y = 174 - i * 9
        line(layout, (26, y - 4), (141, y - 4), "12_LEGENDA")
        add_text(layout, name, (28, y), 1.45, layer="02_TEXTO")
        add_text(layout, current, (118, y), 1.45, layer="02_TEXTO")


def io_table(layout, x0: float, x1: float, y_top: float, title: str,
             rows: tuple[tuple[str, str, str, str], ...]) -> None:
    header = 13.0
    row_h = 15.0
    y_bottom = y_top - header - row_h * len(rows)
    add_rect(layout, x0, y_bottom, x1, y_top, "07_INSTRUMENTACAO")
    line(layout, (x0, y_top - header), (x1, y_top - header), "07_INSTRUMENTACAO")
    columns = (x0 + 25, x0 + 70, x1 - 29)
    for x in columns:
        line(layout, (x, y_bottom), (x, y_top - header), "07_INSTRUMENTACAO")
    centered(layout, title, ((x0 + x1) / 2, y_top - 6.5), 2.1, "07_INSTRUMENTACAO")
    for index, (address, tag, description, terminal) in enumerate(rows):
        y1 = y_top - header - index * row_h
        y0 = y1 - row_h
        if index:
            line(layout, (x0, y1), (x1, y1), "07_INSTRUMENTACAO")
        cy = (y0 + y1) / 2
        centered(layout, address, ((x0 + columns[0]) / 2, cy), 1.45, "07_INSTRUMENTACAO")
        centered(layout, tag, ((columns[0] + columns[1]) / 2, cy), 1.35, "02_TEXTO")
        centered(layout, description, ((columns[1] + columns[2]) / 2, cy), 1.30, "02_TEXTO")
        centered(layout, terminal, ((columns[2] + x1) / 2, cy), 1.40, "09_BORNES")


def draw_inputs(layout) -> None:
    io_table(layout, 18, 207, 257, "GRUPO DI0 - I0.0 A I0.7", INPUTS[:8])
    io_table(layout, 213, 402, 257, "GRUPO DI1 - I1.0 A I1.7", INPUTS[8:])
    centered(layout, "+24 Vcc -> dispositivo de campo -> DI; comum M -> 0 V", (210, 112), 1.75, "07_INSTRUMENTACAO")
    centered(layout, "Normal = 1: KSR1_OK, S3_P1, S5_P2, LSL_LL, RT1_OK e RT2_OK", (210, 105), 1.45, "13_NOTAS")


def draw_outputs(layout) -> None:
    io_table(layout, 18, 207, 257, "GRUPO DO0 - Q0.0 A Q0.7", OUTPUTS[:8])
    io_table(layout, 213, 402, 257, "GRUPO DO1 - Q1.0 A Q1.7", OUTPUTS[8:])
    centered(layout, "DO PNP -> carga 24 Vcc -> 0 V; K1/K2/KA1 com diodo de supressão", (210, 112), 1.65, "07_INSTRUMENTACAO")
    centered(layout, "Q1.2 a Q1.7: reserva identificada, sem conexão externa", (210, 105), 1.45, "13_NOTAS")


def contact(layout, x: float, y: float, tag: str, *, nc: bool = False) -> None:
    layout.add_blockref("P03_NF" if nc else "P03_NA", (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, tag, (x, y + 6), 1.55, "06_COMANDO")


def coil(layout, x: float, y: float, tag: str) -> None:
    layout.add_blockref("P03_COIL", (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, tag, (x, y + 7), 1.6, "06_COMANDO")


def draw_command(layout) -> None:
    left, right = 22.0, 276.0
    line(layout, (left, 105), (left, 258), "06_COMANDO")
    line(layout, (right, 105), (right, 258), "06_COMANDO")
    centered(layout, "+24 Vcc", (left, 263), 1.8, "06_COMANDO")
    centered(layout, "0 V", (right, 263), 1.8, "06_COMANDO")

    for y in (244, 224):
        line(layout, (left, y), (47, y), "06_COMANDO")
    contact(layout, 54, 244, "S0-A", nc=True)
    contact(layout, 54, 224, "S0-B", nc=True)
    line(layout, (60, 244), (112, 244), "06_COMANDO")
    line(layout, (60, 224), (112, 224), "06_COMANDO")
    box(layout, 112, 214, 175, 254, "KSR1", "Relé segurança 2 canais", "06_COMANDO", text_height=1.25)
    line(layout, (175, 244), (right, 244), "06_COMANDO")
    line(layout, (175, 224), (right, 224), "06_COMANDO")
    centered(layout, "SAÍDAS SEGURAS", (224, 234), 1.45, "13_NOTAS")

    for y, output, overload, interface, contactor in ((188, "Q0.0", "RT1", "K1", "KM1"),
                                                       (151, "Q0.1", "RT2", "K2", "KM2")):
        line(layout, (left, y), (45, y), "06_COMANDO")
        contact(layout, 52, y, "KSR1")
        line(layout, (58, y), (77, y), "06_COMANDO")
        contact(layout, 84, y, "KDRY")
        line(layout, (90, y), (109, y), "06_COMANDO")
        contact(layout, 116, y, overload, nc=True)
        line(layout, (122, y), (141, y), "06_COMANDO")
        contact(layout, 148, y, output)
        line(layout, (154, y), (178, y), "06_COMANDO")
        coil(layout, 186, y, interface)
        line(layout, (194, y), (213, y), "06_COMANDO")
        contact(layout, 220, y, interface)
        line(layout, (226, y), (245, y), "06_COMANDO")
        coil(layout, 253, y, contactor)
        line(layout, (261, y), (right, y), "06_COMANDO")
        centered(layout, "BOMBA 1" if y == 188 else "BOMBA 2", (148, y - 9), 1.35, "02_TEXTO")

    line(layout, (left, 116), (46, 116), "06_COMANDO")
    contact(layout, 53, 116, "LSL-LL")
    line(layout, (59, 116), (116, 116), "06_COMANDO")
    coil(layout, 124, 116, "KDRY")
    line(layout, (132, 116), (right, 116), "06_COMANDO")
    centered(layout, "Relé de nível energizado com captação disponível", (198, 108), 1.35, "13_NOTAS")

    add_rect(layout, 292, 109, 402, 257, "12_LEGENDA")
    centered(layout, "COMANDOS E ESTADOS", (347, 249), 2.0, "12_LEGENDA")
    entries = (("S1", "MAN-0-AUTO"), ("S2/S3", "PARTIR/PARAR M1"),
               ("S4/S5", "PARTIR/PARAR M2"), ("S6", "ACK / REARME"),
               ("H1", "PAINEL PRONTO"), ("H2", "MODO AUTO"),
               ("H3/H4", "M1/M2 EM MARCHA"), ("H5", "ALARME GERAL"),
               ("H6", "DEMANDA"), ("BZ1", "ALARME SONORO"))
    for index, (tag, description) in enumerate(entries):
        y = 231 - index * 12.0
        add_text(layout, tag, (300, y), 1.5, layer="06_COMANDO")
        add_text(layout, description, (326, y), 1.35, layer="02_TEXTO")


def draw_layout(layout) -> None:
    add_rect(layout, 53, 105, 367, 261, "11_ARQUITETURA")
    centered(layout, "PLACA DE MONTAGEM - 800 x 600 mm", (210, 255), 2.2, "11_ARQUITETURA")
    for x0, x1 in ((62, 79), (341, 358)):
        add_rect(layout, x0, 116, x1, 244, "10_ELETROCALHAS")
        centered(layout, "CANALETA", ((x0 + x1) / 2, 180), 1.25, "10_ELETROCALHAS")
    for y0, y1 in ((225, 237), (181, 193), (137, 149)):
        add_rect(layout, 79, y0, 341, y1, "10_ELETROCALHAS")
    for y in (220, 176, 132):
        line(layout, (85, y), (335, y), "03_COTAS")

    top = ((88, 199, 119, 219, "Q0", "40 A", "05_POTENCIA"),
           (126, 199, 157, 219, "QF1", "9-14 A", "05_POTENCIA"),
           (164, 199, 195, 219, "QF2", "9-14 A", "05_POTENCIA"),
           (202, 199, 233, 219, "QF3", "4 A", "05_POTENCIA"),
           (240, 199, 286, 219, "PSU1", "24 V / 10 A", "04_EQUIPAMENTOS"),
           (293, 199, 333, 219, "KSR1", "2 canais", "06_COMANDO"))
    for values in top:
        box(layout, *values)
    box(layout, 89, 155, 147, 176, "CLP1-CPU", "24 Vcc", "07_INSTRUMENTACAO")
    box(layout, 154, 155, 209, 176, "DI 16x", "PNP", "07_INSTRUMENTACAO")
    box(layout, 216, 155, 271, 176, "DO 16x", "PNP", "07_INSTRUMENTACAO")
    box(layout, 278, 155, 332, 176, "K1/K2/KA1", "Interfaces", "06_COMANDO")
    box(layout, 89, 111, 137, 132, "KM1/RT1", "Bomba 1", "05_POTENCIA")
    box(layout, 144, 111, 192, 132, "KM2/RT2", "Bomba 2", "05_POTENCIA")
    box(layout, 199, 111, 235, 132, "KDRY", "Nível", "06_COMANDO")
    add_rect(layout, 242, 111, 332, 132, "09_BORNES")
    centered(layout, "X1 | X2 | X3 | X4", (287, 121.5), 1.65, "09_BORNES")
    centered(layout, "TB-PE", (321, 102), 1.55, "05_POTENCIA")
    line(layout, (287, 105), (350, 105), "05_POTENCIA")

    line(layout, (45, 105), (45, 261), "03_COTAS")
    line(layout, (41, 105), (49, 105), "03_COTAS")
    line(layout, (41, 261), (49, 261), "03_COTAS")
    centered(layout, "600 mm", (39, 183), 1.7, "03_COTAS")
    line(layout, (53, 265), (367, 265), "03_COTAS")
    centered(layout, "800 mm", (210, 263), 1.7, "03_COTAS")


def terminal_table(layout, x0: float, x1: float, y_top: float, title: str,
                   rows: tuple[tuple[str, str, str], ...], row_h: float) -> None:
    header = 12.0
    y_bottom = y_top - header - row_h * len(rows)
    add_rect(layout, x0, y_bottom, x1, y_top, "09_BORNES")
    line(layout, (x0, y_top - header), (x1, y_top - header), "09_BORNES")
    c1, c2 = x0 + 21, x1 - 35
    line(layout, (c1, y_bottom), (c1, y_top - header), "09_BORNES")
    line(layout, (c2, y_bottom), (c2, y_top - header), "09_BORNES")
    centered(layout, title, ((x0 + x1) / 2, y_top - 6), 1.9, "09_BORNES")
    for i, (terminal, function, cable) in enumerate(rows):
        y1 = y_top - header - i * row_h
        y0 = y1 - row_h
        if i:
            line(layout, (x0, y1), (x1, y1), "09_BORNES")
        cy = (y0 + y1) / 2
        centered(layout, terminal, ((x0 + c1) / 2, cy), 1.35, "09_BORNES")
        centered(layout, function, ((c1 + c2) / 2, cy), 1.25, "02_TEXTO")
        centered(layout, cable, ((c2 + x1) / 2, cy), 1.25, "08_CABOS")


def draw_terminals(layout) -> None:
    terminal_table(layout, 18, 104, 257, "X1 - ENTRADA",
                   (("1", "L1", "W01"), ("2", "L2", "W01"), ("3", "L3", "W01"), ("4", "PE", "W01")), 10)
    terminal_table(layout, 110, 218, 257, "X2 - MOTORES",
                   (("1", "M1-U", "W02"), ("2", "M1-V", "W02"), ("3", "M1-W", "W02"), ("4", "M1-PE", "W02"),
                    ("5", "M2-U", "W03"), ("6", "M2-V", "W03"), ("7", "M2-W", "W03"), ("8", "M2-PE", "W03")), 10)
    terminal_table(layout, 224, 404, 257, "X3 - ENTRADAS",
                   tuple((str(i + 1), row[1], row[3]) for i, row in enumerate(INPUTS)), 8)
    terminal_table(layout, 18, 115, 159, "X4:1-6 - SAÍDAS",
                   tuple((str(i + 1), row[1], row[3]) for i, row in enumerate(OUTPUTS[:6])), 7)
    terminal_table(layout, 121, 218, 159, "X4:7-12 - SAÍDAS",
                   tuple((str(i + 7), row[1], row[3]) for i, row in enumerate(OUTPUTS[6:12])), 7)
    centered(layout, "X4:13-16 reservados; X3:17 = 0 V; X3:18 = PE/blindagem", (113, 102), 1.25, "13_NOTAS")


def draw_field(layout) -> None:
    box(layout, 153, 147, 268, 224, "PAINEL P03", "Q0 / PSU1 / CLP1 / X1-X4")
    box(layout, 20, 185, 91, 224, "QDG", "220 V 3~ + PE", "05_POTENCIA")
    box(layout, 20, 235, 100, 258, "S0", "Emergência 2 canais", "06_COMANDO")
    box(layout, 20, 108, 100, 137, "SUPERVISÃO", "Alarme remoto", "07_INSTRUMENTACAO")
    box(layout, 321, 232, 401, 258, "RESERVATÓRIO", "LSL / LSH / LSHH", "11_ARQUITETURA")
    box(layout, 321, 190, 401, 220, "CAPTAÇÃO", "LSL-LL / KDRY", "07_INSTRUMENTACAO")
    box(layout, 323, 140, 400, 174, "M1", "Bomba 1 - 3 kW", "05_POTENCIA")
    box(layout, 323, 101, 400, 135, "M2", "Bomba 2 - 3 kW", "05_POTENCIA")

    paths = (
        ([(91, 204), (153, 204)], "W01 - 4G6", (122, 210), "05_POTENCIA"),
        ([(100, 246), (130, 246), (130, 214), (153, 214)], "W04", (128, 252), "06_COMANDO"),
        ([(100, 122), (130, 122), (130, 158), (153, 158)], "W11", (128, 116), "07_INSTRUMENTACAO"),
        ([(268, 211), (300, 211), (300, 245), (321, 245)], "W07", (296, 251), "07_INSTRUMENTACAO"),
        ([(268, 194), (308, 194), (308, 205), (321, 205)], "W06", (294, 188), "07_INSTRUMENTACAO"),
        ([(268, 172), (296, 172), (296, 157), (323, 157)], "W02 - 4G2,5", (296, 178), "05_POTENCIA"),
        ([(268, 155), (286, 155), (286, 118), (323, 118)], "W03 - 4G2,5", (286, 112), "05_POTENCIA"),
    )
    for points, cable, point, layer in paths:
        orthogonal(layout, points, layer)
        label(layout, cable, point, "08_CABOS")
    centered(layout, "X1", (147, 207), 1.5, "09_BORNES")
    centered(layout, "X3", (274, 211), 1.5, "09_BORNES")
    centered(layout, "X2", (274, 176), 1.5, "09_BORNES")
    centered(layout, "X4", (147, 162), 1.5, "09_BORNES")
    centered(layout, "PE contínuo para painel, porta e carcaças M1/M2", (210, 106), 1.45, "05_POTENCIA")


def draw_sequence_box(layout, x0: float, x1: float, tag: str, description: str) -> None:
    add_rect(layout, x0, 232, x1, 260, "06_COMANDO")
    centered(layout, tag, ((x0 + x1) / 2, 252.5), 1.55, "06_COMANDO")
    centered(layout, description, ((x0 + x1) / 2, 239), 1.18, "02_TEXTO")


def flow_arrow(layout, x0: float, x1: float, y: float) -> None:
    line(layout, (x0, y), (x1 - 2.0, y), "06_COMANDO")
    layout.add_lwpolyline(
        [(x1, y), (x1 - 2.0, y + 1.4), (x1 - 2.0, y - 1.4)],
        close=True,
        dxfattribs={"layer": "06_COMANDO"},
    )


def down_arrow(layout, x: float, y_top: float, y_bottom: float) -> None:
    line(layout, (x, y_top), (x, y_bottom + 2.0), "06_COMANDO")
    layout.add_lwpolyline(
        [(x, y_bottom), (x - 1.4, y_bottom + 2.0), (x + 1.4, y_bottom + 2.0)],
        close=True,
        dxfattribs={"layer": "06_COMANDO"},
    )


def draw_matrix(layout) -> None:
    x0, x1, y_top = 18.0, 402.0, 188.0
    header_h, row_h = 10.0, 10.0
    widths = (48.0, 78.0, 156.0, 102.0)
    y_bottom = y_top - header_h - row_h * len(CAUSE_EFFECTS)
    add_rect(layout, x0, y_bottom, x1, y_top, "12_LEGENDA")
    columns = [x0]
    for width in widths:
        columns.append(columns[-1] + width)
    for x in columns[1:-1]:
        line(layout, (x, y_bottom), (x, y_top), "12_LEGENDA")
    line(layout, (x0, y_top - header_h), (x1, y_top - header_h), "12_LEGENDA")
    headers = ("EVENTO", "DETECÇÃO", "RESPOSTA CONCEITUAL", "RETORNO / PENDÊNCIA")
    for index, header in enumerate(headers):
        centered(layout, header, ((columns[index] + columns[index + 1]) / 2, y_top - header_h / 2), 1.35, "12_LEGENDA")
    for row_index, row in enumerate(CAUSE_EFFECTS):
        y1 = y_top - header_h - row_index * row_h
        y0 = y1 - row_h
        if row_index:
            line(layout, (x0, y1), (x1, y1), "12_LEGENDA")
        for col_index, value in enumerate(row):
            centered(
                layout,
                value,
                ((columns[col_index] + columns[col_index + 1]) / 2, (y0 + y1) / 2),
                1.22,
                "02_TEXTO",
            )


def draw_sequence(layout) -> None:
    boxes = ((18, 74, "01 ENERGIZAR", "Q0 + PSU1 / 24 V"),
             (80, 136, "02 DIAGNÓSTICO", "KSR1, KDRY, RTs, LS"),
             (142, 194, "03 PRONTO", "H1; sem falha travada"),
             (200, 264, "04 AUTO", "LSH memoriza demanda"),
             (270, 330, "05 TITULAR", "Comanda K1 ou K2"),
             (336, 402, "06 RETORNO?", "KMx_FB em até 2 s"))
    for x0, x1, tag, description in boxes:
        draw_sequence_box(layout, x0, x1, tag, description)
    for left_box, right_box in zip(boxes, boxes[1:]):
        flow_arrow(layout, left_box[1], right_box[0], 246)

    add_rect(layout, 18, 198, 205, 222, "06_COMANDO")
    centered(layout, "SEM RETORNO EM 2 s", (111.5, 216), 1.55, "06_COMANDO")
    centered(layout, "Bloqueia bomba; tenta reserva sob demanda", (111.5, 204.5), 1.18, "02_TEXTO")
    add_rect(layout, 212, 198, 402, 222, "07_INSTRUMENTACAO")
    centered(layout, "CICLO AUTOMÁTICO", (307, 216), 1.55, "07_INSTRUMENTACAO")
    centered(layout, "LSL encerra; sem falha, alterna. LSHH ≥ 10 s solicita reserva", (307, 204.5), 1.18, "02_TEXTO")
    line(layout, (369, 232), (369, 227), "06_COMANDO")
    line(layout, (111.5, 227), (369, 227), "06_COMANDO")
    down_arrow(layout, 111.5, 227, 222)
    down_arrow(layout, 307, 227, 222)
    centered(layout, "NÃO", (103, 224.5), 1.0, "06_COMANDO")
    centered(layout, "SIM", (316, 224.5), 1.0, "06_COMANDO")
    draw_matrix(layout)


DRAWERS = {
    1: draw_architecture,
    2: draw_24v,
    3: draw_inputs,
    4: draw_outputs,
    5: draw_command,
    6: draw_layout,
    7: draw_terminals,
    8: draw_field,
    9: draw_sequence,
}


def write_matrix_csv(project_dir: Path) -> Path:
    path = project_dir / "matriz-causa-efeito.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("evento", "deteccao", "resposta_conceitual", "retorno_ou_pendencia"))
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
