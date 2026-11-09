"""CAD e dados reproduciveis dos estudos conceituais P23-P25."""

from __future__ import annotations

import argparse
import csv
import json
import math
import numpy as np
from pathlib import Path
import re
import sys
from typing import Callable

import ezdxf
from ezdxf.enums import TextEntityAlignment

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

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
    define_symbols,
    define_title_block,
    prepare_deterministic_write,
)
from portfolio_config import SheetGeometry, load_config  # noqa: E402
from renderizar import render_document  # noqa: E402


DATE = "2026-11-09"
REVISION = "00"
DISCLAIMER = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços "
    "sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado."
)


SHEETS: dict[str, list[dict[str, str]]] = {
    "p23": [
        ("01_diagrama_unifilar_geral", "UNIFILAR GERAL DO COMPLEXO SIDERURGICO EAF", "Rede 138 kV, subestacao 138/34,5 kV, forno 30 MVA e auxiliares", "PCC no lado de 138 kV; barra industrial principal em 34,5 kV.\\PTransformador de forno de 30 MVA, secundario conceitual de 1,0 kV e derivacoes sob carga.\\PCompensacao dinamica e filtros conectados a barra de 34,5 kV.", "138 kV: entrada | T1: 45 MVA | TF1: 30 MVA | STATCOM: ±12,5 MVAr | F5/F7/HP: filtros"),
        ("02_planta_subestacao_receptora", "IMPLANTACAO DA SUBESTACAO RECEPTORA", "Arranjo conceitual AIS com bays de 138 kV, transformador e cubiculos de 34,5 kV", "Dimensoes e afastamentos sao esquematicos e devem ser substituidos por estudos de isolamento, acesso, incendio e solo.\\PEquipamentos representados em planta, sem coordenadas de levantamento.", "AIS: isolamento a ar | T1: 45 MVA | Q0: disjuntor 138 kV | B1: barra 34,5 kV"),
        ("03_layout_area_eletrica_forno", "LAYOUT ELETRICO DA AREA DO FORNO", "Arranjo do transformador de forno, reator, cabos flexiveis e equipamentos de agua", "Arranjo indicativo sem levantamento civil, estrutural, termico ou de seguranca de processo.\\PManter rotas de cabos de potencia afastadas de instrumentacao e agua de resfriamento.", "EAF: forno a arco | TF1: transformador | CCW: agua de resfriamento | E1-E3: eletrodos"),
        ("04_arranjo_transformadores_cubiculos", "TRANSFORMADORES, CUBICULOS E BARRAMENTOS", "Cortes conceituais do transformador principal e da alimentacao de forno", "T1: 45 MVA, 138/34,5 kV, uk=12,5% assumido.\\PTF1: 30 MVA, 34,5/1,0 kV, uk=10% assumido; valores sujeitos a especificacao do fabricante.", "T1: transformador receptor | TF1: transformador de forno | QF: disjuntor | TC/TP: medicao"),
        ("05_alimentacao_secundaria_forno", "ALIMENTACAO SECUNDARIA E CONEXOES DO FORNO", "Derivacoes do transformador, condutores refrigerados e circuito de eletrodos", "Corrente secundaria nominal de referencia: 17,32 kA em 1,0 kV, para 30 MVA trifasicos.\\PCondutores flexiveis e contatos sao apenas esquematicos; nao constituem especificacao de fabricacao.", "U/V/W: fases | E1-E3: eletrodos | CCW: cabos refrigerados a agua | TAPS: regulacao"),
        ("06_protecao_medicao", "PROTECAO E MEDICAO DO COMPLEXO", "Zonas de protecao, TCs/TPs, relés e pontos de medicao", "Codigos ANSI indicam funcoes de estudo, sem ajustes ou coordenacao validados.\\PCurto-circuito preliminar nao substitui estudo de protecao, arco eletrico ou seletividade.", "87T: diferencial trafo | 50/51: sobrecorrente | 87B: diferencial barra | 27/59: tensao | 86: bloqueio"),
        ("07_statcom_compensacao", "STATCOM E COMPENSACAO DINAMICA", "Conversor VSC, reator de acoplamento, transformador e controle de Q/V", "Balanço reativo calculado a partir da potência do forno, das cargas auxiliares, do fator de potência-alvo e dos filtros cadastrados.\\POs valores e a margem do STATCOM são mostrados na tabela; modelo conceitual, sem validação de fabricante.", "VSC: conversor fonte de tensao | PCC: ponto de acoplamento comum | Qref: comando reativo"),
        ("08_filtros_harmonicos", "BANCO DE FILTROS HARMONICOS", "Ramos sintonizados de 5a e 7a ordem e ramo amortecido de alta frequencia", "Espectro de corrente adotado (20%, 12%, 6%, 4%) e hipotese, nao medicao do processo.\\PValidar ressonancia, THD/TDD, perdas e dimensionamento termico com dados reais e impedancia de rede.", "F5: 3,0 MVAr | F7: 2,0 MVAr | HP: 2,5 MVAr | THD: distorcao harmonica total"),
        ("09_aterramento_equipotencializacao", "ATERRAMENTO E EQUIPOTENCIALIZACAO", "Malha conceitual da subestacao, estruturas, transformador e casa do forno", "Malha indicativa; resistividade, corrente de falta, tempo de eliminacao e tensoes de toque/passo nao medidos.\\PDimensionamento conforme estudo de solo e criterios vigentes da instalacao.", "Cu: condutor de cobre | BEP: barra equipotencial | H: haste | ligacao a carcaças e estruturas"),
        ("10_controle_intertravamentos", "CONTROLE, COMANDO E INTERTRAVAMENTOS", "Permissivos de energizacao, sequencia de fusao e desligamento seguro", "Intertravamentos funcionais de estudo; analise de risco e validacao de seguranca independentes.\\PPerda de fluxo de agua, falha de protecao ou emergencia bloqueia arco e abre QF.", "PLC: controlador | QF: disjuntor do forno | FL: fluxo de agua | EMG: emergencia | 86: lockout"),
    ],
    "p24": [
        ("01_planta_tracado", "PLANTA GERAL DO TRACADO DA LT", "Corredor ficticio de 30 km, estacas e coordenadas cartesianas locais", "Eixo, azimutes, cotas, travessias e estruturas sao dados sinteticos.\\PCoordenadas locais em metros, origem na SE A; nao representam levantamento, cadastro, servidao ou consulta ambiental.", "SE A/SE B: terminais | A: ancoragem | S: suspensao | OPGW: guarda optico | km: estaca ficticia"),
        ("02_perfil_longitudinal", "PERFIL LONGITUDINAL TOPOGRAFICO SINTETICO", "100 vaos, 101 estruturas e envelopes calculados para o condutor selecionado", "Cotas do terreno interpoladas de marcos sinteticos de 2 km.\\PEnvelope parabolico inclui flecha e alturas de fixacao assumidas; perfil nao serve para locacao ou liberacao de travessias.\\PEscala grafica vertical exagerada 100x; nao usar escala do papel para medir distancias.", "x: progressiva (km) | z: elevacao sintetica (m) | curva vermelha: 75 °C/0 m/s | verde: 20 °C/1 m/s | vao: 300 m"),
        ("03_vano_critico_envelope_flecha", "VAO NOMINAL E ENVELOPES DE FLECHA", "CAA Drake 795 kcmil em tres pares representativos de temperatura e vento", "Modelo parabolico com compatibilidade elastica de um vao e vento transversal equivalente; catenaria completa, creep, vibracao e estados finais nao substituidos.\\PAltura livre de 8 m e criterio ilustrativo, sujeito a local e norma aplicavel; ventos mecanicos sao cenarios uniformes sinteticos, nao vento de projeto.", "20/0: 20 °C e 0 m/s | 45/15: 45 °C e 15 m/s | 75/30: 75 °C e 30 m/s"),
        ("04_torre_suspensao", "TORRE DE SUSPENSAO - ELEVACAO E PLANTA", "Estrutura conceitual para feixe duplo CAA Drake em 138 kV", "Geometria e perfis sao conceituais; nao ha verificacao estrutural, fadiga, montagem ou fundacao.\\PAltura de 38 m e dimensoes preliminares de estudo.", "S: suspensao | fases em feixe 2x | OPGW: guarda optico | H: altura assumida"),
        ("05_torre_ancoragem", "TORRE DE ANCORAGEM - ELEVACAO E PLANTA", "Estrutura de retencao para terminacao e seccionamento do trecho", "Estrutura nao dimensionada para cargas de ruptura, angulos reais, vento ou montagem.\\PArranjo de ferragens deve ser confirmado pelo projeto mecanico especifico.", "A: ancoragem | CA: cadeia de ancoragem | T: tracao longitudinal | OPGW: cabo guarda"),
        ("06_cadeias_isoladores_ferragens", "CADEIAS DE ISOLADORES E FERRAGENS", "Suspensao, ancoragem, grampo de suspensao, amortecedor e OPGW", "Contagem de discos, distancia de escoamento e ferragens sao esquematicas.\\PCoordenacao de isolamento depende de poluicao, altitude, sobretensoes e especificacao do sistema.", "IS: isolador | GS: grampo suspensao | GA: grampo ancoragem | AHD: amortecedor"),
        ("07_arranjo_condutores_distancias", "ARRANJO DE FASES E DISTANCIAS GEOMETRICAS", "Configuracao horizontal de circuito simples com cabo(s) guarda", "Geometria de 7,5 m entre fases e altura media adotada para estimativas.\\PDistancias eletricas e afastamentos devem ser validados pelo corredor e requisitos vigentes.", "GMD: distancia media geometrica | GMR: raio medio geometrico | F1-F3: fases"),
        ("08_fundacoes_conceituais", "FUNDACOES CONCEITUAIS DAS ESTRUTURAS", "Planta de bases e secoes indicativas de blocos e stubs", "Solo, nivel d'agua, arrancamento, tombamento e concreto nao foram investigados.\\PDimensoes servem apenas para discutir interfaces civis e eletricas.", "B1-B4: bases de pernas | stub: extensao embutida | dimensoes ilustrativas em m"),
        ("09_aterramento_torres", "ATERRAMENTO CONCEITUAL DAS TORRES", "Aterramento local, contrapesos radiais e ligacao das pernas", "Resistividade de 100 Ω·m e comprimento de haste de 3 m sao premissas sinteticas.\\PModelo nao calcula tensoes de passo/toque, acoplamento, impulsos ou desempenho de protecao.", "H1-H4: hastes | CP: contrapeso | PE: ligacao a torre | ρ: resistividade assumida"),
        ("10_interfaces_subestacoes", "INTERFACES COM AS SUBESTACOES TERMINAIS", "Bay de linha, portal, para-raios, TP/CVT, OPGW e limites de escopo", "Arranjos terminais dependem do proprietario, estudos de conexao e padrao das subestacoes.\\PAs interfaces nao declaram atendimento a requisitos de acesso ou operacao.", "LA: para-raios | CVT: TP capacitivo | QL: disjuntor de linha | OPGW: fibra optica"),
    ],
    "p25": [
        ("01_diagrama_unifilar", "UNIFILAR DA USINA DE COGERACAO", "Gerador 25 MW / 13,8 kV, transformador elevador e conexao em 138 kV", "Geracao bruta de 25 MW; auxiliares estimados em 2,2 MW; exportacao liquida de 22,8 MW.\\PTransformador de 40 MVA; barra de geracao 13,8 kV e POI de 138 kV.", "G1: gerador 32 MVA | T1: 40 MVA, 13,8/138 kV | Qaux: auxiliares | POI: conexao"),
        ("02_implantacao_casa_maquinas", "IMPLANTACAO ELETRICA DA CASA DE MAQUINAS", "Planta conceitual cotada em coordenadas locais; bloco fisico em mm mostrado a 1:500", "Dimensoes de predios e equipamentos sao hipoteses de envelope, sem levantamento ou dados de fabricante.\\PRotas de cabo, vapor, agua, incendio, ventilacao e manutencao precisam de coordenacao multidisciplinar.", "CB1: caldeira | TG1: conjunto turbina-gerador | linha cinza: vapor | eixo TV1/G1: acoplamento mecanico | T1: elevador 40 MVA | QSA: auxiliares | origem: canto sudoeste"),
        ("03_layout_gerador_auxiliares", "GERADOR E EQUIPAMENTOS AUXILIARES", "Vista em planta e corte da linha de eixo, excitatriz e auxiliares principais", "Gerador sincronico de 32 MVA, 13,8 kV, 2 polos; rotacao sincrona de 3600 rpm.\\PDimensoes de carcaca e base nao fornecidas por fabricante.", "G1: gerador | EX: excitatriz | M1: bomba | F1: ventilador | 3~: trifasico"),
        ("04_transformador_conexao_rede", "TRANSFORMADOR ELEVADOR E CONEXAO A REDE", "Transformador 13,8/138 kV, bays de geracao e de linha", "Transformador 40 MVA com impedancia de 12% assumida.\\PProtecao, aterramento do neutro, isolamento e coordenacao dependem do arranjo real.", "T1: elevador | QG/QP: disjuntores | TC/TP: medicao | LA: para-raios"),
        ("05_sistema_excitacao_avr", "SISTEMA DE EXCITACAO E AVR", "Medicao de tensao, regulador automatico, limitadores e campo do gerador", "Blocos funcionais representativos; parametros de AVR sao valores de estudo, sem ensaio de resposta.\\PExcitacao real deve incluir limitadores e requisitos do fabricante e do operador.", "AVR: regulador de tensao | PT: TP | CT: TC | OEL/UEL: limitadores | Efd: campo"),
        ("06_regulador_velocidade_turbina", "REGULADOR DE VELOCIDADE DA TURBINA", "Sensor de velocidade, droop, controle de valvula e potencia mecanica", "Modelo dinamico simplificado; nao representa caldeira, combustao, vapor ou atuadores reais.\\PConstante de inercia, droop e tempos sao premissas ajustaveis.", "ω: velocidade | GOV: regulador | CV: valvula de controle | Pm: potencia mecanica"),
        ("07_sincronismo", "SINCRONISMO E FECHAMENTO DO DISJUNTOR", "Verificacao de tensao, frequencia, angulo e permissivos de fechamento", "Limites desenhados sao envelopes de ilustracao, nao ajustes aprovados.\\PFechamento requer sincronizador, rele de verificacao e intertravamentos independentes.", "25: sincronismo | 52: disjuntor | 27/59: tensao | 81: frequencia | Δφ: angulo"),
        ("08_protecao_gerador", "PROTECOES ELETRICAS DO GERADOR", "Zonas de protecao, TCs/TPs, diferencial e funcoes ANSI de gerador", "Funcoes listadas nao incluem estudo de ajustes, saturacao, estabilidade ou coordenacao.\\PProtecao final exige dados de fabricante e estudo de curto-circuito e estabilidade.", "87G: diferencial | 64G: terra estator | 40: perda excitacao | 32: potencia reversa | 46: sequencia negativa"),
        ("09_servicos_auxiliares", "QUADROS E SERVICOS AUXILIARES", "Distribuicao de baixa tensao, motores, UPS e sistema CC", "Carga auxiliar total preliminar de 2,2 MW, sem lista completa de consumidores.\\PAlimentacao de emergencia, partida autonoma e redundancia nao foram verificadas.", "QSA: servicos auxiliares | UPS: fonte ininterrupta | 125 Vcc: tensao conceitual"),
        ("10_aterramento_equipotencializacao", "ATERRAMENTO E PROTECAO DOS EQUIPAMENTOS", "Malha da casa de maquinas, gerador, transformador e estruturas metalicas", "Malha conceitual sem medicao de solo, corrente de falta ou verificacao de tensoes de toque/passo.\\PCoordenar com SPDA, neutro do gerador, neutro do transformador e protecoes.", "M: malha | BEP: barra equipotencial | N: neutro | PE: protecao | H: haste"),
    ],
}


