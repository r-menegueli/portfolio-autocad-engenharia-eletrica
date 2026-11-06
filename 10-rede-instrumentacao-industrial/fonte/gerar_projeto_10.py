"""Gera dados estruturados e oito pranchas DXF do Projeto 10."""

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


PROJECT_SLUG = "10-rede-instrumentacao-industrial"
PROJECT_DATE = "2026-11-05"
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
    SheetSpec(1, "01_arquitetura_rede.dxf", "ARQUITETURA DA REDE", "Supervisão, controle, remotas, instrumentos e distribuição 24 Vcc", "Topologia acadêmica genérica; protocolo, fabricante e disponibilidade não foram selecionados.\\PSeparar alimentação, sinais de campo e comunicação em rotas compatíveis com o estudo de EMC.", "Vermelho: 24 Vcc | Magenta: 4-20 mA | Verde: digital | Laranja: comunicação"),
    SheetSpec(2, "02_diagrama_instrumentacao.dxf", "DIAGRAMA DE INSTRUMENTAÇÃO", "Quatro malhas analógicas e duas entradas digitais de processo", "Transmissores de dois fios são alimentados pela malha 24 Vcc e entregam 4-20 mA.\\PChaves digitais representam somente estado; não transportam valor contínuo de engenharia.", "TT: temperatura | PT: pressão | FT: vazão | LT/LSH: nível | PSL: pressão"),
    SheetSpec(3, "03_diagrama_interligacao.dxf", "DIAGRAMA DE INTERLIGAÇÃO", "Cabos, bornes, canais, blindagem e equipotencialização", "Blindagem analógica aterrada apenas em BE-101, no painel; extremidade de campo isolada.\\PPE, 0 V funcional e blindagem têm funções distintas e não devem ser confundidos.", "X2: 24 Vcc | X3: analógicos | X4: digitais | BE-101: barra de blindagem | PE-101: proteção"),
    SheetSpec(4, "04_topologia_comunicacao.dxf", "TOPOLOGIA DE COMUNICAÇÃO", "Ethernet industrial acadêmica em estrela com switch gerenciável", "A comunicação transporta quadros e diagnósticos, não a energia nem o valor 4-20 mA.\\PEndereços são premissas de documentação; VLAN, protocolo e redundância exigem projeto posterior.", "Linha laranja: Ethernet industrial | NET-xxx: identificação do enlace | /24: máscara 255.255.255.0"),
    SheetSpec(5, "05_painel_instrumentacao.dxf", "PAINEL DE INSTRUMENTAÇÃO", "Arranjo conceitual 800 x 600 x 250 mm — PI-101", "Layout não define produto, dissipação, grau IP, folgas ou certificação.\\PConfirmar térmica, EMC, segregação, curvatura, torque e acesso antes de execução.", "PS: fonte | QF: proteção | PLC: controlador | SW: switch | X: bornes | BE/PE: barras"),
    SheetSpec(6, "06_lista_instrumentos.dxf", "LISTA DE INSTRUMENTOS", "Tags, variáveis, faixas, sinais, canais e documentos associados", "Faixas e tags são dados fictícios, revisados graficamente em 01. Aplicar unidades exatamente como indicadas.\\PA relação matemática é EU = LRV + (I-4)/16 x (URV-LRV).", "AI: entrada analógica | DI: entrada digital | RIO: I/O remota | EU: unidade de engenharia"),
    SheetSpec(7, "07_matriz_causa_efeito_sinais.dxf", "MATRIZ CAUSA-EFEITO DE SINAIS", "Falhas analógicas, I/O remota, rede, supervisão e 24 Vcc", "Resposta de processo e diagnósticos de fabricante não estão definidos.\\PNão converter canal inválido em variável válida nem presumir comportamento de retorno.", "AI: entrada analógica | DI: entrada digital | RIO: I/O remota | SCADA: supervisão"),
    SheetSpec(8, "08_matriz_escala_analogica.dxf", "MATRIZ DE ESCALA ANALÓGICA", "Quatro malhas 4–20 mA; cinco pontos calculados por faixa", "Valores calculados pela relação linear declarada; não são calibração nem teste de bancada.\\PTolerância, resolução, burden, limites de diagnóstico e critérios de aceitação dependem do hardware e do processo selecionados.", "LRV/URV: limites da faixa | EU: unidade de engenharia | pontos intermediários: 25 %, 50 % e 75 % da faixa"),
)


