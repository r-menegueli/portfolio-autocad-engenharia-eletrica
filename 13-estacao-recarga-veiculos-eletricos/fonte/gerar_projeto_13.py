"""Gera as tres pranchas conceituais da estacao de recarga P13."""

from __future__ import annotations

import argparse
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


SLUG = "13-estacao-recarga-veiculos-eletricos"
DATE = "2026-11-06"
REVISION = "00"
WARNING_FALLBACK = (
    "Projeto academico e conceitual. Nao deve ser utilizado para fabricacao, "
    "instalacao ou execucao de servicos sem revisao, dimensionamento e "
    "responsabilidade de profissional legalmente habilitado."
)


def text(layout, value: str, x: float, y: float, h: float = 1.7,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(
        layout,
        value,
        (x, y),
        h,
        layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
        style=TITLE_STYLE if bold else TEXT_STYLE,
    )


def line(layout, a: tuple[float, float], b: tuple[float, float],
         layer: str = "02_TEXTO") -> None:
    add_line(layout, a, b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float,
        title: str, detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        detail_height: float = 1.3) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    midx = (x0 + x1) / 2
    midy = (y0 + y1) / 2
    if detail:
        if "\n" in detail:
            text(layout, title, midx, y1 - 5, 1.7, layer, centered=True, bold=True)
            add_mtext(
                layout,
                detail.replace("\n", "\\P"),
                (x0 + 2, y1 - 8),
                x1 - x0 - 4,
                detail_height,
                "02_TEXTO",
            )
        else:
            text(layout, title, midx, midy + 2, 1.7, layer, centered=True, bold=True)
            text(layout, detail, midx, midy - 2, detail_height, "02_TEXTO", centered=True)
    else:
        text(layout, title, midx, midy, 1.7, layer, centered=True, bold=True)


def arrow(layout, start: tuple[float, float], end: tuple[float, float],
          layer: str, size: float = 2.3) -> None:
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(
            layout,
            (end[0] - ux * size + side * px * size * 0.55,
             end[1] - uy * size + side * py * size * 0.55),
            end,
            layer,
        )


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 3.2, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.65, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66.5, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.42, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90.5, 2.0, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.38, "12_LEGENDA")

    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, value, x, 89.5, 1.55, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.45, "02_TEXTO", centered=True)