def t(layout, value: str, x: float, y: float, h: float = 1.55, layer: str = "02_TEXTO", align=TextEntityAlignment.LEFT, style=TEXT_STYLE, rotation: float = 0.0) -> None:
    add_text(layout, value, (x, y), h, layer=layer, align=align, style=style, rotation=rotation)


def tc(layout, value: str, x: float, y: float, h: float = 1.55, layer: str = "02_TEXTO", style=TEXT_STYLE) -> None:
    t(layout, value, x, y, h, layer, TextEntityAlignment.MIDDLE_CENTER, style)


def ln(layout, x1: float, y1: float, x2: float, y2: float, layer: str = "05_POTENCIA", width: float | None = None) -> None:
    attrs = {"layer": layer}
    if width is not None:
        attrs["lineweight"] = int(round(width * 100))
    layout.add_line((x1, y1), (x2, y2), dxfattribs=attrs)


def poly(layout, points, layer: str = "04_EQUIPAMENTOS", close: bool = False, width: float | None = None) -> None:
    attrs = {"layer": layer}
    if width is not None:
        attrs["const_width"] = width
    layout.add_lwpolyline(points, close=close, dxfattribs=attrs)


def rect(layout, x1, y1, x2, y2, layer="04_EQUIPAMENTOS") -> None:
    add_rect(layout, x1, y1, x2, y2, layer)


def circle(layout, x: float, y: float, r: float, layer: str = "04_EQUIPAMENTOS") -> None:
    layout.add_circle((x, y), r, dxfattribs={"layer": layer})


def arrow(layout, x1: float, y1: float, x2: float, y2: float, layer: str = "05_POTENCIA", size: float = 2.0) -> None:
    ln(layout, x1, y1, x2, y2, layer)
    a = math.atan2(y2 - y1, x2 - x1)
    for da in (2.55, -2.55):
        ln(layout, x2, y2, x2 + size * math.cos(a + da), y2 + size * math.sin(a + da), layer)


def dim_h(layout, x1: float, x2: float, y: float, y_obj: float, label: str) -> None:
    ln(layout, x1, y_obj, x1, y, "03_COTAS")
    ln(layout, x2, y_obj, x2, y, "03_COTAS")
    ln(layout, x1, y, x2, y, "03_COTAS")
    for x, sgn in ((x1, 1), (x2, -1)):
        ln(layout, x - 1.4, y - 1.1, x + 1.4, y + 1.1, "03_COTAS")
    tc(layout, label, (x1 + x2) / 2, y + 2.0, 1.45, "03_COTAS")


def dim_v(layout, x: float, y1: float, y2: float, x_obj: float, label: str) -> None:
    ln(layout, x_obj, y1, x, y1, "03_COTAS")
    ln(layout, x_obj, y2, x, y2, "03_COTAS")
    ln(layout, x, y1, x, y2, "03_COTAS")
    ln(layout, x - 1.1, y1 - 1.4, x + 1.1, y1 + 1.4, "03_COTAS")
    ln(layout, x - 1.1, y2 - 1.4, x + 1.1, y2 + 1.4, "03_COTAS")
    t(layout, label, x - 2.2, (y1 + y2) / 2, 1.45, "03_COTAS", TextEntityAlignment.MIDDLE_CENTER, rotation=90)


def breaker(layout, x: float, y: float, label: str, vertical: bool = True, layer: str = "05_POTENCIA") -> None:
    if vertical:
        ln(layout, x, y - 7, x, y - 2.5, layer)
        ln(layout, x, y + 2.5, x, y + 7, layer)
        circle(layout, x - 1.5, y - 1.2, 1.0, layer)
        circle(layout, x + 1.5, y + 1.2, 1.0, layer)
        ln(layout, x - 1.1, y - 0.4, x + 1.1, y + 0.4, layer)
        tc(layout, label, x + 7.0, y, 1.25, "02_TEXTO")
    else:
        ln(layout, x - 7, y, x - 2.5, y, layer)
        ln(layout, x + 2.5, y, x + 7, y, layer)
        circle(layout, x - 1.3, y, 1.0, layer)
        circle(layout, x + 1.3, y, 1.0, layer)
        ln(layout, x - 0.5, y + 0.8, x + 0.6, y - 0.8, layer)
        tc(layout, label, x, y + 5, 1.15, "02_TEXTO")


def isolator(layout, x: float, y: float, vertical: bool = True, label: str = "DS") -> None:
    if vertical:
        ln(layout, x, y - 6, x, y - 1.6)
        ln(layout, x, y + 1.6, x, y + 6)
        ln(layout, x - 1.2, y - 1.6, x + 2.3, y + 2.1)
        circle(layout, x, y - 1.8, 0.8, "05_POTENCIA")
        circle(layout, x, y + 1.8, 0.8, "05_POTENCIA")
        tc(layout, label, x + 6, y, 1.15)
    else:
        ln(layout, x - 6, y, x - 1.6, y)
        ln(layout, x + 1.6, y, x + 6, y)
        ln(layout, x - 1.6, y - 1.2, x + 2.0, y + 2.1)
        circle(layout, x - 1.8, y, 0.8, "05_POTENCIA")
        circle(layout, x + 1.8, y, 0.8, "05_POTENCIA")
        tc(layout, label, x, y + 5.5, 1.15)


def transformer(layout, x: float, y: float, label: str, detail: str = "") -> None:
    circle(layout, x - 3.0, y, 5.0, "05_POTENCIA")
    circle(layout, x + 3.0, y, 5.0, "05_POTENCIA")
    tc(layout, label, x, y - 9.5, 1.35, "04_EQUIPAMENTOS", TITLE_STYLE)
    if detail:
        tc(layout, detail, x, y - 13.0, 1.05)


def ground(layout, x: float, y: float, layer: str = "05_POTENCIA") -> None:
    ln(layout, x, y, x, y - 4, layer)
    ln(layout, x - 3.3, y - 4, x + 3.3, y - 4, layer)
    ln(layout, x - 2.1, y - 5.8, x + 2.1, y - 5.8, layer)
    ln(layout, x - 0.9, y - 7.4, x + 0.9, y - 7.4, layer)


def equip(layout, x: float, y: float, w: float, h: float, tag: str, title: str, subtitle: str = "", layer="04_EQUIPAMENTOS") -> None:
    rect(layout, x, y, x + w, y + h, layer)
    ln(layout, x, y + h - 9, x + w, y + h - 9, layer)
    tc(layout, title, x + w / 2, y + h - 5.2, 1.45, layer, TITLE_STYLE)
    tc(layout, tag, x + w / 2, y + h / 2 - 0.4, 1.7, "02_TEXTO", TITLE_STYLE)
    if subtitle:
        tc(layout, subtitle, x + w / 2, y + 3.5, 1.05, "02_TEXTO")


def panel(layout, x: float, y: float, w: float, h: float, title: str, subtitle: str = "") -> None:
    rect(layout, x, y, x + w, y + h, "11_ARQUITETURA")
    tc(layout, title, x + w / 2, y + h - 5, 1.5, "11_ARQUITETURA", TITLE_STYLE)
    if subtitle:
        tc(layout, subtitle, x + w / 2, y + h - 9, 1.05)


def table(layout, x: float, y: float, widths: list[float], row_h: float, headers: list[str], rows: list[list[str]], font: float = 1.15) -> None:
    total = sum(widths)
    nrows = len(rows) + 1
    rect(layout, x, y - row_h * nrows, x + total, y, "12_LEGENDA")
    for i in range(1, nrows):
        ln(layout, x, y - row_h * i, x + total, y - row_h * i, "12_LEGENDA")
    xc = x
    for w in widths[:-1]:
        xc += w
        ln(layout, xc, y, xc, y - row_h * nrows, "12_LEGENDA")
    for row_i, values in enumerate([headers, *rows]):
        yy = y - row_h * (row_i + 0.5)
        xx = x
        for idx, value in enumerate(values):
            tc(layout, str(value), xx + widths[idx] / 2, yy, font, "12_LEGENDA", TITLE_STYLE if row_i == 0 else TEXT_STYLE)
            xx += widths[idx]