CAUSE_EFFECT_COLUMNS = ("id", "evento", "deteccao_condicao", "resposta_conceitual", "alarme_indicacao", "retorno_limite")

CAUSE_EFFECT_ROWS = (
    ("E01", "Qualidade AI invalida", "AI-001 a AI-004: diagnostico ou valor fora do range; limites do modulo pendentes", "Marcar o canal como invalido; nao tratar valor retido como medida atual", "Tag, codigo e retencao dependem do modulo/PLC", "Verificar transmissor, escala e criterio do fabricante"),
    ("E02", "Perda do loop 4-20 mA", "Corrente ausente ou anomala em C-101 a C-104; deteccao depende do hardware", "Nao inferir zero de processo; marcar qualidade conforme diagnostico disponivel", "Canal afetado e modo de diagnostico pendentes", "Inspecionar cabos, borne, alimentacao de malha e transmissor"),
    ("E03", "Perda de RIO-201", "NET-102 ou RIO-201 sem comunicacao; AI-001/002 e DI-001 afetados", "Invalidar dados da remota; acao de processo depende da criticidade", "Timeout, tag e historico dependem do protocolo/PLC", "Restabelecer link e validar qualidade antes de liberar uso"),
    ("E04", "Perda de RIO-202", "NET-103 ou RIO-202 sem comunicacao; AI-003/004 e DI-002 afetados", "Invalidar dados da remota; acao de processo depende da criticidade", "Timeout, tag e historico dependem do protocolo/PLC", "Restabelecer link e validar qualidade antes de liberar uso"),
    ("E05", "Perda do link SCADA", "NET-104 sem dados atualizados entre PLC-101 e SCADA-101", "Supervisao fica desatualizada; tarefa local do PLC nao deve depender da tela", "Alarme, buffering e recuperacao dependem da plataforma", "Confirmar conexao e reconciliar historico apos retorno"),
    ("E06", "Dado recebido obsoleto", "Valor sem atualizacao dentro do timeout a definir; tempo nao especificado", "Assinalar dado como obsoleto; nao usar amostra antiga como atual", "Timestamp, heartbeat e timeout dependem do protocolo", "Validar sequencia e qualidade apos recuperar comunicacao"),
    ("E07", "Perda da alimentacao 24 Vcc", "PS1, barramento ou protecao fora da condicao; pontos de monitoramento pendentes", "Instrumentos/remotas afetados deixam de fornecer dados validos", "Deteccao remota e tag de falha dependem da arquitetura", "Inspecionar causa, tensao e protecoes antes de liberar os nos"),
    ("E08", "Falha de DI de campo", "C-105/C-106 ou entrada DI sem diagnostico de linha definido", "Estado 0/1 pode nao distinguir falha de campo; tratamento depende do sensor", "PNP/NPN, contato e indicacao de circuito aberto pendentes", "Testar entrada e instrumento; nao presumir estado seguro"),
)


INSTRUMENTS = (
    ("TT-101", "Temperatura", "0", "150", "°C", "4-20 mA, 2 fios", "RIO-201/AI0", "C-101"),
    ("PT-102", "Pressão", "0", "10", "bar(g)", "4-20 mA, 2 fios", "RIO-201/AI1", "C-102"),
    ("FT-103", "Vazão", "0", "60", "m³/h", "4-20 mA, 2 fios", "RIO-202/AI0", "C-103"),
    ("LT-104", "Nível", "0", "5", "m", "4-20 mA, 2 fios", "RIO-202/AI1", "C-104"),
    ("LSH-105", "Nível alto", "0", "1", "estado", "digital 24 Vcc", "RIO-201/DI0", "C-105"),
    ("PSL-106", "Pressão baixa", "0", "1", "estado", "digital 24 Vcc", "RIO-202/DI0", "C-106"),
)

IO_ROWS = (
    ("AI-001", "TT-101", "RIO-201", "AI0", "4-20 mA", "0-150 °C", "temperatura contínua"),
    ("AI-002", "PT-102", "RIO-201", "AI1", "4-20 mA", "0-10 bar(g)", "pressão contínua"),
    ("AI-003", "FT-103", "RIO-202", "AI0", "4-20 mA", "0-60 m³/h", "vazão contínua"),
    ("AI-004", "LT-104", "RIO-202", "AI1", "4-20 mA", "0-5 m", "nível contínuo"),
    ("DI-001", "LSH-105", "RIO-201", "DI0", "24 Vcc", "0/1", "nível alto"),
    ("DI-002", "PSL-106", "RIO-202", "DI0", "24 Vcc", "0/1", "pressão baixa"),
)

