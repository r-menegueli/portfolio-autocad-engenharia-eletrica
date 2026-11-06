"""Gera pranchas conceituais de auxilios visuais luminosos de um aerodromo."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "22-auxilios-visuais-luminosos-aerodromo"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
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

DATE = "2026-11-06"
REVISION = "00"
BOX_BLOCK = "P22_CAIXA_EQUIPAMENTO"
BOX_WIDTH = 57.0
BOX_HEIGHT = 37.0


def text(layout, value: str, x: float, y: float, h: float = 1.3,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(layout, value, (x, y), h, layer=layer,
             align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
             style=TITLE_STYLE if bold else TEXT_STYLE)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def rect(layout, x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)


def arrow(layout, a: tuple[float, float], b: tuple[float, float], layer: str,
          size: float = 1.5) -> None:
    line(layout, a, b, layer)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout, (b[0] - ux * size + side * px * size * 0.55,
                      b[1] - uy * size + side * py * size * 0.55), b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float, title: str,
        detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.2, detail_height: float = 0.9) -> None:
    rect(layout, x0, y0, x1, y1, layer)
    text(layout, title, (x0 + x1) / 2, (y0 + y1) / 2 + (1.4 if detail else 0),
         title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, (x0 + x1) / 2, (y0 + y1) / 2 - 2,
             detail_height, "02_TEXTO", centered=True)


def lamp(layout, x: float, y: float, *, layer: str = "04_EQUIPAMENTOS", tag: str = "") -> None:
    layout.add_circle((x, y), 1.65, dxfattribs={"layer": layer})
    line(layout, (x - 1.0, y - 1.0), (x + 1.0, y + 1.0), layer)
    line(layout, (x - 1.0, y + 1.0), (x + 1.0, y - 1.0), layer)
    if tag:
        text(layout, tag, x + 2.7, y + 1.4, 0.9, "02_TEXTO")


def equipment(layout, x: float, y: float, tag: str, title: str, detail: str,
              *, layer: str = "04_EQUIPAMENTOS") -> None:
    insert = layout.add_blockref(BOX_BLOCK, (x, y), dxfattribs={"layer": layer})
    insert.add_auto_attribs({"TAG": tag, "TITULO": title, "DADOS": detail})


def make_component_block(doc) -> None:
    if BOX_BLOCK in doc.blocks:
        return
    block = doc.blocks.new(name=BOX_BLOCK)
    block.add_lwpolyline([(0, 0), (BOX_WIDTH, 0), (BOX_WIDTH, BOX_HEIGHT), (0, BOX_HEIGHT)],
                         close=True, dxfattribs={"layer": "0"})
    block.add_line((0, 27), (BOX_WIDTH, 27), dxfattribs={"layer": "0"})
    for tag, point, height in (("TAG", (2.0, 31.5), 1.12),
                               ("TITULO", (2.0, 18.3), 1.2),
                               ("DADOS", (2.0, 7.2), 0.95)):
        block.add_attdef(tag, insert=point, text="",
                         dxfattribs={"height": height, "style": TEXT_STYLE, "layer": "0"})


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 2.5, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.35, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 1.8, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.45, "13_NOTAS")
    rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66, 1.6, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.15, "13_NOTAS")
    rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90, 1.6, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.1, "12_LEGENDA")
    rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for label, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, label, x, 89.5, 1.25, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.2, "02_TEXTO", centered=True)


def draw_layout(layout) -> None:
    text(layout, "CONFIGURACAO FICTICIA DE PISTA E PISTA DE TAXI | SEM ESCALA", 24, 253,
         1.25, "05_POTENCIA", bold=True)
    # Geometria didatica de superficie de movimento, sem dimensoes ou afastamentos normativos.
    rect(layout, 46, 162, 350, 206, "11_ARQUITETURA")
    rect(layout, 46, 162, 55, 206, "04_EQUIPAMENTOS")
    rect(layout, 341, 162, 350, 206, "04_EQUIPAMENTOS")
    text(layout, "PISTA RWY-01", 197, 199, 1.2, "11_ARQUITETURA", centered=True, bold=True)
    text(layout, "CABECEIRA A", 50.5, 213, 0.95, "02_TEXTO", centered=True)
    text(layout, "CABECEIRA B", 345.5, 213, 0.95, "02_TEXTO", centered=True)
    # Centro de pista pontilhado e bordas laterais; simbolos sem cor, espacamento ou codigo operacional.
    for x in range(67, 332, 24):
        line(layout, (x, 184), (x + 10, 184), "03_COTAS")
    for x in range(66, 335, 26):
        lamp(layout, x, 164, tag="LBR-01" if x == 66 else "")
        lamp(layout, x, 204)
    for x in (48, 52):
        line(layout, (x, 162), (x, 206), "03_COTAS")
        line(layout, (344, 162), (344, 206), "03_COTAS")
    # Aproximacao esquematica e ligacao a taxiway.
    for x in (26, 34, 42):
        lamp(layout, x, 184, tag="LAP-01" if x == 26 else "")
    rect(layout, 270, 207, 296, 239, "11_ARQUITETURA")
    text(layout, "TWY-A", 283, 228, 1.05, "11_ARQUITETURA", centered=True, bold=True)
    for y in range(212, 237, 8):
        lamp(layout, 273, y, tag="LTW-01" if y == 212 else "")
        lamp(layout, 293, y)
    for y in (212, 220, 228, 236):
        layout.add_circle((283, y), 1.2, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    line(layout, (296, 222), (365, 222), "08_CABOS")
    text(layout, "ROTA DE CIRCUITOS / DRENAGEM A COORDENAR", 313, 226, 0.92, "08_CABOS")
    text(layout, "Posicoes e quantidade de luminarias nao representam afastamentos ou classificacao da pista.",
         24, 112, 1.0, "13_NOTAS")


def draw_circuits(layout) -> None:
    text(layout, "TOPOLOGIA DE CIRCUITOS SERIE E TRANSFORMADORES DE ISOLAMENTO", 24, 253,
         1.3, "05_POTENCIA", bold=True)
    equipment(layout, 25, 211, "PCC-ILS", "FONTE BT", "dados do ponto pendentes")
    equipment(layout, 105, 211, "QGBT-ILS", "DISTRIBUICAO", "selecao a estudar")
    equipment(layout, 292, 211, "SCIL-01", "CONTROLE", "interface a especificar", layer="06_COMANDO")
    arrow(layout, (82, 229.5), (105, 229.5), "05_POTENCIA", 1.0)
    arrow(layout, (162, 229.5), (292, 229.5), "05_POTENCIA", 1.2)
    line(layout, (133.5, 211), (133.5, 202), "05_POTENCIA")
    line(layout, (18, 202), (303, 202), "05_POTENCIA")
    arrow(layout, (52, 202), (52, 188), "05_POTENCIA", 1.0)
    line(layout, (18, 202), (18, 121.5), "05_POTENCIA")
    arrow(layout, (18, 121.5), (25, 121.5), "05_POTENCIA", 1.0)
    text(layout, "DERIVACOES PARA CCR — PROTECAO E SELETIVIDADE A DEFINIR", 83, 205, 0.9, "05_POTENCIA")

    rows = (
        ("CCR-01", "REGULADOR", "pista RWY-01", 151.0, "LOOP-01", "TIS / LBR"),
        ("CCR-02", "REGULADOR", "pista de taxi TWY-A", 103.0, "LOOP-02", "TIS / LTW"),
    )
    for ccr, title, detail, y, loop, load in rows:
        equipment(layout, 25, y, ccr, title, "corrente / potencia pendentes")
        box(layout, 130, y, 187, y + 37, loop, "circuito serie primario", layer="08_CABOS")
        box(layout, 245, y, 302, y + 37, load, "transformador por luminaria", layer="04_EQUIPAMENTOS")
        arrow(layout, (82, y + 18.5), (130, y + 18.5), "05_POTENCIA", 1.1)
        arrow(layout, (187, y + 18.5), (245, y + 18.5), "08_CABOS", 1.1)
        text(layout, "RETORNO / CONTINUIDADE DO LOOP A ESTUDAR", 310, y + 18.5, 0.85, "08_CABOS")

    # Interface funcional de monitoracao dos reguladores, sem assumir protocolo ou supervisao instalada.
    line(layout, (320, 211), (320, 196), "06_COMANDO")
    line(layout, (320, 196), (335, 196), "06_COMANDO")
    arrow(layout, (335, 196), (335, 186), "06_COMANDO", 1.0)
    text(layout, "COMANDO / ALARME", 339, 192, 0.88, "06_COMANDO")
def draw_control(layout) -> None:
    text(layout, "CONTROLE, MONITORACAO E EVIDENCIAS PARA ACEITACAO", 24, 253,
         1.35, "13_NOTAS", bold=True)
    box(layout, 24, 211, 105, 244, "OPERADOR / TORRE", "comando sujeito a procedimento", layer="06_COMANDO")
    box(layout, 151, 211, 232, 244, "SCIL-01", "interface local/remota a definir", layer="06_COMANDO")
    box(layout, 278, 211, 396, 244, "CCR-01 / CCR-02", "estado, nivel e falha a monitorar", layer="07_INSTRUMENTACAO")
    arrow(layout, (105, 227.5), (151, 227.5), "06_COMANDO", 1.2)
    arrow(layout, (232, 227.5), (278, 227.5), "06_COMANDO", 1.2)
    arrow(layout, (278, 218), (232, 218), "07_INSTRUMENTACAO", 0.9)

    columns = ((24, 115, "EVENTO / SINAL"), (115, 207, "INDICACAO"),
               (207, 305, "RESPOSTA A DEFINIR"), (305, 396, "EVIDENCIA NECESSARIA"))
    top, head_bottom = 197.0, 187.0
    for left, right, label in columns:
        rect(layout, left, head_bottom, right, top, "12_LEGENDA")
        text(layout, label, (left + right) / 2, 192, 0.95, "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("Falha fonte normal", "estado QGBT / QTA", "indicar fonte disponivel", "transferencia e retorno testados"),
        ("Falha CCR", "alarme do regulador", "indicar circuito afetado", "simular falha conforme fabricante"),
        ("Falha de loop", "alarme / corrente", "registrar circuito", "teste de continuidade e isolacao"),
        ("Perda comunicacao", "SCIL indisponivel", "modo degradado definido", "perda de enlace simulada"),
        ("Comando local/remoto", "modo ativo", "controle sem conflito", "permissivos e autoridade definidos"),
    )
    row_h = (head_bottom - 127.0) / len(rows)
    for index, values in enumerate(rows):
        y_top = head_bottom - index * row_h
        y_bottom = y_top - row_h
        for (left, right, _), value in zip(columns, values):
            rect(layout, left, y_bottom, right, y_top, "02_TEXTO")
            text(layout, value, left + 1.4, (y_top + y_bottom) / 2, 0.93, "02_TEXTO")

    text(layout, "SEQUENCIA DE REVISAO — NAO E PROCEDIMENTO DE OPERACAO", 24, 116, 0.98,
         "06_COMANDO", bold=True)
    steps = ((24, "PROJETO", "classificar auxilio"), (99, "SELECAO", "definir luminaria"),
             (174, "MONTAGEM", "inspecionar circuitos"), (249, "ENSAIOS", "registrar resultados"),
             (324, "LIBERACAO", "autoridade local"))
    for x, title, detail in steps:
        rect(layout, x, 97, x + 65, 111, "06_COMANDO")
        text(layout, title, x + 32.5, 107, 0.85, "06_COMANDO", centered=True, bold=True)
        text(layout, detail, x + 32.5, 101.5, 0.88, "02_TEXTO", centered=True)


SHEETS = (
    {
        "filename": "01_layout_luminoso_pista_taxi.dxf",
        "title": "AUXILIOS VISUAIS LUMINOSOS DE AERODROMO",
        "subtitle": "Arranjo indicativo de pista, cabeceiras, aproximacao e pista de taxi",
        "scale": "S/ESC.",
        "notes": "Planta e simbolos sem escala, afastamentos, classificacao operacional ou cores especificadas.\\P"
                "Compatibilizar auxilios com RBAC 154 vigente, projeto fisico e operacao do aerodromo.",
        "legend": "LBR: luminaria de borda de pista | LAP: aproximacao ilustrativa | LTW: luminaria de taxiway | circulo/X: ponto luminoso sem especificacao de cor",
        "draw": draw_layout,
    },
    {
        "filename": "02_unifilar_circuitos_serie_ccr.dxf",
        "title": "DISTRIBUICAO E CIRCUITOS SERIE DOS AUXILIOS LUMINOSOS",
        "subtitle": "Fonte BT, reguladores de corrente constante, circuitos e transformadores de isolamento",
        "scale": "S/ESC.",
        "notes": "Topologia funcional; correntes, potencia, protecao, cabos e redundancia nao dimensionados.\\P"
                "Nao define tempo de comutacao, monitor de isolamento ou capacidade de contingencia.",
        "legend": "PCC: ponto de conexao | QGBT: quadro geral | CCR: regulador de corrente constante | TIS: transformador de isolamento | LOOP: circuito serie",
        "draw": draw_circuits,
    },
    {
        "filename": "03_controle_monitoracao_e_ensaios.dxf",
        "title": "CONTROLE, MONITORACAO E ENSAIOS DE ACEITACAO",
        "subtitle": "Interfaces e evidencias propostas, sem valores de operacao ou liberacao de pista",
        "scale": "S/ESC.",
        "notes": "Matriz para estudo. Nenhum ensaio, permissivo, comando remoto ou procedimento operacional foi aprovado.\\P"
                "Coordenar autoridades aeroportuarias, ANAC e prestadores de navegacao aerea.",
        "legend": "SCIL: sistema de controle de iluminacao | CCR: regulador | A DEFINIR: sem selecao ou teste | setas: fluxo funcional conceitual",
        "draw": draw_control,
    },
)


def make_sheet(root: Path, config: dict, number: int, spec: dict) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    make_component_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    spec["draw"](layout)
    footer(layout, spec, config["portfolio"]["warning"])
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs({
        "TITULO": spec["title"], "AUTOR": config["portfolio"]["author"],
        "DATA": DATE, "REVISAO": REVISION, "PRANCHA": f"{number:02d}/03",
        "ARQUIVO": spec["filename"], "UNIDADES": "mm", "ESCALA": spec["scale"],
        "FOLHA": "A3", "STATUS": "CONCEIT.",
    })
    output = root / SLUG / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(root, config, index, spec)
        print(f"DXF gerado: {root / SLUG / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