def add_sheet_frame(root: Path, config: dict, project_id: str, project_title: str, number: int, filename: str, title: str, subtitle: str, notes: str, legend: str, scale: str = "S/ESC."):
    geom = SheetGeometry.from_config(config)
    project_number = project_id.split("-", 1)[0]
    color_key = f"p{project_number}"
    if color_key not in config.get("project_layer_colors", {}):
        raise KeyError(f"Paleta ACI ausente em portfolio.toml: project_layer_colors.{color_key}")
    doc = configure_document(
        config,
        limits=(geom.width, geom.height),
        layer_color_overrides=config["project_layer_colors"][color_key],
    )
    md = doc.ezdxf_metadata()
    md["PORTFOLIO_PROJECT"] = project_id
    md["PORTFOLIO_SHEET"] = f"{number:02d}/10"
    md["PORTFOLIO_DATE"] = DATE
    define_title_block(doc)
    define_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geom)
    tc(layout, title, 210, 277, 3.5, "02_TEXTO", TITLE_STYLE)
    tc(layout, subtitle, 210, 271.5, 1.8)
    rect(layout, 18, 18, 224, 46, "13_NOTAS")
    t(layout, "AVISO OBRIGATORIO", 22, 42, 2.0, "13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, config["portfolio"]["warning"], (22, 37), 198, 1.45, "13_NOTAS")
    rect(layout, 18, 50, 224, 70, "13_NOTAS")
    t(layout, "NOTAS DA PRANCHA", 22, 66.5, 1.8, "13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, notes, (22, 62), 198, 1.28, "13_NOTAS")
    rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    t(layout, "LEGENDA", 22, 90.5, 1.8, "12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, legend, (22, 86), 198, 1.28, "12_LEGENDA")
    rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    ln(layout, 230, 86, 410, 86, "01_CARIMBO")
    for x in (248, 280, 352):
        ln(layout, x, 72, x, 94, "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("AUTOR", 381)):
        tc(layout, value, x, 89.5, 1.55, "01_CARIMBO")
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R. MENEGUELI", 381)):
        tc(layout, value, x, 78.5, 1.25, "02_TEXTO")
    values = {
        "TITULO": title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{number:02d}/10",
        "ARQUIVO": filename,
        "UNIDADES": "mm",
        "ESCALA": scale,
        "FOLHA": "A3",
        "STATUS": "CONCEIT.",
    }
    block = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    block.add_auto_attribs(values)
    return doc, layout


def d23_01(m, p):
    tc(m, "PONTO DE CONEXAO COM A REDE", 45, 245, 1.5, "02_TEXTO", TITLE_STYLE)
    circle(m, 35, 218, 8, "05_POTENCIA")
    tc(m, "138", 35, 219, 1.8, "05_POTENCIA", TITLE_STYLE)
    tc(m, "kV / 60 Hz", 35, 214, 1.15)
    ln(m, 43, 218, 75, 218)
    isolator(m, 82, 218, True, "89L")
    breaker(m, 105, 218, "52L")
    ln(m, 105, 225, 105, 239, "07_INSTRUMENTACAO")
    for y in (235, 239, 243):
        circle(m, 105, y, 1.0, "07_INSTRUMENTACAO")
    tc(m, "TC/TP PCC", 105, 246, 1.2, "07_INSTRUMENTACAO")
    ln(m, 105, 211, 105, 199)
    transformer(m, 105, 188, "T1", "45 MVA")
    ln(m, 105, 183, 105, 160)
    ln(m, 105, 160, 182, 160)
    arrow(m, 132, 160, 148, 160)
    tc(m, "34,5 kV - BARRA B1", 235, 163, 2.0, "05_POTENCIA", TITLE_STYLE)
    ln(m, 182, 160, 388, 160, "05_POTENCIA", 0.8)
    for x,tag in ((206,"52-F1"),(257,"52-A1"),(313,"52-S1"),(363,"52-FT")):
        ln(m, x, 160, x, 146)
        breaker(m, x, 137, tag)
    transformer(m, 206, 119, "TF1")
    tc(m, "30 MVA | 34,5 / 1,0 kV", 206, 101, 1.0)
    ln(m, 206, 114, 206, 105)
    ln(m, 206, 105, 224, 105)
    ln(m, 224, 105, 224, 119)
    rect(m, 230, 103, 275, 132, "11_ARQUITETURA")
    tc(m, "FORNO EAF", 252.5, 125, 1.8, "04_EQUIPAMENTOS", TITLE_STYLE)
    for x in (240, 252.5, 265):
        poly(m, [(x-3,109),(x,104),(x+3,109)], "05_POTENCIA")
    equip(m, 282, 108, 45, 27, "AUX", "CARGAS AUXILIARES", "6,4 MW; fp 0,88")
    ln(m, 257, 129, 257, 135, "05_POTENCIA")
    equip(m, 331, 108, 56, 27, "VSC", "STATCOM", "±12,5 MVAr")
    ln(m, 363, 135, 363, 160)
    table(m, 255, 251, [44, 32, 34, 30], 9.0, ["EQUIPAMENTO", "POTENCIA", "TENSAO", "IMPEDANCIA"], [["T1", "45 MVA", "138/34,5 kV", "12,5%*"],["TF1", "30 MVA", "34,5/1,0 kV", "10%*"],["SOMA CARGAS", "28,0 MW", "34,5 kV", "fp 0,757"]], 0.95)
    table(m, 32, 151, [41, 38, 37], 8.0, ["PONTO", "CORRENTE", "TENSAO"], [["PCC apos Q", "123 A", "138 kV"],["Barra B1", "493 A", "34,5 kV"],["TF1 BT", "17,32 kA", "1,0 kV"]], 1.0)
    tc(m, "* Impedancias de estudo, pendentes de dados de fabricante", 115, 207, 1.1, "13_NOTAS")


def d23_02(m, p):
    rect(m, 34, 111, 389, 251, "11_ARQUITETURA")
    tc(m, "PATIO 138 kV - AIS", 100, 244, 1.7, "11_ARQUITETURA", TITLE_STYLE)
    ln(m, 55, 224, 201, 224, "05_POTENCIA", 0.7)
    ln(m, 55, 221, 201, 221, "05_POTENCIA", 0.7)
    tc(m, "BARRAMENTO 138 kV", 128, 230, 1.45, "05_POTENCIA", TITLE_STYLE)
    for x in (70, 127, 184):
        rect(m, x-10, 152, x+10, 216, "10_ELETROCALHAS")
        for y, tag in ((205,"89"),(190,"TC"),(174,"52"),(158,"89")):
            circle(m, x, y, 2.2, "04_EQUIPAMENTOS")
            tc(m, tag, x+5, y, 1.0)
        ln(m, x, 216, x, 224, "05_POTENCIA")
    equip(m, 218, 179, 57, 48, "T1", "TRANSFORMADOR", "45 MVA / 138-34,5 kV")
    for x in (233, 261):
        circle(m, x, 168, 3.5, "03_COTAS")
        ln(m, x, 172, x, 179, "05_POTENCIA")
    tc(m, "BACIA DE CONTENCAO", 247, 160, 1.1)
    rect(m, 293, 153, 374, 226, "11_ARQUITETURA")
    tc(m, "CASA DE CUBICULOS 34,5 kV", 333, 218, 1.5, "11_ARQUITETURA", TITLE_STYLE)
    for i, x in enumerate(range(301, 368, 11), start=1):
        rect(m, x, 169, x+8, 210, "04_EQUIPAMENTOS")
        tc(m, f"Q{i}", x+4, 187, 1.15, "04_EQUIPAMENTOS", TITLE_STYLE)
        ln(m, x+4, 169, x+4, 160, "05_POTENCIA")
    ln(m, 276, 191, 293, 191, "05_POTENCIA", 0.6)
    rect(m, 51, 121, 121, 140, "11_ARQUITETURA")
    tc(m, "PORTARIA / ACESSO", 86, 131, 1.2, "11_ARQUITETURA")
    poly(m, [(45,145),(200,145),(210,150),(290,150),(290,140),(380,140)], "10_ELETROCALHAS")
    tc(m, "VIA INTERNA 6 m (ESQUEMATICA)", 166, 136, 1.05, "02_TEXTO")
    dim_h(m, 34, 389, 105, 111, "70 m - IMPLANTACAO ILUSTRATIVA")
    dim_v(m, 397, 111, 251, 389, "28 m")
    tc(m, "N", 383, 240, 2.4, "03_COTAS", TITLE_STYLE)
    arrow(m, 383, 226, 383, 238, "03_COTAS")


def d23_03(m, p):
    rect(m, 30, 112, 390, 252, "11_ARQUITETURA")
    tc(m, "NAVE DO FORNO - PLANTA ESQUEMATICA", 210, 243, 1.7, "11_ARQUITETURA", TITLE_STYLE)
    rect(m, 74, 135, 239, 223, "04_EQUIPAMENTOS")
    tc(m, "ZONA DE OPERACAO EAF", 156, 216, 1.6, "04_EQUIPAMENTOS", TITLE_STYLE)
    circle(m, 153, 172, 28, "04_EQUIPAMENTOS")
    circle(m, 153, 172, 18, "05_POTENCIA")
    poly(m, [(130,160),(145,152),(160,151),(178,162),(178,184),(161,193),(141,191),(128,179)], "04_EQUIPAMENTOS", True)
    tc(m, "CASCO / CUBA", 153, 171, 1.4, "04_EQUIPAMENTOS", TITLE_STYLE)
    for x in (145,153,161):
        ln(m, x, 220, x, 188, "06_COMANDO", 0.5)
        poly(m, [(x-2,188),(x,182),(x+2,188)], "06_COMANDO")
    tc(m, "E1-E3 / BRACOS DE ELETRODO", 153, 228, 1.25, "06_COMANDO")
    equip(m, 253, 187, 68, 34, "TF1", "TRANSFORMADOR DE FORNO", "30 MVA - ventilacao forcada")
    equip(m, 253, 143, 68, 30, "CCW", "SKID DE AGUA", "intertravamento de fluxo")
    rect(m, 328, 187, 372, 221, "04_EQUIPAMENTOS")
    tc(m, "PAINEL", 350, 207, 1.35, "04_EQUIPAMENTOS", TITLE_STYLE)
    tc(m, "REGULACAO", 350, 201, 1.1)
    rect(m, 328, 143, 372, 175, "04_EQUIPAMENTOS")
    tc(m, "CCM", 350, 160, 1.5, "04_EQUIPAMENTOS", TITLE_STYLE)
    poly(m, [(234,202),(246,202),(246,204),(253,204)], "08_CABOS")
    poly(m, [(234,153),(246,153),(246,157),(253,157)], "10_ELETROCALHAS")
    tc(m, "CABOS FLEXIVEIS REFRIGERADOS", 244, 211, 1.05, "08_CABOS")
    rect(m, 39, 197, 65, 220, "11_ARQUITETURA")
    tc(m, "PONTE", 52, 210, 1.4, "11_ARQUITETURA", TITLE_STYLE)
    ln(m, 39, 194, 65, 194, "11_ARQUITETURA")
    table(m, 247, 134, [38, 43, 43], 8, ["INTERFACE", "ORIGEM", "DESTINO"], [["Potencia", "TF1", "EAF"],["Agua", "CCW", "Cabos"],["Comando", "PLC", "Regulacao"]], 1.05)
    dim_h(m, 74, 239, 127, 135, "33 m")
    dim_v(m, 68, 135, 223, 74, "17,6 m")


def d23_04(m, p):
    panel(m, 29, 139, 174, 106, "T1 - TRANSFORMADOR RECEPTOR", "Corte longitudinal conceitual")
    rect(m, 51, 163, 180, 216, "04_EQUIPAMENTOS")
    for x in range(61, 172, 12):
        ln(m, x, 170, x, 209, "04_EQUIPAMENTOS")
        ln(m, x+3, 170, x+3, 209, "04_EQUIPAMENTOS")
    poly(m, [(70,163),(70,153),(161,153),(161,163)], "04_EQUIPAMENTOS")
    for x in (78,107,146):
        ln(m, x, 216, x, 231, "05_POTENCIA")
        circle(m, x, 235, 2.0, "05_POTENCIA")
    tc(m, "BUCHAS AT", 67, 239, 1.0)
    rect(m, 83, 142, 144, 154, "04_EQUIPAMENTOS")
    tc(m, "T1  45 MVA | 138/34,5 kV", 113.5, 148, 0.9, "04_EQUIPAMENTOS")
    dim_h(m, 51, 180, 131, 139, "13,0 m (referencia)")
    panel(m, 216, 139, 174, 106, "TF1 - TRANSFORMADOR DE FORNO", "Corte simplificado com comutador")
    rect(m, 236, 164, 369, 213, "04_EQUIPAMENTOS")
    for x in range(247, 360, 13):
        ln(m, x, 170, x, 206, "04_EQUIPAMENTOS")
    circle(m, 256, 190, 6, "05_POTENCIA")
    circle(m, 277, 190, 6, "05_POTENCIA")
    tc(m, "Nucleo", 266, 179, 1.0)
    rect(m, 332, 178, 358, 205, "06_COMANDO")
    tc(m, "OLTC", 345, 194, 1.25, "06_COMANDO", TITLE_STYLE)
    ln(m, 345, 178, 345, 166, "06_COMANDO")
    tc(m, "TAP", 345, 160, 1.1, "06_COMANDO")
    rect(m, 236, 142, 318, 154, "04_EQUIPAMENTOS")
    tc(m, "TF1  30 MVA | 34,5/1,0 kV", 277, 148, 0.9, "04_EQUIPAMENTOS")
    table(m, 35, 126, [45, 35, 41, 40], 7.0, ["TRANSFORMADOR", "S", "RELACAO", "Z*"], [["T1", "45 MVA", "138/34,5 kV", "12,5%"],["TF1", "30 MVA", "34,5/1,0 kV", "10,0%"]], 1.0)
    tc(m, "* VALORES DE IMPEDANCIA SAO PREMISSAS", 311, 128, 1.1, "13_NOTAS")


def d23_05(m, p):
    tc(m, "CIRCUITO DE MEDIA TENSAO", 82, 246, 1.45, "05_POTENCIA", TITLE_STYLE)
    ln(m, 40, 226, 128, 226, "05_POTENCIA", 0.7)
    for x in (57,84,111):
        ln(m, x, 226, x, 217)
    breaker(m, 84, 208, "52-F1")
    ln(m, 84, 201, 84, 187)
    transformer(m, 84, 176, "TF1", "30 MVA")
    ln(m, 84, 171, 84, 157)
    t(m, "34,5 kV / 1,0 kV; taps conceituais 0,8...1,2 kV", 40, 150, 1.2)
    tc(m, "SECUNDARIO DE ALTA CORRENTE", 250, 246, 1.45, "05_POTENCIA", TITLE_STYLE)
    ln(m, 165, 216, 342, 216, "05_POTENCIA", 0.7)
    ln(m, 165, 204, 342, 204, "05_POTENCIA", 0.7)
    ln(m, 165, 192, 342, 192, "05_POTENCIA", 0.7)
    for y, ph in ((216,"U"),(204,"V"),(192,"W")):
        tc(m, ph, 158, y, 1.15, "05_POTENCIA", TITLE_STYLE)
        poly(m, [(342,y),(355,y),(355,172)], "08_CABOS", False, 0.4)
    rect(m, 310, 163, 370, 181, "04_EQUIPAMENTOS")
    tc(m, "EAF / ELETRODOS", 340, 172, 1.3, "04_EQUIPAMENTOS", TITLE_STYLE)
    for x in (320,340,360):
        ln(m, x, 163, x, 151, "05_POTENCIA")
    equip(m, 178, 153, 75, 45, "TCW", "CABOS FLEXIVEIS", "refrigerados; 17,32 kA ref.")
    for y in (192,204,216):
        circle(m, 189, y-5, 1.5, "09_BORNES")
        ln(m, 189, y-3.5, 189, y-1, "08_CABOS")
    table(m, 40, 138, [53, 45, 45, 55], 8, ["CIRCUITO", "U", "I NOMINAL", "OBSERVACAO"], [["Primario TF1", "34,5 kV", "502 A", "30 MVA"],["Secundario TF1", "1,0 kV", "17,32 kA", "ideal 3φ"],["Taps", "0,8-1,2 kV", "variavel", "referencia"]], 1.05)
    arrow(m, 265, 184, 290, 184, "08_CABOS")
    tc(m, "CONEXOES FLEXIVEIS", 276, 190, 1.0, "08_CABOS")


def d23_06(m, p):
    panel(m, 28, 182, 105, 61, "ZONA 1 - T1", "87T / REF")
    panel(m, 151, 182, 105, 61, "ZONA 2 - B1", "87B / 50BF")
    panel(m, 274, 182, 114, 61, "ZONA 3 - FORNO", "50/51 / 49 / 46")
    transformer(m, 292, 159, "T1", "138/34,5 kV")
    ln(m, 292, 154, 292, 128, "05_POTENCIA")
    ln(m, 292, 128, 206, 128, "05_POTENCIA", 0.7)
    tc(m, "BARRA B1 - 34,5 kV", 206, 132, 1.4, "05_POTENCIA", TITLE_STYLE)
    ln(m, 206, 128, 372, 128, "05_POTENCIA", 0.7)
    breaker(m, 352, 151, "52-F1")
    ln(m, 352, 144, 352, 128, "05_POTENCIA")
    for x in (292,206,352):
        circle(m, x, 128, 2.3, "07_INSTRUMENTACAO")
        ln(m, x, 125.5, x, 113, "07_INSTRUMENTACAO")
        rect(m, x-22, 102, x+22, 113, "07_INSTRUMENTACAO")
        tc(m, "IED / MEDICAO", x, 107, 1.0, "07_INSTRUMENTACAO")
    table(m, 30, 176, [38, 51, 42, 42, 60], 8, ["FUNCAO", "ZONA", "ENTRADA", "SAIDA", "NOTA"], [["87T", "T1", "TC 1/2", "86T", "diferencial"],["50/51", "alimentador", "TC", "52-F1", "sem ajuste"],["27/59", "barra", "TP", "alarme/trip", "limites pendentes"],["87B", "B1", "TCs", "52", "conceitual"]], 1.0)
    for x in (118,242):
        ln(m, x, 213, x, 194, "07_INSTRUMENTACAO")
        ln(m, x, 194, x+7, 194, "07_INSTRUMENTACAO")
        ln(m, x+7, 194, x+7, 182, "07_INSTRUMENTACAO")
    tc(m, "BLOQUEIO 86 E INTERTRAVAMENTO DE ABERTURA", 322, 171, 1.15, "06_COMANDO", TITLE_STYLE)


def d23_07(m, p):
    ln(m, 35, 214, 386, 214, "05_POTENCIA", 0.8)
    tc(m, "BARRA 34,5 kV", 210, 219, 1.6, "05_POTENCIA", TITLE_STYLE)
    ln(m, 105, 214, 105, 190)
    breaker(m, 105, 181, "52-S")
    ln(m, 105, 174, 105, 160)
    transformer(m, 105, 149, "TS", f"34,5 / {p['furnace_secondary_voltage_kv']:.1f} kV")
    ln(m, 105, 144, 105, 134)
    rect(m, 54, 108, 164, 134, "04_EQUIPAMENTOS")
    tc(m, "REATANCIA DE ACOPLAMENTO", 109, 125, 1.25, "04_EQUIPAMENTOS", TITLE_STYLE)
    ln(m, 86, 117, 132, 117, "05_POTENCIA")
    for x in (93,101,109,117,125):
        poly(m, [(x-2,117),(x,113),(x+2,117)], "05_POTENCIA")
    ln(m, 109, 117, 109, 108)
    rect(m, 194, 112, 282, 161, "04_EQUIPAMENTOS")
    tc(m, "CONVERSOR VSC", 238, 154, 1.5, "04_EQUIPAMENTOS", TITLE_STYLE)
    for x in (214,234,254):
        rect(m, x, 129, x+12, 147, "06_COMANDO")
        tc(m, "IGBT", x+6, 138, 1.0, "06_COMANDO")
    ln(m, 210, 123, 266, 123, "05_POTENCIA", 0.7)
    ln(m, 210, 119, 266, 119, "05_POTENCIA", 0.7)
    tc(m, "LINK CC", 238, 115, 0.95)
    equip(m, 306, 147, 72, 48, "CTRL", "CONTROLE Q/V", "droop + limitador")
    for x1,y1,x2,y2 in ((282,137,306,160),(282,124,306,154),(378,171,386,214)):
        arrow(m,x1,y1,x2,y2,"07_INSTRUMENTACAO",1.6)
    p_furnace = p["furnace_transformer_mva"] * p["furnace_power_factor"]
    q_furnace = p["furnace_transformer_mva"] * math.sin(math.acos(p["furnace_power_factor"]))
    p_aux = p["auxiliary_active_mw"]
    q_aux = p_aux * math.tan(math.acos(p["auxiliary_power_factor"]))
    p_total = p_furnace + p_aux
    q_raw = q_furnace + q_aux
    q_target = p_total * math.tan(math.acos(p["target_power_factor"]))
    q_statcom = max(0.0, q_raw - p["filter_total_mvar"] - q_target)
    fmt = lambda value: f"{value:.2f}".replace(".", ",")
    table(
        m, 190, 270, [46,44,47,46], 8.0,
        ["ITEM", "VALOR", "UNID.", "BASE"],
        [
            ["P total", fmt(p_total), "MW", "forno + aux."],
            ["Q bruta", fmt(q_raw), "MVAr", "cargas"],
            ["Q filtros", fmt(p["filter_total_mvar"]), "MVAr", "hipotese"],
            ["Q alvo PCC", fmt(q_target), "MVAr", f"FP {p['target_power_factor']:.2f}"],
            ["Q STATCOM req.", fmt(q_statcom), "MVAr", f"lim. ±{fmt(p['statcom_limit_mvar'])}"],
        ],
        1.0,
    )
    tc(m, "CONTROLE DE CORRENTE dq, PLL E LIMITACAO DE CORRENTE - REPRESENTACAO FUNCIONAL", 245, 104, 1.0, "06_COMANDO")


def d23_08(m, p):
    ln(m, 36, 220, 385, 220, "05_POTENCIA", 0.7)
    tc(m, "BARRA 34,5 kV - DERIVACOES DE FILTRO", 210, 226, 1.5, "05_POTENCIA", TITLE_STYLE)
    xs = [92,205,318]
    names = [
        ("F5", f"{p['filter_5th_mvar']:.1f}".replace(".", ",") + " MVAr", 5),
        ("F7", f"{p['filter_7th_mvar']:.1f}".replace(".", ",") + " MVAr", 7),
        ("HP", f"{p['filter_highpass_mvar']:.1f}".replace(".", ",") + " MVAr", 11),
    ]
    for x,(name,rating,harm) in zip(xs,names):
        ln(m, x, 220, x, 205)
        breaker(m, x, 197, "52-"+name)
        ln(m, x, 190, x, 178)
        rect(m, x-24, 139, x+24, 178, "04_EQUIPAMENTOS")
        tc(m, name+" - RAMO", x, 172, 1.15, "04_EQUIPAMENTOS", TITLE_STYLE)
        ln(m, x, 166, x, 161)
        for dx in (-11,0,11):
            poly(m, [(x+dx-3,160),(x+dx,155),(x+dx+3,160)], "04_EQUIPAMENTOS")
        ln(m, x-16, 153, x+16, 153, "04_EQUIPAMENTOS")
        ln(m, x, 153, x, 148)
        circle(m, x, 145, 2.2, "04_EQUIPAMENTOS")
        tc(m, "C", x-9, 145, 1.1)
        if name != "HP":
            for dx in (-13,0,13):
                ln(m, x+dx, 153, x+dx, 145, "04_EQUIPAMENTOS")
            tc(m, "L", x+8, 159, 1.0)
        else:
            rect(m, x-9, 139, x+9, 146, "06_COMANDO")
            tc(m, "R", x, 142, 1.0, "06_COMANDO")
        tc(m, f"{name}: {rating}", x, 130, 1.2, "02_TEXTO", TITLE_STYLE)
        tc(m, f"sintonia {harm}a ordem (premissa)", x, 125, 1.0)
    table(m, 45, 270, [44,37,40,40,42], 8.5, ["RAMO", "Q1", "FUND.", "SINTONIA", "STATUS"], [["F5", names[0][1], "34,5 kV", "5a", "premissa"],["F7", names[1][1], "34,5 kV", "7a", "premissa"],["HP", names[2][1], "34,5 kV", "amortec.", "premissa"]], 1.0)
    tc(m, "ESPECTRO DE CORRENTE INJETADA ASSUMIDO", 210, 113, 1.25, "07_INSTRUMENTACAO", TITLE_STYLE)
    for i,(order,pu) in enumerate(zip(p["harmonic_orders"],p["harmonic_current_pu"])):
        x=248+i*27
        rect(m, x, 117, x+12, 117+pu*95, "07_INSTRUMENTACAO")
        tc(m, f"{order}a", x+6, 112, 1.0)
        tc(m, f"{pu*100:.0f}%", x+6, 120+pu*95, 0.95, "07_INSTRUMENTACAO")


def d23_09(m, p):
    rect(m, 45, 116, 277, 247, "11_ARQUITETURA")
    tc(m, "MALHA DE ATERRAMENTO - PLANTA ESQUEMATICA", 161, 238, 1.45, "11_ARQUITETURA", TITLE_STYLE)
    for x in range(62, 266, 17):
        ln(m,x,132,x,228,"08_CABOS",0.35)
    for y in range(132,229,16):
        ln(m,62,y,266,y,"08_CABOS",0.35)
    for x,y in ((62,132),(266,132),(62,228),(266,228),(130,180),(210,180)):
        circle(m,x,y,2.4,"07_INSTRUMENTACAO")
        tc(m,"H",x+4,y+2,0.95,"07_INSTRUMENTACAO")
    equip(m, 79, 184, 53, 26, "T1", "T1", "carcaca + neutro")
    equip(m, 178, 184, 58, 26, "QF", "CUBICULOS", "PE / porta / painel")
    ln(m, 104, 184, 104, 163, "08_CABOS")
    ln(m, 207, 184, 207, 163, "08_CABOS")
    tc(m,"BARRA DE EQUIPOTENCIALIZACAO BEP",165,157,1.1,"08_CABOS")
    rect(m, 294, 174, 384, 244, "13_NOTAS")
    tc(m,"PONTOS A MEDIR",339,236,1.4,"13_NOTAS",TITLE_STYLE)
    for i,txt in enumerate(("ρ do solo por camada","Icc e tempo de eliminacao","toque e passo","continuidade de ligacoes","interferencia com tubulacoes")):
        t(m,"- "+txt,301,222-i*8,1.12,"13_NOTAS")
    table(m, 298, 156, [43,39], 8, ["ITEM", "PREMISSA"], [["Condutor", "Cu nu"],["Espacamento", "8 m"],["Haste", "3 m"],["Solo", "100 Ω·m"]], 1.0)
    dim_h(m, 62, 266, 124, 132, "32 m - esquematico")
    dim_v(m, 55, 132, 228, 62, "16 m")


def d23_10(m, p):
    x0=39
    steps=[("S0", "Rede 138 kV normal", "PCC permissivo"),("S1","T1 energizado / B1 estavel","QF aberto"),("S2","Fluxo CCW validado","FL1-3 OK"),("S3","Protecoes 87T/86 reset","sem bloqueio"),("S4","Comando do operador","modo fusao"),("S5","Taps e eletrodos prontos","habilita arco"),("S6","Rampa de potencia","limites I/Q"),("S7","Fim de corrida / falha","abre QF / bloqueia")]
    for i,(tag,title,sub) in enumerate(steps):
        x=x0+(i%4)*91
        y=209-(i//4)*67
        rect(m,x,y,x+76,y+35,"06_COMANDO")
        tc(m,tag,x+7,y+27,1.25,"06_COMANDO",TITLE_STYLE)
        tc(m,title,x+40,y+21,1.2,"02_TEXTO")
        tc(m,sub,x+40,y+12,1.0,"07_INSTRUMENTACAO")
        if i in (0,1,2,4,5,6):
            arrow(m,x+76,y+17,x+88,y+17,"06_COMANDO",1.4)
    arrow(m, 377, 226, 377, 176, "06_COMANDO", 1.5)
    arrow(m, 377, 159, 39, 159, "06_COMANDO", 1.5)
    arrow(m, 39, 159, 39, 226, "06_COMANDO", 1.5)
    tc(m,"TRIP GERAL / EMERGENCIA",208,149,1.5,"06_COMANDO",TITLE_STYLE)
    panel(m, 52, 106, 145, 31, "PERMISSIVOS", "agua, protecao, portas, ventilacao, eletrodos")
    panel(m, 222, 106, 145, 31, "TRIPS", "87T, 50/51, falta de fluxo, emergencia, arco anormal")
    arrow(m, 124, 137, 124, 150, "07_INSTRUMENTACAO",1.3)
    arrow(m, 294, 137, 294, 150, "07_INSTRUMENTACAO",1.3)
    tc(m,"A logica nao substitui analise de risco, SIL/PL nem validacao funcional",210,245,1.2,"13_NOTAS")


def d24_01(m, p):
    rect(m, 31, 111, 389, 251, "11_ARQUITETURA")
    tc(m,"CORREDOR FICTICIO - 30 km / CIRCUITO SIMPLES",210,243,1.55,"11_ARQUITETURA",TITLE_STYLE)
    pts=[]
    for k,z in zip(p["route_km"],p["route_elevation_m"]):
        pts.append((45+k*10.4,180+(z-95)*0.7))
    poly(m,pts,"10_ELETROCALHAS",False,0.45)
    for km in range(31):
        x=45+km*10.4
        y=180+((p["route_elevation_m"][min(round(km/2),15)]-95)*0.7)
        ln(m,x,y-3,x,y+3,"03_COTAS")
        if km%2==0:
            circle(m,x,y,1.6,"04_EQUIPAMENTOS")
            tc(m,f"{km:02d}",x,y-7,0.95,"03_COTAS")
    tc(m,"SE A",45,221,1.6,"04_EQUIPAMENTOS",TITLE_STYLE)
    tc(m,"SE B",357,210,1.6,"04_EQUIPAMENTOS",TITLE_STYLE)
    poly(m,[(125,194),(140,203),(153,194),(165,194)],"04_EQUIPAMENTOS")
    tc(m,"TRAVESSIA FICTICIA DE CURSO D'AGUA",147,210,1.0,"13_NOTAS")
    poly(m,[(255,170),(270,180),(286,170)],"04_EQUIPAMENTOS")
    tc(m,"VIA VICINAL ESQUEMATICA",270,185,1.0,"13_NOTAS")
    ln(m,45,126,357,126,"03_COTAS")
    for x in (45,97,149,201,253,305,357):
        ln(m,x,124,x,129,"03_COTAS")
    for i,km in enumerate((0,5,10,15,20,25,30)):
        tc(m,f"km {km}",45+km*10.4,119,1.0,"03_COTAS")
    tc(m,"101 estruturas indicativas; espaco medio 300 m; alinhamento inventado para exercicio",210,107,1.1,"13_NOTAS")


def d24_02(m, p):
    x0,y0,w,h=43,124,330,104
    rect(m,x0-5,y0-6,x0+w+5,y0+h+23,"11_ARQUITETURA")
    tc(m,"PERFIL LONGITUDINAL - TERRENO FICTICIO E CONDUTORES CALCULADOS",210,250,1.8,"11_ARQUITETURA",TITLE_STYLE)
    def page_x(km): return x0+km/30*w
    def page_y(z): return y0+(z-90)*1.1
    terrain=[(page_x(km),page_y(z)) for km,z in zip(p["route_km"],p["route_elevation_m"])]
    poly(m,terrain,"11_ARQUITETURA",False,0.55)
    # All 100 spans are sampled from the same parameterized compatibility model
    # used by P24-03 and the MATLAB result table.
    span=p["span_m"]
    hot_sag=sag_values(p,75.0,0.0)[0]
    reference_sag=sag_values(p,20.0,1.0)[0]
    for s in range(100):
        km0=s*span/1000
        km1=(s+1)*span/1000
        z0=interp_profile(p,km0)
        z1=interp_profile(p,km1)
        xs_hot=[]; ys_hot=[]; xs_ref=[]; ys_ref=[]
        for j in range(11):
            u=j/10
            km=km0+(km1-km0)*u
            ground=z0*(1-u)+z1*u
            zhot=ground+p["mean_conductor_height_m"]-hot_sag*4*u*(1-u)
            zref=ground+p["mean_conductor_height_m"]-reference_sag*4*u*(1-u)
            xs_hot.append(page_x(km)); ys_hot.append(page_y(zhot))
            xs_ref.append(page_x(km)); ys_ref.append(page_y(zref))
        poly(m,list(zip(xs_hot,ys_hot)),"05_POTENCIA",False,0.55)
        poly(m,list(zip(xs_ref,ys_ref)),"08_CABOS",False,0.4)
    for s in range(101):
        km=s*span/1000
        x=page_x(km)
        z=interp_profile(p,km)
        y=page_y(z)
        ln(m,x,y,x,y+5,"03_COTAS")
    for km in p["anchor_stations_km"]:
        x=page_x(km); y=page_y(interp_profile(p,km))
        ln(m,x,y,x,y+p["tower_height_m"]*1.1,"04_EQUIPAMENTOS",0.65)
        tc(m,"A",x,y+p["tower_height_m"]*1.1+3,1.0,"04_EQUIPAMENTOS",TITLE_STYLE)
    for km in range(0,31,2):
        x=x0+km/30*w
        ln(m,x,y0-2,x,y0+h,"03_COTAS")
        tc(m,f"{km:02d}",x,y0-5,1.25,"03_COTAS")
    for i in range(6):
        y=y0+i*16.5
        ln(m,x0-3,y,x0+w+3,y,"03_COTAS")
        tc(m,f"{90+i*15} m",x0-4,y,1.15,"03_COTAS")
    tc(m,"elevacao sintetica (m)",35,183,1.25,"03_COTAS")
    tc(m,"progressiva (km)",210,114,1.25,"03_COTAS")
    tc(m,"V = 1:909 | H = 1:90 909 | exagero vertical = 100x",210,111,1.2,"13_NOTAS")
    tc(m,"ANCORAGENS / ESTACAS: 0+000 | 9+900 | 20+100 | 30+000; vao final ate proxima estrutura = 0 m",210,101,1.2,"13_NOTAS")
    tc(m,"VERMELHO: 75 °C / 0 m/s",337,218,1.3,"05_POTENCIA",TITLE_STYLE)
    tc(m,"VERDE: 20 °C / 1 m/s",337,213,1.3,"08_CABOS",TITLE_STYLE)


def interp_profile(p,km):
    return float(np.interp(km,p["route_km"],p["route_elevation_m"]))


def sag_values(p, temp_c, wind_m_s):
    g=9.80665
    span=p["span_m"]
    mass=p["conductor_mass_kg_m"]
    wv=mass*g
    d=p["conductor_diameter_m"]
    ww=0.5*p["air_density_kg_m3"]*p["drag_coefficient"]*d*wind_m_s**2
    we=math.hypot(wv,ww)
    ea=p["conductor_ea_n"]
    alpha=p["conductor_alpha_per_c"]
    h0=p["reference_horizontal_tension_n"]
    f0=wv*span**2/(8*h0)
    s0=span+8*f0**2/(3*span)
    unstressed=s0/(1+h0/ea)*(1+alpha*(temp_c-p["reference_temperature_c"]))
    def arc(h):
        f=we*span**2/(8*h)
        length=span+8*f*f/(3*span)
        return length/(1+h/ea)
    lo,hi=1000.0,500000.0
    for _ in range(100):
        mid=(lo+hi)/2
        if arc(mid)>unstressed:
            lo=mid
        else:
            hi=mid
    hh=(lo+hi)/2
    sag_v=wv*span**2/(8*hh)
    sag_r=we*span**2/(8*hh)
    t_support=math.hypot(hh,we*span/2)
    sag_h=ww*span**2/(8*hh)
    return sag_v,sag_r,hh,t_support,sag_h


def d24_03(m, p):
    x0,x1,y0,y1=62,354,127,224
    rect(m,42,112,373,251,"11_ARQUITETURA")
    tc(m,"VAO NOMINAL DE 300 m - MODELO PARABOLICO",210,260,1.8,"11_ARQUITETURA",TITLE_STYLE)
    for y in (130,160,190,220):
        ln(m,x0,y,x1,y,"03_COTAS")
        tc(m,f"{y-120:02d} m",52,y,0.9,"03_COTAS")
    for x in (x0,x1):
        ln(m,x,132,x,225,"04_EQUIPAMENTOS",0.6)
        circle(m,x,225,2,"04_EQUIPAMENTOS")
    styles=[(p["mechanical_conductor_temperatures_c"][0],p["mechanical_wind_speeds_m_s"][0],"05_POTENCIA"),
            (p["mechanical_conductor_temperatures_c"][1],p["mechanical_wind_speeds_m_s"][1],"06_COMANDO"),
            (p["mechanical_conductor_temperatures_c"][2],p["mechanical_wind_speeds_m_s"][2],"08_CABOS")]
    details=[]
    for temp,wind,layer in styles:
        sag,_,h,tens,sag_horizontal=sag_values(p,temp,wind)
        pts=[]
        for i in range(41):
            u=i/40
            y=220-sag*3.8*(4*u*(1-u))
            x=x0+(x1-x0)*u
            pts.append((x,y))
        poly(m,pts,layer,False,0.45)
        details.append((f"{temp}°C / {wind} m/s",f"f. vert. {sag:.2f} m; f. transv. {sag_horizontal:.2f} m; H {h/1000:.1f} kN"))
    tc(m,"TERRENO / REFERENCIA DE ALTURA LIVRE",210,139,1.0,"11_ARQUITETURA")
    ln(m,60,137,356,137,"11_ARQUITETURA")
    tc(m,"F1",62,230,1.1,"04_EQUIPAMENTOS",TITLE_STYLE)
    tc(m,"F2",354,230,1.1,"04_EQUIPAMENTOS",TITLE_STYLE)
    table(m,70,251,[47,98],8,["CONDICAO","RESULTADO MECANICO"],[[a,b] for a,b in details],1.4)
    dim_h(m,x0,x1,121,127,"300 m")
    tc(m,"Envelopes ilustrativos; alturas e afastamentos reais dependem da topografia e das regras aplicaveis",210,106,1.2,"13_NOTAS")


def draw_tower(m,p,anchor=False):
    cx=185
    base_y=119
    height=111
    top_y=base_y+height
    width0=57 if anchor else 48
    width_top=9
    tc(m,"ESTRUTURA DE RETENCAO" if anchor else "ESTRUTURA DE SUSPENSAO",210,251,1.5,"04_EQUIPAMENTOS",TITLE_STYLE)
    ln(m,cx-width_top/2,top_y,cx-width0/2,base_y,"04_EQUIPAMENTOS",0.7)
    ln(m,cx+width_top/2,top_y,cx+width0/2,base_y,"04_EQUIPAMENTOS",0.7)
    ln(m,cx-width0/2,base_y,cx+width0/2,base_y,"04_EQUIPAMENTOS",0.7)
    for i in range(1,9):
        y=base_y+i*height/9
        w=width0-(width0-width_top)*i/9
        ln(m,cx-w/2,y,cx+w/2,y,"04_EQUIPAMENTOS",0.45)
        yprev=base_y+(i-1)*height/9
        wp=width0-(width0-width_top)*(i-1)/9
        if i%2:
            ln(m,cx-wp/2,yprev,cx+w/2,y,"04_EQUIPAMENTOS",0.4)
            ln(m,cx+wp/2,yprev,cx-w/2,y,"04_EQUIPAMENTOS",0.4)
        else:
            ln(m,cx-wp/2,yprev,cx-w/2,y,"04_EQUIPAMENTOS",0.4)
            ln(m,cx+wp/2,yprev,cx+w/2,y,"04_EQUIPAMENTOS",0.4)
    # shield wire peak and crossarms
    ln(m,cx,top_y,cx,top_y+9,"05_POTENCIA")
    circle(m,cx,top_y+10,1.8,"05_POTENCIA")
    tc(m,"OPGW",cx+8,top_y+10,1.0,"08_CABOS")
    for dy,arm in ((-6,45),(-24,56),(-44,68)):
        y=top_y+dy
        ln(m,cx-arm/2,y,cx+arm/2,y,"04_EQUIPAMENTOS",0.6)
        for sgn in (-1,1):
            xx=cx+sgn*arm/2
            ln(m,xx,y,xx,y-9,"04_EQUIPAMENTOS")
            if anchor:
                ln(m,xx,y-9,xx+sgn*10,y-9,"05_POTENCIA")
                ln(m,xx+sgn*10,y-9,xx+sgn*22,y-9,"05_POTENCIA")
                circle(m,xx+sgn*22,y-9,1.4,"05_POTENCIA")
            else:
                for i in range(5):
                    circle(m,xx,y-10-i*2.3,0.9,"04_EQUIPAMENTOS")
                circle(m,xx,y-23,1.8,"05_POTENCIA")
            tc(m,f"F{1 if dy==-44 else 2 if dy==-24 else 3}",xx+sgn*4,y-27,1.0,"05_POTENCIA")
    for sgn in (-1,1):
        ln(m,cx+sgn*width0/2,base_y,cx+sgn*width0/2-12,base_y-7,"04_EQUIPAMENTOS")
        rect(m,cx+sgn*width0/2-17,base_y-11,cx+sgn*width0/2-7,base_y-7,"04_EQUIPAMENTOS")
    dim_v(m,111,base_y,top_y,150,"38 m")
    dim_h(m,cx-width0/2,cx+width0/2,base_y-17,base_y,"base 19,0 m")
    panel(m,263,184,115,51,"DADOS DE ESTUDO","1 circuito; 3 fases; 2 guarda")
    for i,label in enumerate(("Altura total: 38 m","Vao de referencia: 300 m",p["conductor_name"],"Feixe: 2x / 0,4 m; estrutura nao verificada")):
        t(m,"• "+label,269,218-i*8,1.5,"02_TEXTO")


def d24_06(m,p):
    panel(m,35,142,150,99,"CADEIA DE SUSPENSAO","Fase 138 kV - detalhe esquematico")
    ln(m,108,225,108,214,"04_EQUIPAMENTOS")
    for i in range(10):
        y=212-i*5.2
        circle(m,108,y,2.2,"04_EQUIPAMENTOS")
        ln(m,105.8,y,110.2,y,"04_EQUIPAMENTOS")
    ln(m,108,160,108,149,"04_EQUIPAMENTOS")
    rect(m,92,143,124,151,"04_EQUIPAMENTOS")
    ln(m,108,143,108,132,"05_POTENCIA")
    circle(m,108,129,2,"05_POTENCIA")
    tc(m,"10 discos - ilustrativo",108,119,1.0)
    dim_v(m,75,160,214,92,"0,54 m (indicativo)")
    panel(m,220,142,165,99,"CADEIA DE ANCORAGEM + OPGW","ferragens indicativas")
    ln(m,235,208,267,208,"05_POTENCIA",0.7)
    for i in range(8):
        x=268+i*5.5
        circle(m,x,208,2.1,"04_EQUIPAMENTOS")
    ln(m,315,208,337,208,"04_EQUIPAMENTOS")
    poly(m,[(337,208),(347,201),(352,208),(347,215),(337,208)],"04_EQUIPAMENTOS")
    circle(m,357,208,3,"08_CABOS")
    tc(m,"grampo",348,192,1.0)
    tc(m,"OPGW 15,2 mm*",342,224,1.0,"08_CABOS")
    for i,(txt,y) in enumerate((("olhal / manilha",181),("haste e garfo",170),("isoladores",159),("grampo de ancoragem",148))):
        t(m,"• "+txt,231,y,1.1,"02_TEXTO")
    tc(m,"* diametro conceitual",315,148,1.0,"13_NOTAS")


def d24_07(m,p):
    rect(m,36,114,388,248,"11_ARQUITETURA")
    tc(m,"SECAO TRANSVERSAL - FEIXE DUPLO POR FASE",212,240,2.0,"11_ARQUITETURA",TITLE_STYLE)
    tower_y=135
    cx=190
    ln(m,cx-5,tower_y,cx-5,226,"04_EQUIPAMENTOS",0.6)
    ln(m,cx+5,tower_y,cx+5,226,"04_EQUIPAMENTOS",0.6)
    for y,arm in ((218,65),(192,80),(166,95)):
        ln(m,cx-arm/2,y,cx+arm/2,y,"04_EQUIPAMENTOS",0.5)
    phase_scale=5.2
    xph=[cx+(d-(p["phase_spacing_m"][0]+p["phase_spacing_m"][1]+p["phase_spacing_m"][2])/3)*phase_scale for d in p["phase_spacing_m"]]
    bundle_offset=p["bundle_spacing_m"]*phase_scale/2
    for i,x in enumerate(xph,1):
        for dx in (-bundle_offset,bundle_offset):
            circle(m,x+dx,166,1.8,"05_POTENCIA")
        tc(m,f"F{i} x2",x,157,1.2,"05_POTENCIA",TITLE_STYLE)
    for x in (cx-25,cx+25):
        circle(m,x,218,2.3,"08_CABOS")
    tc(m,"OPGW / GUARDA",cx,224,1.3,"08_CABOS")
    dim_h(m,xph[0],xph[1],181,166,f"{p['phase_spacing_m'][1]-p['phase_spacing_m'][0]:.1f} m")
    dim_h(m,xph[1],xph[2],181,166,f"{p['phase_spacing_m'][2]-p['phase_spacing_m'][1]:.1f} m")
    dim_v(m,320,135,166,190,f"{p['mean_conductor_height_m']:.0f} m - altura de fixacao")
    ln(m,65,135,318,135,"11_ARQUITETURA")
    tc(m,"terreno de referencia",300,130,0.95,"11_ARQUITETURA")
    gmd=math.prod([abs(p["phase_spacing_m"][1]-p["phase_spacing_m"][0]),abs(p["phase_spacing_m"][2]-p["phase_spacing_m"][1]),abs(p["phase_spacing_m"][2]-p["phase_spacing_m"][0])])**(1/3)
    gmrb=math.sqrt(p["conductor_gmr_m"]*p["bundle_spacing_m"])
    tc(m,f"Feixe: {p['bundle_subconductors']}x CAA; afastamento {p['bundle_spacing_m']:.2f} m",78,210,1.5,"12_LEGENDA")
    tc(m,f"GMD = {gmd:.2f} m; GMR equivalente feixe = {gmrb*1000:.1f} mm",91,201,1.5,"12_LEGENDA")
    tc(m,f"Raio externo = {p['conductor_diameter_m']*500:.2f} mm; condutor {p['conductor_name']}",106,192,1.3,"12_LEGENDA")
    panel(m,65,145,98,30,"DISTANCIAS", "valores geometricos de estudo")
    panel(m,244,145,105,30,"BLINDAGEM", "angulo e cabos guarda a validar")


def d24_08(m,p):
    panel(m,39,142,149,99,"PLANTA - 4 BASES","dimensoes conceituais")
    pts=[(72,165),(154,165),(72,215),(154,215)]
    for i,(x,y) in enumerate(pts,1):
        rect(m,x-9,y-7,x+9,y+7,"04_EQUIPAMENTOS")
        circle(m,x,y,2.4,"04_EQUIPAMENTOS")
        tc(m,f"B{i}",x,y-12,1.0,"02_TEXTO")
    ln(m,72,190,154,190,"08_CABOS")
    ln(m,113,165,113,215,"08_CABOS")
    dim_h(m,72,154,151,165,"8,0 m")
    dim_v(m,63,165,215,72,"5,0 m")
    panel(m,215,142,170,99,"CORTE DE BLOCO ISOLADO","sem parametros geotecnicos")
    poly(m,[(244,224),(244,160),(346,160),(346,224)],"11_ARQUITETURA")
    ln(m,225,175,376,175,"11_ARQUITETURA")
    tc(m,"terreno",366,178,1.0,"11_ARQUITETURA")
    poly(m,[(278,215),(268,201),(268,179),(322,179),(322,201),(312,215)],"04_EQUIPAMENTOS")
    ln(m,295,223,295,190,"04_EQUIPAMENTOS",0.6)
    tc(m,"stub",304,208,1.0,"02_TEXTO")
    dim_v(m,335,179,215,322,"2,0 m*",)
    tc(m,"* altura ilustrativa",296,153,1.0,"13_NOTAS")
    table(m,48,130,[45,43,45,40],7.0,["VERIFICACAO","DADO","STATUS","PENDENCIA"],[["arrancamento","-","aberto","solo"],["tombamento","-","aberto","vento"],["concreto","-","aberto","estrutural"]],0.95)


def d24_09(m,p):
    rect(m,41,117,260,244,"11_ARQUITETURA")
    tc(m,"ATERRAMENTO DA TORRE - PLANTA",150,237,1.5,"11_ARQUITETURA",TITLE_STYLE)
    cx,cy=150,178
    poly(m,[(cx,cy+12),(cx+12,cy),(cx,cy-12),(cx-12,cy)],"04_EQUIPAMENTOS",True)
    for a in (0,90,180,270):
        ang=math.radians(a)
        x2=cx+62*math.cos(ang); y2=cy+51*math.sin(ang)
        ln(m,cx,cy,x2,y2,"08_CABOS",0.6)
        circle(m,x2,y2,2.3,"07_INSTRUMENTACAO")
        tc(m,f"H{a//90+1}",x2+4,y2+3,1.0,"07_INSTRUMENTACAO")
        for frac in (0.25,0.5,0.75):
            x=cx+(x2-cx)*frac; y=cy+(y2-cy)*frac
            ln(m,x-1.8,y-1.8,x+1.8,y+1.8,"08_CABOS")
            ln(m,x-1.8,y+1.8,x+1.8,y-1.8,"08_CABOS")
    for dx in (-28,-14,0,14,28):
        ln(m,cx+dx,cy-25,cx+dx,cy+25,"08_CABOS",0.35)
    for dy in (-25,-12,0,12,25):
        ln(m,cx-35,cy+dy,cx+35,cy+dy,"08_CABOS",0.35)
    panel(m,280,174,105,67,"PREMISSAS DE ESTUDO","sem medicao de campo")
    for i,txt in enumerate(("ρ = 100 Ω·m","4 hastes x 3 m","contrapesos radiais","secao de condutor nao fechada")):
        t(m,"• "+txt,286,221-i*9,1.0)
    panel(m,280,119,105,43,"VERIFICACOES EM ABERTO","toque / passo / impulsos")
    dim_h(m,88,212,131,143,"contrapeso 15 m*")
    tc(m,"* extensao indicativa, a revisar",330,110,0.95,"13_NOTAS")


def d24_10(m,p):
    for x,title,sub in ((37,"SE A - SAIDA LT","138 kV"),(226,"SE B - CHEGADA LT","138 kV")):
        panel(m,x,157,155,83,title,sub)
        ln(m,x+10,220,x+145,220,"05_POTENCIA",0.7)
        for j,tag in enumerate(("89L","LA","CVT","TC","52L","89B")):
            xx=x+22+j*22
            ln(m,xx,220,xx,201,"05_POTENCIA")
            if tag in ("52L",): breaker(m,xx,194,tag)
            elif tag.startswith("89"): isolator(m,xx,194,True,tag)
            else:
                circle(m,xx,194,3,"04_EQUIPAMENTOS")
                tc(m,tag,xx+7,194,0.95)
        ln(m,x+155,220,x+155,183,"05_POTENCIA")
        rect(m,x+145,176,x+165,185,"04_EQUIPAMENTOS")
        tc(m,"PORTAL",x+155,180,0.9,"04_EQUIPAMENTOS")
    poly(m,[(192,211),(208,211),(208,221),(226,221)],"08_CABOS")
    tc(m,"LINHA AEREA 30 km",210,216,1.25,"08_CABOS",TITLE_STYLE)
    tc(m,"OPGW - fibra / teleprotecao",210,202,1.0,"08_CABOS")
    table(m,51,148,[56,63,73,59],8.0,["INTERFACE","RESP. ESTUDO","DADO","SITUACAO"],[["Protecao de linha","ambas SE","teleprotecao","definir"],["Medicao","proprietario","TC/TP","especificar"],["Aterramento","civil/eletrica","solo + Icc","medir"]],1.0)
    tc(m,"Sem declaracao de atendimento aos requisitos de acesso ou do proprietario",210,110,1.1,"13_NOTAS")


def d25_01(m,p):
    circle(m,39,213,8,"05_POTENCIA")
    tc(m,"CALD.",39,214,1.4,"05_POTENCIA",TITLE_STYLE)
    tc(m,"biomassa",39,208,1.0)
    arrow(m,47,213,67,213)
    equip(m,67,199,56,28,"TV1","TURBINA","vapor / 3600 rpm")
    arrow(m,123,213,142,213)
    circle(m,153,213,11,"05_POTENCIA")
    tc(m,"G1",153,215,1.8,"05_POTENCIA",TITLE_STYLE)
    tc(m,"25 MW / 13,8 kV",153,207,0.95)
    arrow(m,164,213,188,213)
    breaker(m,199,213,"52G",False)
    ln(m,206,213,230,213)
    transformer(m,244,213,"T1","40 MVA")
    ln(m,247,208,247,188)
    ln(m,247,188,387,188,"05_POTENCIA",0.7)
    tc(m,"BARRA 138 kV / POI",326,193,1.4,"05_POTENCIA",TITLE_STYLE)
    breaker(m,340,188,"52L",True)
    ln(m,340,181,340,165)
    circle(m,340,158,7,"05_POTENCIA")
    tc(m,"REDE",340,159,1.2,"05_POTENCIA",TITLE_STYLE)
    for x,tag,detail in ((76,"QSA","2,2 MW"),(126,"AVR","campo"),(176,"GOV","turbina"),(286,"CB1","4 MVAr")):
        ln(m,x,188,x,162)
        breaker(m,x,154,"52-"+tag)
        equip(m,x-21,112,42,27,tag,tag,detail)
    # Reserve a clear band above the one-line power path; the previous location
    # touched the turbine/generator symbols at the table's lower edge.
    table(m,158,267,[45,43,47,45,45],8,["EQUIP.","S", "TENSAO", "CORRENTE", "DADO"],[["G1","32 MVA","13,8 kV","1.338 A","placa"],["T1","40 MVA","13,8/138","167 A AT","uk 12%*"],["Exportacao","22,8 MW","138 kV","100 A","fp ~0,95"]],0.95)


def d25_02(m,p):
    # A planta conserva geometria física em mm dentro de um bloco reutilizável;
    # a referência inserida na folha usa 1:500 (1 mm no papel = 500 mm no modelo).
    doc=m.doc
    block_name="P25_IMPLANTACAO_COGERACAO_MM"
    b=doc.blocks.new(name=block_name,base_point=(0,0))
    def bl(x1,y1,x2,y2,layer="11_ARQUITETURA",linetype=None):
        attrs={"layer":layer}
        if linetype: attrs["linetype"]=linetype
        b.add_line((x1,y1),(x2,y2),dxfattribs=attrs)
    def br(x1,y1,x2,y2,layer="04_EQUIPAMENTOS",linetype=None):
        pts=[(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
        attrs={"layer":layer,"closed":True}
        if linetype: attrs["linetype"]=linetype
        b.add_lwpolyline(pts,dxfattribs=attrs)
    def bt(text,x,y,height=1100,layer="02_TEXTO",rotation=0):
        entity=b.add_text(text,dxfattribs={"height":height,"layer":layer,"style":TEXT_STYLE,"rotation":rotation})
        entity.set_placement((x,y),align=TextEntityAlignment.MIDDLE_CENTER)
    def dh(x1,x2,y,base_y,label):
        bl(x1,base_y,x1,y,"03_COTAS"); bl(x2,base_y,x2,y,"03_COTAS"); bl(x1,y,x2,y,"03_COTAS")
        for x,sign in ((x1,1),(x2,-1)):
            bl(x,y,x+sign*900,y+350,"03_COTAS"); bl(x,y,x+sign*900,y-350,"03_COTAS")
        bt(label,(x1+x2)/2,y+900,1050,"03_COTAS")
    def dv(y1,y2,x,base_x,label):
        bl(base_x,y1,x,y1,"03_COTAS"); bl(base_x,y2,x,y2,"03_COTAS"); bl(x,y1,x,y2,"03_COTAS")
        for y,sign in ((y1,1),(y2,-1)):
            bl(x,y,x+350,y+sign*900,"03_COTAS"); bl(x,y,x-350,y+sign*900,"03_COTAS")
        bt(label,x-1100,(y1+y2)/2,1050,"03_COTAS",90)

    # Terreno sintético de 100 x 65 m; origem local declarada no canto sudoeste.
    br(0,0,100000,65000,"11_ARQUITETURA")
    bt("N",50000,62500,1500,"03_COTAS")
    bl(50000,58500,50000,61000,"03_COTAS")
    bl(50000,61000,49250,59500,"03_COTAS"); bl(50000,61000,50750,59500,"03_COTAS")
    bt("ACESSO / VIA INTERNA 6 m",50000,3500,1050,"11_ARQUITETURA")
    bl(0,6500,100000,6500,"11_ARQUITETURA","DASHED")

    # Envelope de armazenagem de biomassa e prédio da caldeira.
    br(8000,8000,33000,22000,"11_ARQUITETURA")
    bt("PATIO COBERTO DE BIOMASSA",20500,17500,1050)
    bt("25 x 14 m - envelope assumido",20500,12500,900,"02_TEXTO")
    br(8000,26000,33000,56000,"11_ARQUITETURA")
    bt("PREDIO DA CALDEIRA CB1",20500,52000,1100)
    br(13000,33000,28000,47000,"04_EQUIPAMENTOS")
    bt("CALDEIRA",20500,42000,1250,"04_EQUIPAMENTOS",90)
    br(10000,28500,13000,32500,"04_EQUIPAMENTOS")
    bt("ALIMENTADOR",11500,30500,750,"02_TEXTO",90)

    # Casa de máquinas: turbina, acoplamento, gerador e condensador em eixo comum.
    br(36000,14000,74000,46000,"11_ARQUITETURA")
    bt("CASA DE MAQUINAS - 38 x 32 m",55000,43500,1050,"11_ARQUITETURA")
    br(40000,27000,54000,35000,"04_EQUIPAMENTOS")
    bt("TV1 - TURBINA",47000,32500,1050,"04_EQUIPAMENTOS")
    bt("14 x 8 m",47000,29000,850,"02_TEXTO")
    br(56000,28000,69000,34000,"04_EQUIPAMENTOS")
    bt("G1 - GERADOR 25 MW",62500,32000,1050,"04_EQUIPAMENTOS")
    bt("13,8 kV / 32 MVA*",62500,29500,850,"02_TEXTO")
    bl(54000,31000,56000,31000,"11_ARQUITETURA")
    br(41000,16500,53000,23000,"04_EQUIPAMENTOS")
    bt("CONDENSADOR",47000,20000,850,"04_EQUIPAMENTOS")
    br(42000,37000,49000,42000,"04_EQUIPAMENTOS")
    bt("BOMBA DE ALIMENTACAO",45500,39500,700,"04_EQUIPAMENTOS")
    # Folga de manutenção ilustrada, sem valor normativo.
    br(38000,25000,71000,37000,"03_COTAS","DASHED")
    bt("AREA DE MANUTENCAO - HIPOTESE",54500,25800,700,"03_COTAS")

    # Equipamentos auxiliares, sala elétrica e pátio elevador fora da casa de máquinas.
    br(40000,50000,56000,61000,"11_ARQUITETURA")
    bt("AGUA / BOMBAS AUXILIARES",48000,57500,900)
    br(73000,46000,95000,61000,"11_ARQUITETURA")
    bt("SALA ELETRICA / QSA",84000,57500,1000)
    br(76500,48500,92000,55500,"04_EQUIPAMENTOS")
    bt("QSA / 2,2 MW (carga agregada)",84250,52000,800,"04_EQUIPAMENTOS")
    br(82000,25000,97000,40000,"11_ARQUITETURA")
    bt("PATIO T1 - 40 MVA",89500,37500,1000,"11_ARQUITETURA")
    br(84000,28500,95000,36500,"04_EQUIPAMENTOS")
    bt("T1 13,8/138 kV",89500,34000,850,"04_EQUIPAMENTOS")
    bt("11 x 8 m - envelope",89500,30500,750,"02_TEXTO")
    # Trincheira de potência G1-T1 e rota de controle para o QSA.
    poly(b,[(69000,31000),(76000,31000),(82000,32500),(84000,32500)],"08_CABOS")
    bt("ROTA DE CABOS CONCEITUAL PARA T1",80000,8800,850,"08_CABOS")
    poly(b,[(69000,29500),(74000,29500),(74000,50500),(76500,52000)],"06_COMANDO")
    bt("eletrocalha de controle",74500,41000,750,"06_COMANDO",90)
    # Ligação de vapor representada separadamente do circuito elétrico.
    poly(b,[(33000,43000),(36000,43000),(40000,35000)],"11_ARQUITETURA")

    dh(0,100000,-2500,0,"100 m - limite sintetico")
    dv(0,65000,103000,100000,"65 m - limite sintetico")
    dh(8000,33000,23500,22000,"25 m")
    dv(26000,56000,35000,33000,"30 m")
    dh(36000,74000,11500,14000,"38 m")
    dv(14000,46000,75500,74000,"32 m")
    dh(82000,97000,41500,40000,"15 m")
    bt("ORIGEM LOCAL (0,0) - canto sudoeste",12000,2500,850,"03_COTAS")
    m.add_blockref(block_name,(90,117),dxfattribs={"xscale":1/500,"yscale":1/500,"zscale":1})

    # Informações de projeto em espaço de folha; envelopes físicos permanecem no bloco em mm.
    rect(m,305,174,405,252,"12_LEGENDA")
    tc(m,"ENVELOPES DE ESTUDO",355,246,1.45,"12_LEGENDA",TITLE_STYLE)
    ln(m,307,241,403,241,"12_LEGENDA")
    rows=[("Terreno sintetico","100 x 65 m"),("Biomassa","25 x 14 m"),("Caldeira","25 x 30 m"),("Casa de maquinas","38 x 32 m"),("Sala eletrica","22 x 15 m"),("Pátio T1","15 x 15 m"),("G1","25 MW / 13,8 kV"),("T1","40 MVA / 138 kV")]
    for index,(label,value) in enumerate(rows):
        yy=235-index*7.2
        tc(m,label,327,yy,1.25,"02_TEXTO")
        tc(m,value,375,yy,1.25,"02_TEXTO")
        if index<len(rows)-1: ln(m,307,yy-3.2,403,yy-3.2,"12_LEGENDA")
    tc(m,"* placa de G1 assumida; dimensoes sem fabricante",355,179,0.95,"13_NOTAS")


def d25_03(m,p):
    panel(m,34,143,172,100,"GERADOR SINCRONO - CORTE AXIAL","eixo acoplado a turbina a vapor")
    ln(m,56,190,188,190,"04_EQUIPAMENTOS",1.0)
    rect(m,75,165,166,216,"04_EQUIPAMENTOS")
    poly(m,[(83,166),(91,176),(91,205),(83,215)],"04_EQUIPAMENTOS")
    poly(m,[(158,166),(150,176),(150,205),(158,215)],"04_EQUIPAMENTOS")
    rect(m,103,178,138,202,"05_POTENCIA")
    for i in range(7):
        ln(m,105+i*5,178,105+i*5,202,"05_POTENCIA")
    for x in (64,178):
        circle(m,x,190,5,"04_EQUIPAMENTOS")
    tc(m,"ESTATOR",120,209,1.0,"04_EQUIPAMENTOS")
    tc(m,"ROTOR 2P",120,184,1.0,"05_POTENCIA")
    rect(m,47,149,87,161,"04_EQUIPAMENTOS")
    tc(m,"EXCITATRIZ / AVR",67,155,0.95,"04_EQUIPAMENTOS")
    panel(m,225,143,158,100,"DADOS NOMINAIS","valores de referencia")
    table(m,237,222,[73,61],8,["PARAMETRO","VALOR"],[["Potencia ativa","25 MW"],["Potencia aparente","32 MVA"],["Tensao","13,8 kV"],["Frequencia","60 Hz"],["Rotacao sincrona","3600 rpm"],["Corrente de placa","1.338 A"]],1.0)
    tc(m,"Desenho nao representa carcaca ou ventilacao de fabricante",304,150,0.95,"13_NOTAS")


def d25_04(m,p):
    ln(m,40,217,155,217,"05_POTENCIA",0.7)
    tc(m,"BARRA 13,8 kV",95,222,1.4,"05_POTENCIA",TITLE_STYLE)
    breaker(m,82,217,"52G",False)
    for y in (208,217,226):
        circle(m,121,y,1.3,"07_INSTRUMENTACAO")
    tc(m,"TCs 3x",126,232,1.0,"07_INSTRUMENTACAO")
    ln(m,155,217,177,217)
    transformer(m,190,217,"T1","40 MVA")
    ln(m,193,212,193,194)
    ln(m,193,194,366,194,"05_POTENCIA",0.7)
    breaker(m,315,194,"52L",True)
    ln(m,315,187,315,171)
    circle(m,315,164,6,"05_POTENCIA")
    tc(m,"REDE",315,165,1.1,"05_POTENCIA",TITLE_STYLE)
    equip(m,215,148,52,29,"LA","PARA-RAIOS","138 kV")
    ln(m,241,177,241,194,"05_POTENCIA")
    ground(m,241,148)
    equip(m,120,148,58,29,"52G","DISJUNTOR","13,8 kV")
    table(m,40,267,[47,45,44,45,47],8,["ITEM","S","LADO 13,8","LADO 138","uk*"],[["T1","40 MVA","13,8 kV","138 kV","12%"],["In","-","1,673 kA","167 A","-"],["Ramo","13,8 kV","TC/TP","138 kV","-+"]],0.95)
    tc(m,"TCs e TPs: relacao/precisao a definir; uk assumido para estudos",288,139,0.9,"13_NOTAS")


def d25_05(m,p):
    # Excitation power circuit
    circle(m,55,213,8,"05_POTENCIA")
    tc(m,"G1",55,214,1.6,"05_POTENCIA",TITLE_STYLE)
    ln(m,63,213,90,213,"05_POTENCIA")
    rect(m,90,202,129,224,"04_EQUIPAMENTOS")
    tc(m,"EXCITATRIZ",109,215,1.2,"04_EQUIPAMENTOS",TITLE_STYLE)
    ln(m,129,213,153,213,"05_POTENCIA")
    rect(m,153,202,195,224,"05_POTENCIA")
    tc(m,"PONTE",174,216,1.2,"05_POTENCIA",TITLE_STYLE)
    tc(m,"RETIFICADORA",174,208,0.95)
    ln(m,195,213,224,213,"05_POTENCIA")
    rect(m,224,205,262,221,"05_POTENCIA")
    tc(m,"CAMPO F+ F-",243,213,1.15,"05_POTENCIA",TITLE_STYLE)
    poly(m,[(262,213),(282,213),(282,196),(55,196),(55,204)],"05_POTENCIA")
    tc(m,"realimentacao de corrente de campo",166,190,1.0,"07_INSTRUMENTACAO")
    # AVR feedback loop
    rect(m,57,125,119,159,"07_INSTRUMENTACAO")
    tc(m,"TP / TC",88,147,1.3,"07_INSTRUMENTACAO",TITLE_STYLE)
    tc(m,"medicao V, I",88,136,1.0)
    rect(m,152,121,238,162,"06_COMANDO")
    tc(m,"AVR / PID",195,151,1.4,"06_COMANDO",TITLE_STYLE)
    tc(m,"limitadores OEL / UEL",195,140,1.0)
    tc(m,"Vref - Vt",195,129,1.0)
    arrow(m,119,142,152,142,"07_INSTRUMENTACAO")
    arrow(m,238,142,275,142,"06_COMANDO")
    rect(m,275,128,360,158,"06_COMANDO")
    tc(m,"Efd / excitacao",317,146,1.25,"06_COMANDO",TITLE_STYLE)
    arrow(m,317,158,317,183,"06_COMANDO")
    ln(m,317,183,174,183,"06_COMANDO")
    ln(m,174,183,174,202,"06_COMANDO")
    table(m,264,244,[38,48,51],8,["BLOCO","MODELO","ESTADO"],[["AVR","1a ordem","conceitual"],["Excitatriz","ganho efetivo","nao selecionada"],["Limitadores","OEL/UEL","sem ajuste"]],0.95)


def d25_06(m,p):
    rect(m,43,207,105,233,"07_INSTRUMENTACAO")
    tc(m,"SENSOR ω",74,223,1.3,"07_INSTRUMENTACAO",TITLE_STYLE)
    rect(m,133,207,202,233,"06_COMANDO")
    tc(m,"GOV / DROOP",167,223,1.3,"06_COMANDO",TITLE_STYLE)
    rect(m,232,207,292,233,"06_COMANDO")
    tc(m,"SERVO",262,223,1.3,"06_COMANDO",TITLE_STYLE)
    rect(m,323,207,378,233,"04_EQUIPAMENTOS")
    tc(m,"VALVULA",350,223,1.3,"04_EQUIPAMENTOS",TITLE_STYLE)
    arrow(m,105,220,133,220,"07_INSTRUMENTACAO")
    arrow(m,202,220,232,220,"06_COMANDO")
    arrow(m,292,220,323,220,"06_COMANDO")
    equip(m,269,158,82,31,"TV1","TURBINA","Pm -> eixo")
    arrow(m,350,207,350,189,"05_POTENCIA")
    arrow(m,269,173,111,173,"07_INSTRUMENTACAO")
    arrow(m,111,173,74,207,"07_INSTRUMENTACAO")
    table(m,215,157,[40,40,77],7.5,["SINAL","VALOR","NOTA"],[["f","60 Hz","referencia nominal"],["Pm","25,38 MW","governador"],["droop","5%","premissa"],["Tgov","0,5 s","1a ordem"]],0.9)
    panel(m,44,119,162,38,"LIMITES FUNCIONAIS","caldeira, vapor e atuadores fora do modelo")


def d25_07(m,p):
    circle(m,56,209,8,"05_POTENCIA")
    tc(m,"G1",56,210,1.4,"05_POTENCIA",TITLE_STYLE)
    circle(m,364,209,8,"05_POTENCIA")
    tc(m,"REDE",364,210,1.2,"05_POTENCIA",TITLE_STYLE)
    for x in (76,121,166,211,256,301,340):
        ln(m,x,209,x+20,209,"05_POTENCIA")
    for x,tag in ((92,"52G"),(137,"89G"),(182,"TC/TP"),(227,"25"),(272,"52L"),(317,"89L")):
        if tag.startswith("52"): breaker(m,x,209,tag,False)
        elif tag.startswith("89"): isolator(m,x,209,False,tag)
        else:
            circle(m,x,209,3,"07_INSTRUMENTACAO")
            tc(m,tag,x,201,1.0,"07_INSTRUMENTACAO")
    panel(m,46,142,155,38,"CONDICOES","V, f, sequencia de fases")
    panel(m,215,142,155,38,"PERMISSIVOS","25 OK, 86 reset, protecoes OK")
    rect(m,130,108,286,129,"06_COMANDO")
    tc(m,"SINCRONIZADOR + RELE 25",208,121,1.3,"06_COMANDO",TITLE_STYLE)
    tc(m,"ΔV, Δf, Δφ dentro de janela configurada",208,113,1.0)
    arrow(m,122,180,164,129,"07_INSTRUMENTACAO")
    arrow(m,294,180,252,129,"06_COMANDO")
    arrow(m,286,118,317,209,"06_COMANDO")
    table(m,52,244,[51,48,55,63],8,["VARIAVEL","MEDICAO","LOGICA","FECHAMENTO"],[["Tensao","TP G1/POI","comparar","permitir"],["Frequencia","81/medidor","comparar","permitir"],["Angulo","25","janela","pulso 52"],["Trip","86","bloqueia","nao fechar"]],0.95)
    tc(m,"A janela e o tempo de compensacao dependem do fabricante e do operador",210,106,1.05,"13_NOTAS")


def d25_08(m,p):
    circle(m,50,211,8,"05_POTENCIA")
    tc(m,"G1",50,212,1.4,"05_POTENCIA",TITLE_STYLE)
    ln(m,58,211,140,211,"05_POTENCIA",0.7)
    ln(m,140,211,210,211,"05_POTENCIA",0.7)
    breaker(m,210,211,"52G")
    ln(m,210,204,210,186,"05_POTENCIA")
    transformer(m,210,175,"T1","13,8/138 kV")
    ln(m,213,170,213,157)
    ln(m,213,157,362,157,"05_POTENCIA",0.7)
    tc(m,"ZONA T1 / POI",305,162,1.2,"05_POTENCIA",TITLE_STYLE)
    for x,code in ((75,"87G"),(110,"64G"),(150,"40/32"),(180,"46/49")):
        circle(m,x,225,8,"07_INSTRUMENTACAO")
        tc(m,code,x,225,1.0,"07_INSTRUMENTACAO",TITLE_STYLE)
        ln(m,x,217,x,219,"07_INSTRUMENTACAO")
    for x,code in ((245,"87T"),(280,"50/51"),(320,"27/59"),(350,"81")):
        circle(m,x,172,8,"07_INSTRUMENTACAO")
        tc(m,code,x,172,1.0,"07_INSTRUMENTACAO",TITLE_STYLE)
        ln(m,x,164,x,157,"07_INSTRUMENTACAO")
    rect(m,67,119,361,145,"06_COMANDO")
    tc(m,"IED G1 / PROTECAO DE TRANSFORMADOR / 86G",214,136,1.4,"06_COMANDO",TITLE_STYLE)
    tc(m,"Saidas: abre 52G, bloqueia excitacao conforme filosofia e sinaliza eventos",214,126,1.05)
    for x in (95,165):
        ln(m,x,211,x,145,"07_INSTRUMENTACAO")
        circle(m,x,211,2.3,"07_INSTRUMENTACAO")
    for x in (260,332):
        ln(m,x,157,x,145,"07_INSTRUMENTACAO")
        circle(m,x,157,2.3,"07_INSTRUMENTACAO")
    table(m,48,267,[42,48,48,52,46],6.0,["ANSI","FUNCAO","MEDICAO","ACAO","AJUSTE"],[["87G","diferencial","TCs estator","trip","pendente"],["64G","terra estator","neutro","alarme/trip","pendente"],["40","perda campo","V/I","trip","pendente"],["32","potencia reversa","P","trip","pendente"]],0.82)
    tc(m,"Lista funcional nao constitui coordenacao de protecao",211,106,1.0,"13_NOTAS")


def d25_09(m,p):
    ln(m,42,220,380,220,"05_POTENCIA",0.7)
    tc(m,"BARRA 480 Vca - SERVICOS AUXILIARES",210,226,1.4,"05_POTENCIA",TITLE_STYLE)
    ln(m,90,220,90,202)
    breaker(m,90,194,"52-QSA")
    ln(m,90,187,90,175)
    rect(m,55,148,126,175,"04_EQUIPAMENTOS")
    tc(m,"QSA-1",90,163,1.4,"04_EQUIPAMENTOS",TITLE_STYLE)
    tc(m,"secao A",90,154,1.0)
    for x,tag,detail in ((150,"M1","bomba"),(202,"M2","ventilador"),(254,"M3","esteira"),(306,"UPS","controle"),(358,"QDC","iluminacao")):
        ln(m,x,220,x,205)
        breaker(m,x,197,"52-"+tag)
        ln(m,x,190,x,179)
        circle(m,x,170,6,"04_EQUIPAMENTOS")
        tc(m,"M" if tag.startswith("M") else tag,x,170,1.1,"04_EQUIPAMENTOS",TITLE_STYLE)
        tc(m,detail,x,159,1.0)
    rect(m,52,113,132,135,"04_EQUIPAMENTOS")
    tc(m,"QDC 220/127 V",92,123,1.15,"04_EQUIPAMENTOS",TITLE_STYLE)
    rect(m,166,113,248,135,"UPS")
    tc(m,"UPS / BATERIA CC",207,123,1.15,"04_EQUIPAMENTOS",TITLE_STYLE)
    arrow(m,90,148,90,135,"05_POTENCIA")
    arrow(m,207,148,207,135,"06_COMANDO")
    table(m,255,144,[54,51,46],8,["CARGA","P (MW)","fp"],[["Auxiliar total","2,20","0,90"],["Motor M1","0,55","0,88"],["Motor M2","0,45","0,90"],["Esteiras","0,35","0,88"],["Outros/UPS","0,85","0,92"]],0.9)
    tc(m,"Distribuicao conceitual; tensoes auxiliares e cargas devem ser confirmadas",211,107,1.0,"13_NOTAS")


def d25_10(m,p):
    rect(m,38,142,263,243,"11_ARQUITETURA")
    tc(m,"MALHA DE TERRA - CASA DE MAQUINAS E PATIO",150,236,1.4,"11_ARQUITETURA",TITLE_STYLE)
    for x in range(56,252,18):
        if 78 <= x <= 130 or 168 <= x <= 230:
            ln(m,x,152,x,176,"08_CABOS",0.35)
            ln(m,x,205,x,224,"08_CABOS",0.35)
        else:
            ln(m,x,152,x,224,"08_CABOS",0.35)
    for y in (152,168,176,208,216,224): ln(m,56,y,251,y,"08_CABOS",0.35)
    for y in (184,200):
        for x1,x2 in ((56,78),(130,168),(230,251)): ln(m,x1,y,x2,y,"08_CABOS",0.35)
    equip(m,78,177,52,27,"G1","GERADOR","neutro e carcaça")
    equip(m,168,177,62,27,"T1","TRANSFORMADOR","tanque / neutro")
    for x,y in ((78,177),(130,177),(168,177),(230,177),(56,128),(251,128),(56,224),(251,224)):
        circle(m,x,y,2.2,"07_INSTRUMENTACAO")
    ln(m,104,177,104,153,"08_CABOS")
    ln(m,199,177,199,153,"08_CABOS")
    ln(m,104,153,199,153,"08_CABOS")
    tc(m,"BEP - BARRA EQUIPOTENCIAL",151,147,1.0,"08_CABOS")
    panel(m,278,175,105,59,"LIGACOES","gerador / neutro / trafo / trilhos")
    panel(m,278,118,105,44,"ESTUDOS EM ABERTO","solo / Icc / toque / passo")
    table(m,46,136,[50,53,52,50],7.5,["ITEM","PONTO","FUNCAO","STATUS"],[["N-G","G1","neutro","definir"],["T1","tanque","PE","ligar"],["M1","carcaça","PE","ligar"]],0.9)
    tc(m,"malha indicativa",151,138,0.95,"08_CABOS")
    tc(m,"Compatibilizar com aterramento de alta tensao e SPDA",330,108,0.95,"13_NOTAS")


DRAW: dict[str, list[Callable]] = {
    "p23": [d23_01,d23_02,d23_03,d23_04,d23_05,d23_06,d23_07,d23_08,d23_09,d23_10],
    "p24": [d24_01,d24_02,d24_03,lambda m,p:draw_tower(m,p,False),lambda m,p:draw_tower(m,p,True),d24_06,d24_07,d24_08,d24_09,d24_10],
    "p25": [d25_01,d25_02,d25_03,d25_04,d25_05,d25_06,d25_07,d25_08,d25_09,d25_10],
}

SLUGS = {
    "p23": "23-complexo-siderurgico-eaf",
    "p24": "24-linha-transmissao-138kv",
    "p25": "25-usina-cogeracao-biomassa",
}


UNITS = {
    "frequency_hz":"Hz", "grid_voltage_kv":"kV", "bus_voltage_kv":"kV", "furnace_secondary_voltage_kv":"kV",
    "source_short_circuit_mva":"MVA", "main_transformer_mva":"MVA", "main_transformer_x_pu":"pu", "main_transformer_r_pu":"pu",
    "furnace_transformer_mva":"MVA", "furnace_transformer_x_pu":"pu", "furnace_transformer_r_pu":"pu", "furnace_power_factor":"pu",
    "auxiliary_active_mw":"MW", "auxiliary_power_factor":"pu", "target_power_factor":"pu", "statcom_limit_mvar":"MVAr",
    "filter_total_mvar":"MVAr", "filter_5th_mvar":"MVAr", "filter_7th_mvar":"MVAr", "filter_highpass_mvar":"MVAr",
    "filter_damping_ohm":"ohm", "bus_voltage_time_constant_s":"s", "statcom_time_constant_s":"s", "arc_fluctuation_pu":"pu",
    "voltage_kv":"kV", "length_km":"km", "span_m":"m", "span_count":"adimensional", "conductor_r20_ohm_km":"ohm/km",
    "conductor_rac75_ohm_km":"ohm/km", "conductor_diameter_m":"m", "conductor_gmr_m":"m", "conductor_mass_kg_m":"kg/m", "conductor_ea_n":"N", "conductor_alpha_per_c":"1/K",
    "conductor_rated_tensile_n":"N", "reference_temperature_c":"°C", "reference_horizontal_tension_n":"N", "resistance_alpha_per_c":"1/K",
    "bundle_subconductors":"adimensional", "bundle_spacing_m":"m", "conductor_temperature_limit_c":"°C",
    "mean_conductor_height_m":"m", "shield_wire_height_m":"m", "tower_height_m":"m", "design_ground_clearance_m":"m", "rated_current_a":"A",
    "wind_speeds_m_s":"m/s", "mechanical_wind_speeds_m_s":"m/s", "ambient_temperatures_c":"°C", "mechanical_conductor_temperatures_c":"°C",
    "thermal_h_w_m2_c":"W/m2/K", "thermal_natural_h_w_m2_c":"W/m2/K", "thermal_reference_wind_m_s":"m/s",
    "solar_flux_w_m2":"W/m2", "air_density_kg_m3":"kg/m3", "drag_coefficient":"adimensional",
    "solar_absorptivity":"pu", "ground_resistivity_ohm_m":"ohm.m", "ground_rod_length_m":"m", "ground_rod_diameter_m":"m",
    "phase_spacing_m":"m", "route_km":"km", "route_elevation_m":"m", "route_bearing_deg":"°", "anchor_stations_km":"km",
    "load_active_mw":"MW", "load_power_factor":"pu",
    "generator_active_mw":"MW", "generator_rating_mva":"MVA", "generator_power_factor":"pu", "generator_voltage_kv":"kV",
    "generator_efficiency":"pu", "grid_short_circuit_mva":"MVA", "power_factor_target":"pu", "capacitor_bank_mvar":"MVAr",
    "process_steam_thermal_mw":"MWth", "biomass_flow_t_h":"t/h", "biomass_lhv_mj_kg":"MJ/kg", "boiler_efficiency":"pu",
    "annual_operating_hours":"h", "pole_count":"poles", "inertia_constant_s":"s", "damping_pu":"pu", "governor_droop_pu":"pu",
    "governor_time_constant_s":"s", "avr_gain":"pu", "avr_time_constant_s":"s", "generator_transient_reactance_pu":"pu",
    "fault_voltage_pu":"pu", "fault_duration_s":"s",
}


def flatten(prefix: str, value, out: list[tuple[str, str]]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            flatten(f"{prefix}_{k}" if prefix else k, v, out)
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value, start=1):
            flatten(f"{prefix}_{i}", v, out)
    else:
        out.append((prefix, str(value)))


def write_parameters(path: Path, params: dict) -> None:
    rows: list[tuple[str,str]]=[]
    flatten("",params,rows)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.writer(stream,lineterminator="\n")
        writer.writerow(("name","value","unit","source"))
        for name,value in rows:
            base=re.sub(r"_\d+$","",name)
            writer.writerow((name,value,UNITS.get(base,"-"),"portfolio.toml: project_parameters"))


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--project",choices=("all","p23","p24","p25"),default="all")
    parser.add_argument("--no-render",action="store_true")
    args=parser.parse_args()
    root=args.root.resolve()
    config=load_config(root)
    selected=("p23","p24","p25") if args.project=="all" else (args.project,)
    updated=[]
    for key in selected:
        params=config["project_parameters"][key]
        slug=SLUGS[key]
        base=root/slug
        for dirname in ("fonte","exports","dados","matlab/parametros","matlab/calculos","matlab/funcoes","matlab/testes","simulink","resultados/graficos","resultados/tabelas","resultados/relatorios","validacao"):
            (base/dirname).mkdir(parents=True,exist_ok=True)
        write_parameters(base/"dados"/"parametros.csv",params)
        numbers=range(1,11)
        for number in numbers:
            spec=SHEETS[key][number-1]
            filename=f"{number:02d}_{spec[0].split('_',1)[1]}.dxf"
            title,subtitle,notes,legend=spec[1:]
            project_title={"p23":"Complexo siderurgico - EAF","p24":"Linha de transmissao 138 kV","p25":"Usina de cogeneracao a biomassa"}[key]
            project_meta=next(p for p in config["projects"] if p["path"]==slug)
            sheet_scale="1:500" if key=="p25" and number==2 else "S/ESC."
            doc,layout=add_sheet_frame(root,config,project_meta["id"],project_title,number,filename,title,subtitle,notes,legend,sheet_scale)
            DRAW[key][number-1](layout,params)
            prepare_deterministic_write(doc)
            source=base/"fonte"/filename
            doc.saveas(source)
            relative=source.relative_to(root).as_posix()
            artifact=next(a for a in config["artifacts"] if a["source"]==relative)
            updated.append(artifact)
            if not args.no_render:
                render_config={**config,"portfolio":{**config["portfolio"],"template_date":DATE}}
                outputs={kind:root/artifact[kind] for kind in ("svg","pdf","png")}
                render_document(source,outputs,(0.0,0.0,float(config["page"]["width"]),float(config["page"]["height"])),render_config,300,artifact)
        # Project-local deterministic report inputs are generated from central parameters.
        print(f"{slug}: 10 DXFs gerados" + (" e renderizados" if not args.no_render else ""))
    if not args.no_render:
        manifest_path=root/"renders"/"manifesto.json"
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["generated_on"]=DATE
        by_id={a["id"]:a for a in manifest.get("artifacts",[])}
        for artifact in updated:
            source=root/artifact["source"]
            by_id[artifact["id"]]={
                "id":artifact["id"],
                "source":artifact["source"],
                "source_sha256":sha256(source),
                "outputs":{
                    kind:{"path":artifact[kind],"sha256":sha256(root/artifact[kind])}
                    for kind in ("pdf","png","svg")
                },
            }
        manifest["artifacts"]=[by_id[key] for key in sorted(by_id)]
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    return 0


def sha256(path: Path) -> str:
    import hashlib
    digest=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__=="__main__":
    raise SystemExit(main())