CABLE_ROWS = (
    ("C-101", "TT-101", "RIO-201/AI0", "Sinal analógico 4-20 mA e alimentação de malha", "1x2x0,75 mm² SH", "+/−/SH", "SIM", "45", "E-101", "X3:01/02", "Blindagem em BE-101 no painel"),
    ("C-102", "PT-102", "RIO-201/AI1", "Sinal analógico 4-20 mA e alimentação de malha", "1x2x0,75 mm² SH", "+/−/SH", "SIM", "38", "E-101", "X3:03/04", "Blindagem em BE-101 no painel"),
    ("C-103", "FT-103", "RIO-202/AI0", "Sinal analógico 4-20 mA e alimentação de malha", "1x2x0,75 mm² SH", "+/−/SH", "SIM", "52", "E-102", "X3:05/06", "Blindagem em BE-101 no painel"),
    ("C-104", "LT-104", "RIO-202/AI1", "Sinal analógico 4-20 mA e alimentação de malha", "1x2x0,75 mm² SH", "+/−/SH", "SIM", "48", "E-102", "X3:07/08", "Blindagem em BE-101 no painel"),
    ("C-105", "LSH-105", "RIO-201/DI0", "Entrada digital 24 Vcc", "1x2x0,75 mm²", "DI/0V", "NÃO", "42", "E-101", "X4:01/02", "Tipo elétrico final pendente"),
    ("C-106", "PSL-106", "RIO-202/DI0", "Entrada digital 24 Vcc", "1x2x0,75 mm²", "DI/0V", "NÃO", "35", "E-102", "X4:03/04", "Tipo elétrico final pendente"),
    ("P24-201", "PI-101", "RIO-201", "Alimentação 24 Vcc", "2x1,5 mm² + PE", "+24V/0V/PE", "NÃO", "50", "E-201", "X2", "Proteção FU2 no painel"),
    ("P24-202", "PI-101", "RIO-202", "Alimentação 24 Vcc", "2x1,5 mm² + PE", "+24V/0V/PE", "NÃO", "55", "E-202", "X2", "Proteção FU3 no painel"),
    ("NET-101", "SW-101/P1", "PLC-101", "Comunicação Ethernet industrial", "Ethernet industrial SH", "TX/RX/SH", "SIM", "3", "N-101", "P1", "Terminação conforme fabricante e EMC"),
    ("NET-102", "SW-101/P2", "RIO-201", "Comunicação Ethernet industrial", "Ethernet industrial SH", "TX/RX/SH", "SIM", "50", "N-102", "P2", "Terminação conforme fabricante e EMC"),
    ("NET-103", "SW-101/P3", "RIO-202", "Comunicação Ethernet industrial", "Ethernet industrial SH", "TX/RX/SH", "SIM", "55", "N-103", "P3", "Terminação conforme fabricante e EMC"),
    ("NET-104", "SW-101/P4", "SCADA-101", "Comunicação Ethernet industrial", "Ethernet industrial SH", "TX/RX/SH", "SIM", "20", "N-104", "P4", "Terminação conforme fabricante e EMC"),
)

TERMINAL_ROWS = (
    ("X1:01", "L", "entrada 230 Vca", "QF0:1"), ("X1:02", "N", "entrada 230 Vca", "QF0:2"), ("X1:PE", "PE", "proteção", "PE-101"),
    ("X2:01", "+24V", "distribuição", "FU1"), ("X2:02", "0V", "retorno funcional", "PS1:-"),
    ("X3:01/02", "TT-101 +/−", "analógico", "RIO-201/AI0"), ("X3:03/04", "PT-102 +/−", "analógico", "RIO-201/AI1"),
    ("X3:05/06", "FT-103 +/−", "analógico", "RIO-202/AI0"), ("X3:07/08", "LT-104 +/−", "analógico", "RIO-202/AI1"),
    ("X4:01/02", "LSH-105", "digital", "RIO-201/DI0"), ("X4:03/04", "PSL-106", "digital", "RIO-202/DI0"),
    ("BE-101", "SHIELD", "blindagem funcional", "PE-101 em ponto definido"), ("PE-101", "PE", "proteção/equipotencial", "chassi"),
)