def make_sheet(config: dict, number: int, spec: dict, draw) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    draw(layout)
    warning = config["portfolio"].get("warning", WARNING_FALLBACK)
    footer(layout, spec, warning)
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(
        {
            "TITULO": spec["title"],
            "AUTOR": config["portfolio"]["author"],
            "DATA": DATE,
            "REVISAO": REVISION,
            "PRANCHA": f"{number:02d}/03",
            "ARQUIVO": spec["filename"],
            "UNIDADES": "mm",
            "ESCALA": spec["scale"],
            "FOLHA": "A3",
            "STATUS": "CONCEIT.",
        }
    )
    output = PROJECT_DIR / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def draw_site(layout) -> None:
    # Limite e vagas esquematicos; apenas as dimensoes nominais das vagas estao anotadas.
    add_rect(layout, 34, 105, 266, 258, "11_ARQUITETURA")
    text(layout, "LIMITE CONCEITUAL DA AREA", 39, 252, 1.55, "11_ARQUITETURA", bold=True)

    # Duas fileiras com tres vagas. A representacao nao substitui levantamento local.
    xs = (64, 94, 124)
    for row_y, labels in ((207, ("V01 AC-01", "V02 AC-02", "V03 DC-05")),
                           (112, ("V04 AC-03", "V05 AC-04", "V06 DC-06"))):
        for x, label in zip(xs, labels):
            add_rect(layout, x, row_y, x + 30, row_y + 45, "11_ARQUITETURA")
            text(layout, label, x + 15, row_y + 39, 1.45, "11_ARQUITETURA", centered=True, bold=True)
            # Veiculo em planta simplificada, sem dimensao de homologacao.
            add_rect(layout, x + 8, row_y + 8, x + 22, row_y + 34, "11_ARQUITETURA")
            line(layout, (x + 9.5, row_y + 11), (x + 20.5, row_y + 11), "03_COTAS")
            line(layout, (x + 9.5, row_y + 31), (x + 20.5, row_y + 31), "03_COTAS")

    # Simbolos EVSE, distribuidos por tipo e identificacao dos circuitos.
    for x, y, tag in (
        (60, 246, "AC"), (90, 246, "AC"), (120, 246, "DC"),
        (60, 116, "AC"), (90, 116, "AC"), (120, 116, "DC"),
    ):
        add_rect(layout, x - 2.0, y - 1.8, x + 2.0, y + 1.8, "04_EQUIPAMENTOS")
        text(layout, tag, x, y, 0.95, "04_EQUIPAMENTOS", centered=True, bold=True)

    # Faixa esquematica de circulacao, sentidos e rota de infraestrutura.
    add_rect(layout, 49, 157, 164, 202, "11_ARQUITETURA")
    for y in (169, 180, 191):
        arrow(layout, (58, y), (155, y), "03_COTAS", 2.0)
    text(layout, "CIRCULACAO - SENTIDO INDICATIVO", 106, 160, 1.35, "11_ARQUITETURA", centered=True)
    line(layout, (169, 117), (169, 249), "10_ELETROCALHAS")
    line(layout, (169, 249), (184, 249), "10_ELETROCALHAS")
    line(layout, (169, 117), (184, 117), "10_ELETROCALHAS")
    text(layout, "ROTA: A DEFINIR", 172, 198, 1.2, "10_ELETROCALHAS")

    box(layout, 190, 212, 252, 240, "QEV-01", "quadro EV\nlocal a confirmar", detail_height=1.3)
    box(layout, 190, 164, 252, 192, "EMS-01", "gestao de carga\ninterface OEM", detail_height=1.3)
    arrow(layout, (221, 211), (221, 195), "05_POTENCIA")
    arrow(layout, (221, 163), (221, 149), "07_INSTRUMENTACAO")
    text(layout, "Acesso tecnico e afastamentos: confirmar em campo e com OEM.", 178, 136, 1.25, "13_NOTAS")

    add_rect(layout, 276, 117, 400, 258, "12_LEGENDA")
    text(layout, "CADASTRO DE POSICOES", 281, 250, 2.1, "12_LEGENDA", bold=True)
    line(layout, (280, 245), (396, 245), "12_LEGENDA")
    rows = (
        ("V01-V02", "EVSE-01/02", "AC 11 kW cada"),
        ("V04-V05", "EVSE-03/04", "AC 11 kW cada"),
        ("V03", "EVSE-05", "DC 60 kW"),
        ("V06", "EVSE-06", "DC 60 kW"),
    )
    y = 235
    for vaga, equipamento, potencia in rows:
        text(layout, f"{vaga}  |  {equipamento}", 281, y, 1.4, "02_TEXTO", bold=True)
        text(layout, potencia, 283, y - 4.2, 1.35, "02_TEXTO")
        y -= 13
    add_rect(layout, 280, 124, 396, 168, "13_NOTAS")
    text(layout, "PREMISSAS GEOMETRICAS", 284, 161, 1.8, "13_NOTAS", bold=True)
    add_mtext(
        layout,
        "Vagas representadas com envelope indicativo de 2,5 x 5,0 m.\\P"
        "Limite, acessos, circulacao, sinalizacao, drenagem, protecao contra impacto,\\P"
        "acessibilidade e afastamentos requerem levantamento e verificacao local.",
        (284, 155), 107, 1.42, "13_NOTAS",
    )


