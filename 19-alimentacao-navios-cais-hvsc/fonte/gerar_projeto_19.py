"""Gera tres pranchas conceituais para alimentacao de navios no cais (HVSC)."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "19-alimentacao-navios-cais-hvsc"
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
BOX_BLOCK = "P19_CAIXA_EQUIPAMENTO"
BOX_WIDTH = 57.0
BOX_HEIGHT = 37.0


def text(layout, value: str, x: float, y: float, h: float = 1.35,
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


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def rect(layout, x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)


def arrow(layout, a: tuple[float, float], b: tuple[float, float], layer: str,
          size: float = 1.65) -> None:
    line(layout, a, b, layer)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout, (b[0] - ux * size + side * px * size * 0.55,
                      b[1] - uy * size + side * py * size * 0.55), b, layer)


def equipment(layout, x: float, y: float, tag: str, title: str, detail: str,
              *, layer: str = "04_EQUIPAMENTOS") -> None:
    insert = layout.add_blockref(BOX_BLOCK, (x, y), dxfattribs={"layer": layer})
    insert.add_auto_attribs({"TAG": tag, "TITULO": title, "DADOS": detail})


def box(layout, x0: float, y0: float, x1: float, y1: float, title: str,
        detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.25, detail_height: float = 1.0) -> None:
    rect(layout, x0, y0, x1, y1, layer)
    text(layout, title, (x0 + x1) / 2, (y0 + y1) / 2 + (1.5 if detail else 0),
         title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, (x0 + x1) / 2, (y0 + y1) / 2 - 2,
             detail_height, "02_TEXTO", centered=True)


def make_component_block(doc) -> None:
    if BOX_BLOCK in doc.blocks:
        return
    block = doc.blocks.new(name=BOX_BLOCK)
    block.add_lwpolyline(
        [(0, 0), (BOX_WIDTH, 0), (BOX_WIDTH, BOX_HEIGHT), (0, BOX_HEIGHT)],
        close=True,
        dxfattribs={"layer": "0"},
    )
    block.add_line((0, 27), (BOX_WIDTH, 27), dxfattribs={"layer": "0"})
    for tag, point, height in (
        ("TAG", (2.0, 31.5), 1.12),
        ("TITULO", (2.0, 18.3), 1.35),
        ("DADOS", (2.0, 7.2), 1.0),
    ):
        block.add_attdef(
            tag,
            insert=point,
            text="",
            dxfattribs={"height": height, "style": TEXT_STYLE, "layer": "0"},
        )


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 2.65, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.45, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 1.8, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.45, "13_NOTAS")
    rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66, 1.65, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.2, "13_NOTAS")
    rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90, 1.65, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.17, "12_LEGENDA")
    rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for label, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, label, x, 89.5, 1.25, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.2, "02_TEXTO", centered=True)


def draw_single_line(layout) -> None:
    text(layout, "HVSC CONCEITUAL | S=3,2 MVA* | 13,8/6,6 kV* | 60 Hz*", 24, 252, 1.45, "05_POTENCIA", bold=True)
    x_positions = (20, 83, 146, 209, 272, 335)
    units = (
        ("PCC-01", "REDE DO PORTO", "13,8 kV | 60 Hz"),
        ("QMT-01", "ENTRADA MT", "protecoes a definir"),
        ("TR-01", "TRANSFORMADOR", "4 MVA | 13,8/6,6 kV*"),
        ("Q-HVSC", "QUADRO HVSC", "6,6 kV | intertravado"),
        ("PT-01", "PONTO NO CAIS", "cabo e plug HVSC"),
        ("NAVIO", "BARRAMENTO", "6,6 kV | 60 Hz*"),
    )
    for x, (tag, title, detail) in zip(x_positions, units):
        equipment(layout, x, 210, tag, title, detail)
    for left, right in zip(x_positions, x_positions[1:]):
        arrow(layout, (left + BOX_WIDTH, 228.5), (right, 228.5), "05_POTENCIA", 1.25)
    for idx, x in enumerate((111.5, 174.5, 237.5, 300.5)):
        line(layout, (x, 210), (x, 187), "05_POTENCIA" if idx < 2 else "07_INSTRUMENTACAO")

    box(layout, 22, 148, 105, 184, "MEDICAO E DADOS", "V, I, P, S, energia", layer="07_INSTRUMENTACAO")
    box(layout, 112, 148, 197, 184, "CONTROLE OPERACIONAL", "estado / permissivos", layer="06_COMANDO")
    box(layout, 204, 148, 289, 184, "INTERFACE NAVIO", "IEC/IEEE 80005-2*", layer="07_INSTRUMENTACAO")
    box(layout, 296, 148, 397, 184, "LAÇO DE SEGURANÇA", "independente dos dados", layer="06_COMANDO")
    arrow(layout, (105, 166), (112, 166), "07_INSTRUMENTACAO", 1.1)
    arrow(layout, (197, 166), (204, 166), "07_INSTRUMENTACAO", 1.1)
    line(layout, (346.5, 148), (346.5, 137), "06_COMANDO")
    line(layout, (113.5, 137), (303.5, 137), "06_COMANDO")
    arrow(layout, (113.5, 137), (113.5, 128), "06_COMANDO", 1.0)
    arrow(layout, (303.5, 137), (303.5, 128), "06_COMANDO", 1.0)
    box(layout, 22, 105, 205, 128, "CB-TERRA / Q-HVSC", "abertura pelo circuito de seguranca", layer="13_NOTAS", title_height=1.15, detail_height=0.9)
    box(layout, 210, 105, 397, 128, "CB-NAVIO", "abertura coordenada a bordo", layer="13_NOTAS", title_height=1.15, detail_height=0.9)
    text(layout, "* Compatibilidade de tensao, frequencia, aterramento, conectores e protecao depende do navio e do porto.", 24, 101, 0.8, "13_NOTAS")


def draw_quay_plan(layout) -> None:
    # Planta esquematica sem escala; geometria simples para explicitar interfaces.
    rect(layout, 24, 116, 156, 245, "11_ARQUITETURA")
    text(layout, "AREA TERRESTRE / TERMINAL", 28, 237, 1.4, "11_ARQUITETURA", bold=True)
    rect(layout, 38, 184, 140, 225, "11_ARQUITETURA")
    text(layout, "SALA ELETRICA", 89, 210, 1.55, "11_ARQUITETURA", centered=True, bold=True)
    text(layout, "QMT-01 | TR-01 | Q-HVSC", 89, 196, 1.15, "02_TEXTO", centered=True)
    rect(layout, 165, 116, 194, 245, "11_ARQUITETURA")
    text(layout, "CAIS", 179, 238, 1.4, "11_ARQUITETURA", centered=True, bold=True)
    line(layout, (140, 204), (178, 204), "05_POTENCIA")
    line(layout, (178, 204), (178, 174), "05_POTENCIA")
    rect(layout, 174, 166, 182, 174, "04_EQUIPAMENTOS")
    text(layout, "PT-01", 183, 179, 0.95, "04_EQUIPAMENTOS", bold=True)
    text(layout, "armario HVSC", 183, 176, 0.85, "02_TEXTO")
    rect(layout, 212, 116, 398, 245, "11_ARQUITETURA")
    text(layout, "BACIA DO PORTO", 300, 237, 1.5, "11_ARQUITETURA", centered=True, bold=True)

    # Navio representado por contorno esquematico, sem dimensao ou escala de cais.
    layout.add_lwpolyline(
        [(225, 147), (240, 130), (360, 130), (385, 148), (374, 202), (241, 202), (225, 147)],
        dxfattribs={"layer": "11_ARQUITETURA", "closed": True},
    )
    text(layout, "NAVIO COMPATIVEL COM HVSC", 302, 181, 1.55, "11_ARQUITETURA", centered=True, bold=True)
    line(layout, (178, 166), (238, 166), "08_CABOS")
    line(layout, (238, 166), (238, 194), "08_CABOS")
    line(layout, (238, 194), (247, 194), "08_CABOS")
    layout.add_circle((238, 194), radius=2.1, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    text(layout, "PA-01 / INLET HVSC", 249, 197, 1.0, "04_EQUIPAMENTOS", bold=True)
    text(layout, "CABO HVSC — ROTA ESQUEMATICA", 207, 158, 1.0, "08_CABOS")


def draw_sequence(layout) -> None:
    text(layout, "SEQUENCIA DIDATICA DE ALTO NIVEL — NAO SUBSTITUI O PROCEDIMENTO HVSC APLICAVEL", 24, 250, 1.25, "13_NOTAS", bold=True)
    stages = (
        ("S0", "ISOLADO", "CBs abertos;\nfonte indisponivel"),
        ("S1", "COMPATIVEL", "navio, tensao,\nfrequencia e dados"),
        ("S2", "CONECTADO", "interface mecanica\ne cabo verificados"),
        ("S3", "PERMISSIVOS", "terra, seguranca\ne comunicacao"),
        ("S4", "AUTORIZADO", "parametros e\nprocedimento aceitos"),
        ("S5", "ALIMENTADO", "transferencia por\nprocedimento aprovado"),
    )
    x_positions = (21, 84, 147, 210, 273, 336)
    for x, (tag, title, detail) in zip(x_positions, stages):
        rect(layout, x, 202, x + 58, 239, "06_COMANDO")
        text(layout, tag, x + 3, 233, 1.0, "06_COMANDO", bold=True)
        text(layout, title, x + 29, 225, 1.12, "02_TEXTO", centered=True, bold=True)
        add_mtext(layout, detail.replace("\n", "\\P"), (x + 4, 218), 50, 1.0, "02_TEXTO")
    for left, right in zip(x_positions, x_positions[1:]):
        arrow(layout, (left + 58, 220.5), (right, 220.5), "06_COMANDO", 1.1)

    box(layout, 22, 154, 205, 189, "ABERTURA DO CIRCUITO DE SEGURANCA", "trip coordenado dos CBs HVSC de terra e a bordo; limite da norma a confirmar", layer="06_COMANDO", title_height=1.1, detail_height=0.95)
    box(layout, 216, 154, 398, 189, "COMUNICACAO DE DADOS", "monitoramento/controle funcional nao substitui o circuito de seguranca", layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=0.95)
    arrow(layout, (205, 171.5), (216, 171.5), "07_INSTRUMENTACAO", 0.95)
    text(layout, "EVENTO DE ABERTURA DO LAÇO -> ABERTURA AUTOMATICA DOS DISJUNTORES HVSC EM ATE 200 ms, CONFORME IEC/IEEE 80005-1:2019 + EMENDAS*", 24, 141, 1.1, "05_POTENCIA", bold=True)

    # Matriz compacta: estados esperados, sem alegar FAT/SAT ou ensaio de campo.
    x0, x1 = 22.0, 398.0
    top = 137.0
    columns = ((x0, 98, "CONDICAO"), (98, 233, "EVIDENCIA / INTERFACE"), (233, 325, "RESPOSTA ESPERADA"), (325, x1, "ESTADO"))
    for left, right, label in columns:
        rect(layout, left, 123, right, top, "12_LEGENDA")
        text(layout, label, (left + right) / 2, 131, 0.9, "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("Compatibilidade", "tensao/frequencia/interface aprovadas", "bloquear energizacao se pendente", "A VALIDAR"),
        ("Cabo e conector", "estado mecanico e confirmacao de acoplamento", "manter fonte isolada", "A VALIDAR"),
        ("Laço de seguranca", "circuito dedicado fechado e supervisionado", "trip coordenado ao abrir", "A VALIDAR"),
        ("Dados operacionais", "interface nao emergencial conforme 80005-2", "alarme / permissivo conforme projeto", "A VALIDAR"),
    )
    row_h = 5.0
    for index, values in enumerate(rows):
        y_top = 123.0 - index * row_h
        y_bottom = y_top - row_h
        for (left, right, _), value in zip(columns, values):
            rect(layout, left, y_bottom, right, y_top, "02_TEXTO")
            text(layout, value, left + 2, (y_bottom + y_top) / 2, 0.98, "02_TEXTO")
    text(layout, "* Revisar texto integral, emendas, anexo de tipo de navio, autoridades portuarias e requisitos locais antes de qualquer uso.", 24, 140, 0.8, "13_NOTAS")


SHEETS = (
    {
        "filename": "01_unifilar_hvsc_cais.dxf",
        "title": "ALIMENTACAO HVSC NO CAIS — DIAGRAMA UNIFILAR",
        "subtitle": "Rede do porto, transformacao, quadro HVSC e interface eletrica com o navio",
        "scale": "S/ESC.",
        "notes": "Base ilustrativa: 3,2 MVA em 6,6 kV/60 Hz; entrada 13,8 kV; transformador 4 MVA.\\P"
                "Nao define protecoes, aterramento, cabos, aterramento do neutro ou parametros de equipamento.",
        "legend": "HVSC: conexao de alta tensao em terra | QMT: quadro MT | CB: disjuntor | PCC: ponto de acoplamento comum | S: potencia aparente",
        "draw": draw_single_line,
    },
    {
        "filename": "02_implantacao_eletrica_cais.dxf",
        "title": "IMPLANTACAO CONCEITUAL DA INTERFACE NO CAIS",
        "subtitle": "Sala eletrica, ponto de conexao, rota esquematica e navio em berco",
        "scale": "S/ESC.",
        "notes": "Planta esquematica sem escala, levantamento topografico ou dimensoes reais.\\P"
                "Posicao, acesso, alcance, esforcos e manuseio dos cabos devem ser estudados no local.",
        "legend": "PT: ponto no cais | PA: ponto de acoplamento | rota e contorno: ilustrativos | limites de acesso: nao definidos",
        "draw": draw_quay_plan,
    },
    {
        "filename": "03_sequencia_intertravamentos_hvsc.dxf",
        "title": "INTERFACES E SEQUENCIA CONCEITUAL DE CONEXAO HVSC",
        "subtitle": "Permissivos, circuito de seguranca, comunicacao de dados e eventos a validar",
        "scale": "S/ESC.",
        "notes": "Sequencia didatica de alto nivel; nao e procedimento operacional nem logica de seguranca.\\P"
                "Ensaios, tempos, intertravamentos e interfaces dependem do navio, porto e norma aplicavel.",
        "legend": "CB: disjuntor | HVSC: conexao de alta tensao em terra | dados funcionais nao substituem seguranca dedicada",
        "draw": draw_sequence,
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