NETWORK_ROWS = (
    ("PLC-101", "192.168.10.10", "255.255.255.0", "SW-101/P1", "controlador"),
    ("RIO-201", "192.168.10.21", "255.255.255.0", "SW-101/P2", "remota área A"),
    ("RIO-202", "192.168.10.22", "255.255.255.0", "SW-101/P3", "remota área B"),
    ("SCADA-101", "192.168.10.30", "255.255.255.0", "SW-101/P4", "supervisão"),
    ("ENG-101", "192.168.10.40", "255.255.255.0", "SW-101/P5", "engenharia temporária"),
    ("SW-101", "192.168.10.2", "255.255.255.0", "gerenciado", "infraestrutura"),
)

POWER_ROWS = (
    ("PLC-101", "24", "0.60", "14.40"), ("SW-101", "24", "0.35", "8.40"),
    ("RIO-201", "24", "0.45", "10.80"), ("RIO-202", "24", "0.45", "10.80"),
    ("malhas AI (4)", "24", "0.10", "2.40"), ("sensores DI (2)", "24", "0.10", "2.40"),
    ("reserva auxiliares", "24", "1.05", "25.20"),
)

MATERIAL_ROWS = (
    ("1", "PI-101", "Painel metálico 800 x 600 x 250 mm", "un", "1", "dimensão conceitual"),
    ("2", "PS1", "Fonte 230 Vca / 24 Vcc / 10 A", "un", "1", "seleção final pendente"),
    ("3", "PLC-101", "CLP com CPU e interface Ethernet", "un", "1", "genérico"),
    ("4", "RIO-201/202", "Remota com AI e DI 24 Vcc", "un", "2", "genérica"),
    ("5", "SW-101", "Switch Ethernet industrial gerenciável, 8 portas", "un", "1", "genérico"),
    ("6", "SCADA-101", "Estação de supervisão", "un", "1", "computador/software não selecionados"),
    ("7", "TT/PT/FT/LT", "Transmissor 2 fios 4-20 mA", "un", "4", "faixas conforme lista"),
    ("8", "LSH/PSL", "Chave de processo 24 Vcc", "un", "2", "contato/sensor final pendente"),
    ("9", "X1-X4", "Bornes seccionáveis e de passagem", "conj", "1", "dimensionamento conceitual"),
    ("10", "BE-101/PE-101", "Barras de blindagem e proteção", "conj", "1", "funções distintas"),
)

PARAMETER_ROWS = (
    ("tensao_controle", "24", "Vcc", "barramento funcional da instrumentação"),
    ("corrente_fonte", "10", "A", "capacidade nominal proposta de PS1"),
    ("tensao_entrada", "230", "Vca", "alimentação monofásica conceitual de PI-101"),
    ("corrente_carga", "3.10", "A", "carga prevista incluindo reserva auxiliar"),
    ("potencia_carga", "74.40", "W", "soma das cargas 24 Vcc"),
    ("topologia_rede", "estrela", "texto", "switch SW-101 como ponto central"),
    ("subrede", "192.168.10.0/24", "IPv4", "endereçamento documental fictício"),
    ("painel_largura", "800", "mm", "dimensão conceitual"),
    ("painel_altura", "600", "mm", "dimensão conceitual"),
    ("painel_profundidade", "250", "mm", "dimensão conceitual"),
)


def line(layout, start, end, layer):
    add_line(layout, start, end, layer)


def centered(layout, value, point, height=1.35, layer="02_TEXTO"):
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def left(layout, value, point, height=1.2, layer="02_TEXTO"):
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_LEFT)


def component(layout, x0, y0, x1, y1, tag, detail, layer="04_EQUIPAMENTOS"):
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5), 1.55, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4), 0.95, "02_TEXTO")


def arrow(layout, start, end, layer, label="", offset=(0.0, 4.0)):
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base = (end[0] - 3.5 * ux, end[1] - 3.5 * uy)
    layout.add_lwpolyline([end, (base[0] + 1.4 * px, base[1] + 1.4 * py), (base[0] - 1.4 * px, base[1] - 1.4 * py)], close=True, dxfattribs={"layer": layer})
    if label:
        centered(layout, label, ((start[0] + end[0]) / 2 + offset[0], (start[1] + end[1]) / 2 + offset[1]), 0.9, layer)


def orthogonal(layout, points, layer):
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def table(layout, x, top, widths, headers, rows, row_height, text_height=0.85, layer="12_LEGENDA"):
    total_width = sum(widths)
    total_height = row_height * (len(rows) + 1)
    add_rect(layout, x, top - total_height, x + total_width, top, layer)
    cursor = x
    centers = []
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