def draw_single_line(layout) -> None:
    box(layout, 27, 207, 89, 237, "REDE BT", "tensao / curto-circuito\nregime de aterramento", detail_height=1.35)
    box(layout, 113, 207, 175, 237, "MEDICAO", "fronteira / medidor\ndados da concessionaria", detail_height=1.35)
    box(layout, 199, 207, 270, 237, "QGBT EXISTENTE", "capacidade / reserva\ndados ainda pendentes", detail_height=1.35)
    box(layout, 293, 202, 382, 242, "QEV-01", "seccionamento e protecao\nselecionar apos estudos", detail_height=1.4)
    arrow(layout, (89, 222), (113, 222), "05_POTENCIA")
    arrow(layout, (175, 222), (199, 222), "05_POTENCIA")
    arrow(layout, (270, 222), (293, 222), "05_POTENCIA")
    text(layout, "380/220 V, 3F+N+PE, 60 Hz: hipotese de estudo, nao dado de concessionaria.", 27, 195, 1.42, "13_NOTAS")

    # Barramento conceitual e seis alimentadores individualizados, sem especificar protecao.
    line(layout, (36, 178), (388, 178), "05_POTENCIA")
    text(layout, "BARRAMENTO QEV - dimensionamento e curto-circuito pendentes", 212, 183, 1.4, "05_POTENCIA", centered=True, bold=True)
    # A descida de potencia passa pelo lado de fora da caixa de comunicacao.
    line(layout, (382, 222), (390, 222), "05_POTENCIA")
    arrow(layout, (390, 222), (390, 178), "05_POTENCIA")
    centers = (53, 117, 181, 245, 309, 373)
    tags = ("EVSE-01", "EVSE-02", "EVSE-03", "EVSE-04", "EVSE-05", "EVSE-06")
    powers = ("AC 11 kW", "AC 11 kW", "AC 11 kW", "AC 11 kW", "DC 60 kW", "DC 60 kW")
    for idx, (cx, tag, power) in enumerate(zip(centers, tags, powers), 1):
        line(layout, (cx, 178), (cx, 166), "05_POTENCIA")
        text(layout, f"QF-{idx:02d}*", cx, 162, 1.25, "05_POTENCIA", centered=True)
        line(layout, (cx, 158), (cx, 151), "05_POTENCIA")
        box(layout, cx - 23, 124, cx + 23, 151, tag, power, detail_height=1.35)
        line(layout, (cx, 124), (cx, 113), "05_POTENCIA")
        line(layout, (cx - 4, 113), (cx + 4, 113), "05_POTENCIA")
        line(layout, (cx - 2.7, 110.5), (cx + 2.7, 110.5), "05_POTENCIA")
    # Caminho de dados mantido separado da potencia.
    box(layout, 305, 188, 369, 199, "EMS-01", "medicao de entrada / controle", layer="07_INSTRUMENTACAO", detail_height=1.15)
    line(layout, (369, 193.5), (398, 193.5), "07_INSTRUMENTACAO")
    line(layout, (398, 193.5), (398, 119), "07_INSTRUMENTACAO")
    line(layout, (76, 119), (398, 119), "07_INSTRUMENTACAO")
    for cx in centers:
        arrow(layout, (cx + 23, 119), (cx + 23, 124), "07_INSTRUMENTACAO", 1.4)