def transmitter(layout, center, tag, variable, digital=False):
    layer = "06_COMANDO" if digital else "07_INSTRUMENTACAO"
    layout.add_circle(center, 7.5, dxfattribs={"layer": layer})
    centered(layout, tag, (center[0], center[1] + 1.6), 1.15, layer)
    centered(layout, variable, (center[0], center[1] - 2.3), 0.9, "02_TEXTO")


def add_revision_table(layout):
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRIÇÃO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.6, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("REVISAO DE SINAIS", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.35, "02_TEXTO")


def add_bottom_information(layout, spec, warning):
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATÓRIO", (22, 42), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.5, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.0, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.35, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.0, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.35, "12_LEGENDA")


def add_title_block(layout, spec, config):
    values = {"TITULO": spec.title, "AUTOR": config["portfolio"]["author"], "DATA": PROJECT_DATE, "REVISAO": REVISION, "PRANCHA": f"{spec.number:02d}/{len(SHEETS):02d}", "ARQUIVO": spec.filename, "UNIDADES": "mm", "ESCALA": "S/ESC.", "FOLHA": "A3", "STATUS": "CONCEIT."}
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(values)


def create_sheet(config, spec):
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    meta = doc.ezdxf_metadata()
    meta["PORTFOLIO_PROJECT"] = PROJECT_SLUG
    meta["PORTFOLIO_SHEET"] = f"{spec.number:02d}/{len(SHEETS):02d}"
    meta["PORTFOLIO_EPISTEMIC_STATUS"] = "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION"
    define_title_block(doc)
    define_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 3.7, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.7, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_architecture(layout):
    component(layout, 165, 235, 255, 258, "SCADA-101", "supervisão / históricos")
    component(layout, 180, 191, 240, 219, "SW-101", "switch gerenciável")
    component(layout, 46, 188, 116, 222, "PLC-101", "CPU / controle")
    component(layout, 48, 128, 118, 164, "RIO-201", "área A | 2 AI + 1 DI")
    component(layout, 292, 128, 362, 164, "RIO-202", "área B | 2 AI + 1 DI")
    for start, end, tag in (((210,235),(210,219),"NET-104"),((180,205),(116,205),"NET-101"),((195,191),(83,164),"NET-102"),((225,191),(327,164),"NET-103")):
        arrow(layout, start, end, "08_CABOS", tag, (0,3))
    for x, tag, var in ((30,"TT-101","T"),(75,"PT-102","P"),(335,"FT-103","F"),(380,"LT-104","L")):
        transmitter(layout, (x,108), tag, var)
    transmitter(layout, (145,108), "LSH-105", "DI", True)
    transmitter(layout, (265,108), "PSL-106", "DI", True)
    for x, target, cable in ((30,60,"C-101"),(75,88,"C-102"),(145,105,"C-105")):
        arrow(layout, (x,116), (target,128), "07_INSTRUMENTACAO" if x != 145 else "06_COMANDO", cable, (0,2))
    for x, target, cable in ((335,318,"C-103"),(380,350,"C-104"),(265,305,"C-106")):
        arrow(layout, (x,116), (target,128), "07_INSTRUMENTACAO" if x != 265 else "06_COMANDO", cable, (0,2))
    add_rect(layout, 270, 195, 397, 254, "05_POTENCIA")
    centered(layout, "PS1 — 24 Vcc / 10 A", (333.5,245), 1.5, "05_POTENCIA")
    for y, text_value in ((232,"FU1 PLC/SW"),(220,"FU2 RIO-201"),(208,"FU3 RIO-202")):
        left(layout, text_value, (280,y), 1.0, "05_POTENCIA")
        arrow(layout, (350,y), (385,y), "05_POTENCIA", "+24V/0V", (0,2))
    centered(layout, "ALIMENTAÇÃO ≠ SINAL ANALÓGICO ≠ SINAL DIGITAL ≠ COMUNICAÇÃO", (210,101), 1.25, "13_NOTAS")


def draw_instrumentation(layout):
    centered(layout, "MALHAS ANALÓGICAS DE DOIS FIOS — 4 A 20 mA", (205,257), 1.45, "07_INSTRUMENTACAO")
    rows = (("TT-101","0...150 °C","C-101","RIO-201 / AI0"),("PT-102","0...10 bar(g)","C-102","RIO-201 / AI1"),("FT-103","0...60 m³/h","C-103","RIO-202 / AI0"),("LT-104","0...5 m","C-104","RIO-202 / AI1"))
    for index, (tag, span, cable, channel) in enumerate(rows):
        y = 232 - 31 * index
        centered(layout, "+24 V", (28,y), 0.95, "05_POTENCIA")
        transmitter(layout, (78,y), tag, span)
        component(layout, 270, y-10, 365, y+10, channel, "entrada analógica isolada")
        arrow(layout, (35,y), (70,y), "05_POTENCIA", "alimentação")
        arrow(layout, (86,y), (270,y), "07_INSTRUMENTACAO", f"{cable} | 4-20 mA", (0,3))
        orthogonal(layout, ((365,y),(390,y),(390,y-13),(35,y-13),(35,y)), "08_CABOS")
        left(layout, "0 V", (393,y-13), 0.9, "08_CABOS")
    centered(layout, "ENTRADAS DIGITAIS — ESTADO 24 Vcc", (205,111), 1.35, "06_COMANDO")
    for x, tag, cable, channel in ((65,"LSH-105","C-105","RIO-201 / DI0"),(260,"PSL-106","C-106","RIO-202 / DI0")):
        transmitter(layout, (x,105), tag, "0/1", True)
        component(layout, x+28, 97, x+120, 113, channel, "entrada digital")
        arrow(layout, (x+8,105), (x+28,105), "06_COMANDO", cable, (0,3))


def draw_interconnection(layout):
    centered(layout, "PAINEL PI-101", (205,257), 1.5, "04_EQUIPAMENTOS")
    table(layout, 20, 248, (28,31,38,35,35,35,35,35,35,35), ("CABO","CAMPO","COND.","BORNE","+24V","CANAL","0V","SHIELD","REMOTA","FUNÇÃO"), [
        ("C-101","TT-101","1x2 SH","X3:01/02","X2:01","AI0","X2:02","BE-101","RIO-201","4-20 mA"),
        ("C-102","PT-102","1x2 SH","X3:03/04","X2:01","AI1","X2:02","BE-101","RIO-201","4-20 mA"),
        ("C-103","FT-103","1x2 SH","X3:05/06","X2:01","AI0","X2:02","BE-101","RIO-202","4-20 mA"),
        ("C-104","LT-104","1x2 SH","X3:07/08","X2:01","AI1","X2:02","BE-101","RIO-202","4-20 mA"),
        ("C-105","LSH-105","1x2","X4:01/02","X2:01","DI0","X2:02","—","RIO-201","digital"),
        ("C-106","PSL-106","1x2","X4:03/04","X2:01","DI0","X2:02","—","RIO-202","digital"),
    ], 11.5, 0.78)
    add_rect(layout, 25, 132, 395, 164, "09_BORNES")
    for x, tag in ((55,"X2 +24V/0V"),(125,"X3 ANALÓGICOS"),(205,"X4 DIGITAIS"),(285,"BE-101 SHIELD"),(365,"PE-101")):
        centered(layout, tag, (x,153), 1.0, "09_BORNES")
        layout.add_circle((x,141), 4, dxfattribs={"layer":"09_BORNES"})
    arrow(layout, (285,137), (365,137), "06_COMANDO", "PONTO ÚNICO DEFINIDO", (0,-4))
    centered(layout, "CAMPO: blindagem isolada", (90,115), 1.1, "07_INSTRUMENTACAO")
    centered(layout, "PAINEL: blindagem em BE-101", (210,115), 1.1, "07_INSTRUMENTACAO")
    centered(layout, "PE-101: proteção e equipotencialização", (335,115), 1.1, "06_COMANDO")
    centered(layout, "0 V é retorno funcional; PE não conduz corrente operacional; SHIELD não substitui PE.", (210,102), 1.05, "13_NOTAS")


def draw_communication(layout):
    component(layout, 170, 185, 250, 225, "SW-101", "192.168.10.2 / 8 portas")
    nodes = ((55,235,"PLC-101",".10","NET-101"),(55,145,"RIO-201",".21","NET-102"),(355,145,"RIO-202",".22","NET-103"),(355,235,"SCADA-101",".30","NET-104"),(210,150,"ENG-101",".40","NET-105"))
    for x,y,tag,ip,cable in nodes:
        component(layout, x-32, y-14, x+32, y+14, tag, f"192.168.10{ip}")
        start = (170,205) if x < 210 else (250,205)
        if tag == "ENG-101": start = (210,185)
        arrow(layout, start, (x,y), "08_CABOS", cable, (0,3))
    table(layout, 22, 128, (58,68,68,58,58), ("NÓ","ENDEREÇO","MÁSCARA","PORTA","PAPEL"), [(r[0],r[1],"/24",r[3],r[4]) for r in NETWORK_ROWS[:5]], 4.5, 0.70)
    add_rect(layout, 140, 232, 280, 260, "13_NOTAS")
    centered(layout, "LIMITES", (210,255), 1.05, "13_NOTAS")
    add_mtext(layout, "Nós alimentados em 24 Vcc. Sem tráfego em tempo real, VLAN, firewall, gateway, sincronismo ou redundância definidos.", (146,250), 128, 0.9, "13_NOTAS")