def draw_management(layout) -> None:
    # Lado esquerdo: dados de entrada e estado dos pontos.
    add_rect(layout, 24, 151, 134, 255, "07_INSTRUMENTACAO")
    text(layout, "ENTRADAS DO EMS", 29, 247, 2.0, "07_INSTRUMENTACAO", bold=True)
    line(layout, (28, 242), (130, 242), "07_INSTRUMENTACAO")
    inputs = (
        "P01  potencia ativa da entrada (medidor)",
        "P02  limite de importacao contratado",
        "P03  demanda das cargas do edificio",
        "P04  estado / disponibilidade de EVSE",
        "P05  limite operacional definido pelo operador",
    )
    for i, item in enumerate(inputs):
        y = 232 - i * 11
        add_rect(layout, 30, y - 3, 128, y + 4, "12_LEGENDA")
        text(layout, item, 33, y + 0.5, 1.25, "02_TEXTO")
    box(layout, 35, 162, 123, 181, "QUALIDADE DE DADOS", "validade / idade / falha\nacao segura pendente", layer="13_NOTAS", detail_height=1.3)

    # Centro: fluxo de limitacao e comando aos seis carregadores.
    box(layout, 166, 216, 251, 252, "EMS-01", "supervisao e alocacao\nalgoritmo sujeito a revisao", layer="07_INSTRUMENTACAO", detail_height=1.4)
    box(layout, 166, 179, 251, 205, "REGRA DE POTENCIA", "Pdisp = limite - cargas nao EV", layer="13_NOTAS", detail_height=1.4)
    arrow(layout, (134, 202), (166, 231), "07_INSTRUMENTACAO")
    arrow(layout, (208, 216), (208, 205), "07_INSTRUMENTACAO")
    box(layout, 166, 145, 251, 167, "ALOCA / LIMITA", "prioridade e rampas a definir", layer="06_COMANDO", detail_height=1.3)
    arrow(layout, (208, 179), (208, 167), "06_COMANDO")
    add_rect(layout, 145, 101, 265, 138, "04_EQUIPAMENTOS")
    text(layout, "LIMITES SOLICITADOS POR PONTO", 205, 132.5, 1.55, "04_EQUIPAMENTOS", centered=True, bold=True)
    line(layout, (148, 128), (262, 128), "03_COTAS")
    text(layout, "EVSE", 158, 125, 1.05, "12_LEGENDA", centered=True, bold=True)
    text(layout, "TIPO", 207, 125, 1.05, "12_LEGENDA", centered=True, bold=True)
    text(layout, "kW*", 251, 125, 1.05, "12_LEGENDA", centered=True, bold=True)
    commands = (("01", "AC", "11"), ("02", "AC", "11"), ("03", "AC", "11"),
                ("04", "AC", "11"), ("05", "DC", "60"), ("06", "DC", "60"))
    for i, row in enumerate(commands):
        y = 121 - i * 3.1
        text(layout, row[0], 158, y, 1.0, "02_TEXTO", centered=True)
        text(layout, row[1], 207, y, 1.0, "02_TEXTO", centered=True)
        text(layout, row[2], 251, y, 1.0, "02_TEXTO", centered=True)
    arrow(layout, (208, 145), (208, 138), "06_COMANDO", 1.6)

    # Lado direito: passos de operacao.
    add_rect(layout, 278, 184, 398, 255, "12_LEGENDA")
    text(layout, "SEQUENCIA FUNCIONAL", 283, 247, 2.0, "12_LEGENDA", bold=True)
    steps = (
        "1  Validar medidor, comunicacao e limites.",
        "2  Atualizar demanda nao EV e margem disponivel.",
        "3  Distribuir potencia entre sessoes autorizadas.",
        "4  Aplicar limites aceitos por cada carregador.",
        "5  Registrar medicao, comando, retorno e alarme.",
    )
    for i, item in enumerate(steps):
        text(layout, item, 284, 235 - i * 10, 1.3, "02_TEXTO")

    # Tabela de envelope ilustrativo e matematicamente rastreavel.
    add_rect(layout, 278, 105, 398, 177, "03_COTAS")
    text(layout, "SENSIBILIDADE DE SAIDA (kW)", 283, 168, 1.8, "03_COTAS", bold=True)
    line(layout, (281, 162), (395, 162), "03_COTAS")
    headers = ((285, "CENARIO"), (324, "COMBINACAO"), (385, "TOTAL"))
    for x, label in headers:
        text(layout, label, x, 157, 1.15, "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("S1", "2 DC", "120"),
        ("S2", "2 DC + 2 AC", "142"),
        ("S3", "1 DC + 3 AC", "93"),
        ("S4", "2 DC + 4 AC", "164"),
    )
    for i, row in enumerate(rows):
        y = 149 - i * 9
        line(layout, (281, y - 3), (395, y - 3), "03_COTAS")
        text(layout, row[0], 285, y, 1.35, "02_TEXTO", centered=True)
        text(layout, row[1], 324, y, 1.35, "02_TEXTO", centered=True)
        text(layout, row[2], 385, y, 1.35, "02_TEXTO", centered=True)
    text(layout, "Soma ideal das saidas; nao representa limite da rede.", 283, 109, 1.15, "13_NOTAS")
    add_rect(layout, 24, 104, 134, 138, "13_NOTAS")
    text(layout, "ESTADOS OPERACIONAIS PROPOSTOS", 29, 130, 1.65, "13_NOTAS", bold=True)
    states = ("DISPONIVEL", "SESSAO", "LIMITADO", "PAUSA", "FALHA DE DADOS")
    for i, state in enumerate(states):
        x = 28 + i * 21
        add_rect(layout, x, 112, x + 19, 123, "06_COMANDO")
        text(layout, state, x + 9.5, 117.5, 0.9, "06_COMANDO", centered=True, bold=True)
    text(layout, "Retorno depende de equipamentos e criterios operacionais.", 29, 107, 1.0, "13_NOTAS")