def draw_panel(layout):
    x0,y0,w,h = 45,105,320,150
    add_rect(layout, x0,y0,x0+w,y0+h,"11_ARQUITETURA")
    centered(layout, "PI-101 — 800 x 600 x 250 mm", (205,248), 1.5, "11_ARQUITETURA")
    # Eletrocalhas laterais e horizontais.
    for rx0,ry0,rx1,ry1 in ((52,112,68,238),(342,112,358,238),(75,225,335,238),(75,112,335,125)):
        add_rect(layout,rx0,ry0,rx1,ry1,"10_ELETROCALHAS")
    # Trilhos e componentes.
    for y in (205,164): line(layout,(78,y),(332,y),"11_ARQUITETURA")
    component(layout,82,211,132,224,"QF0/FU1-6","proteção e distribuição")
    component(layout,145,207,205,224,"PS1","24 Vcc / 10 A")
    component(layout,220,207,280,224,"SW-101","Ethernet 8 portas")
    component(layout,294,207,330,224,"Q24","distribuição")
    component(layout,82,166,158,202,"PLC-101","CPU / 24 Vcc")
    component(layout,174,166,244,202,"I/O LOCAL","reserva acadêmica")
    component(layout,260,166,330,202,"RELÉS","interfaces futuras")
    add_rect(layout,82,130,330,157,"09_BORNES")
    for index,tag in enumerate(("X1","X2","X3","X4","BE-101","PE-101")):
        x=102+41*index
        centered(layout,tag,(x,149),0.9,"09_BORNES")
        layout.add_circle((x,138),3.2,dxfattribs={"layer":"09_BORNES"})
    centered(layout, "SEGREGAR 230 Vca | 24 Vcc | ANALÓGICO | DIGITAL | REDE", (205,118), 1.0, "13_NOTAS")
    add_rect(layout, 75, 96, 335, 105, "13_NOTAS")
    centered(layout, "CARGA PREVISTA: 3,10 A / 74,4 W | PS1: 10 A / 240 W | MARGEM: 69 %", (205,100.5), 0.95, "13_NOTAS")


def draw_instrument_list(layout):
    table(layout, 20, 255, (36,46,35,35,24,50,48,44), ("TAG","VARIÁVEL","LRV","URV","UN.","SINAL","CANAL","CABO"), [tuple(row) for row in INSTRUMENTS], 12.5, 0.82)
    centered(layout, "MAPA DE I/O E CONVERSÃO", (205,162), 1.3, "07_INSTRUMENTACAO")
    table(layout, 30, 155, (42,42,48,48,58,58,64), ("I/O","TAG","NÓ","CANAL","SINAL","ESCALA","SEMÂNTICA"), [tuple(row) for row in IO_ROWS], 7.2, 0.78)
    add_rect(layout, 30, 96, 380, 102, "13_NOTAS")
    centered(layout, "4 mA = LRV | 12 mA = 50 % da faixa | 20 mA = URV | DI = somente 0/1", (205,99), 1.0, "13_NOTAS")


def draw_analog_scale_matrix(layout):
    currents = (4.0, 8.0, 12.0, 16.0, 20.0)
    rows = []

    def fmt(value):
        return f"{value:g}".replace(".", ",")

    for tag, _, lrv_text, urv_text, unit, signal, _, _ in INSTRUMENTS:
        if "4-20" not in signal:
            continue
        lrv, urv = float(lrv_text), float(urv_text)
        values = [lrv + ((current - 4.0) / 16.0) * (urv - lrv) for current in currents]
        rows.append((tag, f"{fmt(lrv)}–{fmt(urv)} {unit}", *(f"{fmt(value)} {unit}" for value in values)))

    table(
        layout,
        27,
        251,
        (36, 56, 54, 54, 54, 54, 54),
        ("TAG", "FAIXA EU", "4 mA", "8 mA", "12 mA", "16 mA", "20 mA"),
        rows,
        16.5,
        1.8,
    )

    centered(layout, "CORRESPONDÊNCIA RELATIVA DA FAIXA", (210, 160), 1.15, "07_INSTRUMENTACAO")
    x_positions = (55, 135, 215, 295, 375)
    y = 137
    line(layout, (x_positions[0], y), (x_positions[-1], y), "07_INSTRUMENTACAO")
    for current, percent, x in zip(currents, (0, 25, 50, 75, 100), x_positions):
        line(layout, (x, y - 4), (x, y + 4), "03_COTAS")
        layout.add_circle((x, y), 1.6, dxfattribs={"layer": "07_INSTRUMENTACAO"})
        centered(layout, f"{current:g} mA", (x, 128), 1.4, "02_TEXTO")
        centered(layout, f"{percent} %", (x, 146), 1.4, "02_TEXTO")


def draw_cause_effect(layout):
    headers = ("ID", "EVENTO", "DETECCAO / CONDICAO", "RESPOSTA CONCEITUAL", "ALARME / INDICACAO", "RETORNO / LIMITE")
    widths = (14, 43, 70, 80, 64, 82)
    table(layout, 31, 261, widths, headers, CAUSE_EFFECT_ROWS, 13.2, 1.15)
    add_rect(layout, 18, 105, 402, 126, "13_NOTAS")
    centered(layout, "Tempos, limites, alarmes, fail state e acoes de processo dependem dos dispositivos e da analise de risco.", (210,115.5), 1.2, "13_NOTAS")


DRAWERS = (draw_architecture, draw_instrumentation, draw_interconnection, draw_communication, draw_panel, draw_instrument_list, draw_cause_effect, draw_analog_scale_matrix)


def write_csv(path, headers, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def write_data(project):
    write_csv(project / "parametros.csv", ("parametro","valor","unidade","descricao"), PARAMETER_ROWS)
    write_csv(project / "lista-instrumentos.csv", ("tag","variavel","lrv","urv","unidade","sinal","canal","cabo"), INSTRUMENTS)
    write_csv(project / "lista-io.csv", ("id","tag","no","canal","sinal","escala","semantica"), IO_ROWS)
    write_csv(project / "lista-cabos.csv", ("cabo","de","para","funcao","formacao","identificacao_condutores","blindagem","comprimento_assumido_m","rota","bornes","observacoes"), CABLE_ROWS)
    write_csv(project / "lista-bornes.csv", ("borne","potencial","funcao","destino"), TERMINAL_ROWS)
    write_csv(project / "lista-redes.csv", ("no","ip","mascara","porta","papel"), NETWORK_ROWS)
    write_csv(project / "lista-alimentacao.csv", ("carga","tensao_vcc","corrente_a","potencia_w"), POWER_ROWS)
    material_rows = [(item, quantity, unit, description, tag, note) for item, tag, description, unit, quantity, note in MATERIAL_ROWS]
    write_csv(project / "lista-materiais.csv", ("item","quantidade","unidade","descricao","referencia","observacoes"), material_rows)
    write_csv(project / "causa-efeito.csv", CAUSE_EFFECT_COLUMNS, CAUSE_EFFECT_ROWS)
    flat = []
    for tag, _, lrv, urv, unit, signal, _, _ in INSTRUMENTS:
        if "4-20" not in signal:
            continue
        lower, upper = float(lrv), float(urv)
        for current in (4.0, 8.0, 12.0, 16.0, 20.0):
            fraction = (current - 4.0) / 16.0
            value = lower + fraction * (upper - lower)
            flat.append((tag, f"{current:g}", f"{value:.3f}", unit))
    write_csv(project / "resultados-calculo.csv", ("tag","corrente_ma","valor_engenharia","unidade"), flat)


def generate(root):
    config = load_config(root)
    project = root / PROJECT_SLUG
    source_dir = project / "fonte"
    export_dir = project / "exports"
    source_dir.mkdir(parents=True, exist_ok=True)
    export_dir.mkdir(parents=True, exist_ok=True)
    write_data(project)
    for spec, drawer in zip(SHEETS, DRAWERS):
        doc, layout = create_sheet(config, spec)
        drawer(layout)
        prepare_deterministic_write(doc)
        doc.saveas(source_dir / spec.filename)
        print(f"gerado: {source_dir / spec.filename}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    generate(args.root.resolve())


if __name__ == "__main__":
    main()