SHEETS = (
    {
        "filename": "01_layout_estacao_recarga.dxf",
        "title": "ARRANJO CONCEITUAL DA ESTACAO DE RECARGA",
        "subtitle": "Seis pontos de carga AC/DC, circulacao esquematica e rota de infraestrutura",
        "scale": "S/ESC.",
        "notes": "Local, geometria, vagas, rota, acessibilidade e protecao mecanica sao premissas abertas.\\P"
                "Confirmar levantamento, concessionaria, acesso e dados OEM antes de qualquer projeto real.",
        "legend": "EVSE: equipamento de alimentacao de veiculo eletrico | AC: corrente alternada | DC: corrente continua | EMS: gestor de energia",
        "draw": draw_site,
    },
    {
        "filename": "02_diagrama_unifilar_estacao.dxf",
        "title": "DIAGRAMA UNIFILAR DA ALIMENTACAO EV",
        "subtitle": "Fronteiras, seis alimentadores e interface de gestao; protecoes ainda nao selecionadas",
        "scale": "S/ESC.",
        "notes": "Tensao, aterramento, curto-circuito, seletividade e demanda nao foram confirmados.\\P"
                "QF: tipo, polos, corrente, curva e ajustes pendentes; interface EMS depende de dados OEM.",
        "legend": "QEV: quadro dedicado | QGBT: quadro geral | QF-01 a QF-06: protecoes nao selecionadas | Pnom. saida assumida: 4 x 11 + 2 x 60 = 164 kW; nao e demanda da rede.",
        "draw": draw_single_line,
    },
    {
        "filename": "03_gestao_dinamica_carga.dxf",
        "title": "GESTAO DE POTENCIA E SEQUENCIA OPERACIONAL",
        "subtitle": "Dados de entrada, alocacao de potencia, estados e cenarios aritmeticos de saida",
        "scale": "S/ESC.",
        "notes": "Compatibilidade, interface, limites, prioridades, rampas, falhas e comportamento de perda de comunicacao requerem validacao.\\P"
                "A matriz de sensibilidade e uma soma de potencias nominais assumidas; nao e calculo de demanda ou entrada.",
        "legend": "Pdisp: margem disponibilizada pelo operador | AC/DC: tipo de saida | setpoint: limite solicitado ao equipamento, sujeito a aceite OEM",
        "draw": draw_management,
    },
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    warning = config["portfolio"]["warning"]
    if warning != WARNING_FALLBACK:
        # A configuracao central e a fonte do aviso obrigatorio.
        pass
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(config, index, spec, spec["draw"])
        print(f"DXF gerado: {PROJECT_DIR / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
