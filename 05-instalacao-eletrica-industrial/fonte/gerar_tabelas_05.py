"""Gera o workbook técnico reproduzível do Projeto 05 com openpyxl."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side


NAVY = "1F4E78"
BLUE = "D9EAF7"
PALE = "FFF2CC"
GRAY = "E7E6E6"
GREEN = "E2F0D9"
RED = "F4CCCC"
WHITE = "FFFFFF"
TEXT = "1F1F1F"
FONT = "Arial"
FIXED_DATE = datetime(2026, 9, 10, 12, 0, 0)
WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação "
    "ou execução de serviços sem revisão, dimensionamento e responsabilidade de "
    "profissional legalmente habilitado."
)
THIN = Side(style="thin", color="D9D9D9")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, help="Destino XLSX; por padrão, atualiza o workbook do projeto")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def base_sheet(workbook: Workbook, name: str, subtitle: str):
    sheet = workbook.create_sheet(name)
    sheet.sheet_view.showGridLines = False
    sheet["A2"] = name.upper()
    sheet["A2"].font = Font(name=FONT, size=14, bold=True, color=NAVY)
    sheet["A3"] = subtitle
    sheet["A3"].font = Font(name=FONT, size=9, italic=True, color="666666")
    bottom = Side(style="thin", color=NAVY)
    for cell in sheet["2:2"][:6]:
        cell.border = Border(bottom=bottom)
    return sheet


def apply_header(sheet, cell_range: str) -> None:
    for row in sheet[cell_range]:
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=NAVY)
            cell.font = Font(name=FONT, size=10, bold=True, color=WHITE)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def apply_body(sheet, cell_range: str) -> None:
    for row in sheet[cell_range]:
        for cell in row:
            cell.font = Font(name=FONT, size=10, color=TEXT)
            cell.alignment = Alignment(vertical="center")
            cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def apply_total(sheet, cell_range: str) -> None:
    for row in sheet[cell_range]:
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=GRAY)
            cell.font = Font(name=FONT, size=10, bold=True)
            cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def set_widths(sheet, widths: dict[str, float]) -> None:
    for column, width in widths.items():
        sheet.column_dimensions[column].width = width


def write_row(sheet, row: int, values: list[object], start_column: int = 1) -> None:
    for offset, value in enumerate(values):
        sheet.cell(row=row, column=start_column + offset, value=value)


def number(value: str) -> float:
    return float(value.replace(",", "."))


def normalize_xlsx(path: Path) -> None:
    """Normaliza ordem e timestamps do ZIP para obter saída determinística."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    with ZipFile(path, "r") as source, ZipFile(
        temporary,
        "w",
        compression=ZIP_DEFLATED,
        compresslevel=9,
    ) as target:
        for name in sorted(source.namelist()):
            original = source.getinfo(name)
            data = source.read(name)
            if name == "docProps/core.xml":
                data = re.sub(
                    rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                    rb"\g<1>2026-09-10T12:00:00Z\g<2>",
                    data,
                )
            info = ZipInfo(name, date_time=(2026, 9, 10, 12, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = original.external_attr
            info.internal_attr = original.internal_attr
            info.create_system = original.create_system
            target.writestr(info, data)
    temporary.replace(path)


def create_workbook(project: Path) -> Workbook:
    loads = read_csv(project / "quadro-cargas.csv")
    feeders = read_csv(project / "alimentadores.csv")
    cables = read_csv(project / "lista-cabos.csv")
    materials = read_csv(project / "lista-materiais.csv")

    workbook = Workbook()
    workbook.remove(workbook.active)
    workbook.properties.creator = "Rogério Eduardo Moreira Menegueli"
    workbook.properties.lastModifiedBy = "Rogério Eduardo Moreira Menegueli"
    workbook.properties.title = "Projeto 05 - Instalação elétrica industrial"
    workbook.properties.subject = "Workbook técnico acadêmico e reproduzível"
    workbook.properties.description = "Tabelas, fórmulas e auditoria do Projeto 05."
    workbook.properties.created = FIXED_DATE
    workbook.properties.modified = FIXED_DATE
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    workbook.calculation.calcMode = "auto"

    summary = base_sheet(
        workbook,
        "Resumo",
        "Projeto 05 - instalação elétrica industrial | revisão 00 | 2026-09-09",
    )
    write_row(summary, 5, ["Indicador", "Resultado"])
    apply_header(summary, "A5:B5")
    indicators = [
        "Potência ativa instalada (kW)",
        "Potência aparente instalada (kVA)",
        "Potência ativa demandada (kW)",
        "Potência aparente demandada (kVA)",
        "Corrente equivalente (A)",
        "Maior corrente de fase (A)",
        "Desequilíbrio total (%)",
        "Maior queda combinada (%)",
        "Circuitos / alimentadores",
    ]
    formulas = [
        "='Quadro Cargas'!I20",
        "='Quadro Cargas'!J20",
        "='Quadro Cargas'!L20",
        "='Quadro Cargas'!M20",
        "='Quadro Cargas'!M20*1000/(SQRT(3)*380)",
        "=MAX(Auditoria!B14:B16)",
        "=Auditoria!B18",
        "=MAX(Circuitos!L4:L19)",
        '=16&" / "&4',
    ]
    for row, (indicator, formula) in enumerate(zip(indicators, formulas), start=6):
        write_row(summary, row, [indicator, formula])
    apply_body(summary, "A6:B14")
    for row in range(6, 14):
        summary[f"B{row}"].number_format = "0.000"
    summary["B14"].alignment = Alignment(horizontal="center", vertical="center")
    write_row(summary, 5, ["Quadro", "P inst. kW", "S inst. kVA", "P dem. kW", "S dem. kVA"], 4)
    apply_header(summary, "D5:H5")
    for row, name in enumerate(["QDF-05", "QDL-05", "QADM-05", "TOTAL"], start=6):
        summary[f"D{row}"] = name
    summary["E6"], summary["F6"], summary["G6"], summary["H6"] = (
        "=SUM('Quadro Cargas'!I4:I11)", "=SUM('Quadro Cargas'!J4:J11)",
        "=SUM('Quadro Cargas'!L4:L11)", "=SUM('Quadro Cargas'!M4:M11)",
    )
    summary["E7"], summary["F7"], summary["G7"], summary["H7"] = (
        "=SUM('Quadro Cargas'!I12:I16)", "=SUM('Quadro Cargas'!J12:J16)",
        "=SUM('Quadro Cargas'!L12:L16)", "=SUM('Quadro Cargas'!M12:M16)",
    )
    summary["E8"], summary["F8"], summary["G8"], summary["H8"] = (
        "=SUM('Quadro Cargas'!I17:I19)", "=SUM('Quadro Cargas'!J17:J19)",
        "=SUM('Quadro Cargas'!L17:L19)", "=SUM('Quadro Cargas'!M17:M19)",
    )
    summary["E9"], summary["F9"], summary["G9"], summary["H9"] = (
        "='Quadro Cargas'!I20", "='Quadro Cargas'!J20",
        "='Quadro Cargas'!L20", "='Quadro Cargas'!M20",
    )
    apply_body(summary, "D6:H9")
    apply_total(summary, "D9:H9")
    for row in range(6, 10):
        for column in range(5, 9):
            summary.cell(row, column).number_format = "0.000"
    summary.merge_cells("A16:H18")
    summary["A16"] = WARNING
    summary["A16"].fill = PatternFill("solid", fgColor=PALE)
    summary["A16"].font = Font(name=FONT, size=10, bold=True, color="7F6000")
    summary["A16"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    summary["A16"].border = Border(left=Side(style="thin", color="BF9000"), right=Side(style="thin", color="BF9000"), top=Side(style="thin", color="BF9000"), bottom=Side(style="thin", color="BF9000"))
    set_widths(summary, {"A": 38, "B": 18, "C": 3, "D": 14, "E": 16, "F": 16, "G": 16, "H": 16})
    summary.freeze_panes = "A6"

    load_sheet = base_sheet(workbook, "Quadro Cargas", "Entradas do CSV e fórmulas de potência/corrente; valores em kW, kVA, V e A")
    load_headers = ["Circuito", "Quadro", "Descrição", "Fases", "V", "P saída", "η", "fp", "P inst.", "S inst.", "fd", "P dem.", "S dem.", "Ib"]
    write_row(load_sheet, 3, load_headers)
    apply_header(load_sheet, "A3:N3")
    for row, item in enumerate(loads, start=4):
        write_row(load_sheet, row, [item["circuito"], item["quadro"], item["descricao"], item["fases"], number(item["tensao_v"]), number(item["potencia_saida_kw"]), number(item["rendimento"]), number(item["fator_potencia"])])
        load_sheet[f"K{row}"] = number(item["fator_demanda"])
        load_sheet[f"I{row}"] = f"=F{row}/G{row}"
        load_sheet[f"J{row}"] = f"=I{row}/H{row}"
        load_sheet[f"L{row}"] = f"=I{row}*K{row}"
        load_sheet[f"M{row}"] = f"=J{row}*K{row}"
        load_sheet[f"N{row}"] = f'=IF(D{row}="ABC",J{row}*1000/(SQRT(3)*E{row}),J{row}*1000/E{row})'
    load_sheet["A20"] = "TOTAL"
    for column in ("I", "J", "L", "M"):
        load_sheet[f"{column}20"] = f"=SUM({column}4:{column}19)"
    apply_body(load_sheet, "A4:N20")
    apply_total(load_sheet, "A20:N20")
    for row in range(4, 21):
        for column in range(5, 15):
            load_sheet.cell(row, column).number_format = "0.000000"
    for row in range(4, 20):
        load_sheet[f"K{row}"].number_format = "0.00"
        load_sheet[f"C{row}"].alignment = Alignment(vertical="center", wrap_text=True)
    set_widths(load_sheet, {"A": 10, "B": 12, "C": 34, "D": 9, **{column: 12 for column in "EFGHIJKLMN"}})
    load_sheet.freeze_panes = "A4"

    circuits = base_sheet(workbook, "Circuitos", "Dimensionamento preliminar e queda combinada; rho = 0,0225 ohm.mm²/m")
    write_row(circuits, 3, ["Circuito", "Quadro", "Descrição", "Ib (A)", "L (m)", "S (mm²)", "PE (mm²)", "In (A)", "Iz (A)", "dV circ. (%)", "dV aliment. (%)", "dV total (%)"])
    apply_header(circuits, "A3:L3")
    for row, item in enumerate(loads, start=4):
        write_row(circuits, row, [item["circuito"], item["quadro"], item["descricao"], None, number(item["comprimento_m"]), number(item["condutor_mm2"]), number(item["pe_mm2"]), number(item["disjuntor_a"]), number(item["iz_assumida_a"])])
        circuits[f"D{row}"] = f"='Quadro Cargas'!N{row}"
        circuits[f"J{row}"] = f'=100*IF(\'Quadro Cargas\'!D{row}="ABC",SQRT(3),2)*0.0225*E{row}*D{row}/F{row}/\'Quadro Cargas\'!E{row}'
        circuits[f"K{row}"] = f'=IF(B{row}="QDF-05",Alimentadores!N5,IF(B{row}="QDL-05",Alimentadores!N6,Alimentadores!N7))'
        circuits[f"L{row}"] = f"=J{row}+K{row}+Alimentadores!N4"
    apply_body(circuits, "A4:L19")
    for row in range(4, 20):
        for column in range(4, 13):
            circuits.cell(row, column).number_format = "0.000"
        circuits[f"C{row}"].alignment = Alignment(vertical="center", wrap_text=True)
    circuits.conditional_formatting.add("L4:L19", CellIsRule(operator="greaterThan", formula=["4"], fill=PatternFill("solid", fgColor=RED), font=Font(color="9C0006", bold=True)))
    circuits.conditional_formatting.add("L4:L19", CellIsRule(operator="lessThanOrEqual", formula=["4"], fill=PatternFill("solid", fgColor=GREEN), font=Font(color="006100")))
    set_widths(circuits, {"A": 10, "B": 12, "C": 34, **{column: 13 for column in "DEFGHIJKL"}})
    circuits.freeze_panes = "A4"

    feeders_sheet = base_sheet(workbook, "Alimentadores", "Corrente de projeto, proteção, ampacidade e queda de tensão")
    write_row(feeders_sheet, 3, ["Alimentador", "De", "Para", "Quadro", "Sistema", "V ref.", "S dem. kVA", "Ib (A)", "L (m)", "S (mm²)", "PE (mm²)", "In (A)", "Iz (A)", "dV (%)", "Ib<=In", "In<=Iz"])
    apply_header(feeders_sheet, "A3:P3")
    for row, item in enumerate(feeders, start=4):
        write_row(feeders_sheet, row, [item["alimentador"], item["de"], item["para"], item["quadro_destino"], item["fases"], number(item["tensao_v"]), None, None, number(item["comprimento_m"]), number(item["condutores_fase_neutro_mm2"]), number(item["pe_mm2"]), number(item["disjuntor_a"]), number(item["iz_assumida_a"])])
    feeders_sheet["G4"], feeders_sheet["H4"] = "='Quadro Cargas'!M20", "=H5+('Quadro Cargas'!M13+'Quadro Cargas'!M15+'Quadro Cargas'!M18)*1000/220"
    feeders_sheet["G5"], feeders_sheet["H5"] = "=SUM('Quadro Cargas'!M4:M11)", "=G5*1000/(SQRT(3)*380)"
    feeders_sheet["G6"], feeders_sheet["H6"] = "=SUM('Quadro Cargas'!M12:M16)", "=('Quadro Cargas'!M13+'Quadro Cargas'!M15)*1000/220"
    feeders_sheet["G7"], feeders_sheet["H7"] = "=SUM('Quadro Cargas'!M17:M19)", "='Quadro Cargas'!M17*1000/220"
    for row in range(4, 8):
        feeders_sheet[f"N{row}"] = f'=100*IF(A{row}="AL-QDF",SQRT(3),2)*0.0225*I{row}*H{row}/J{row}/IF(A{row}="AL-QDF",380,220)'
        feeders_sheet[f"O{row}"] = f'=IF(H{row}<=L{row},"PASS","FAIL")'
        feeders_sheet[f"P{row}"] = f'=IF(L{row}<=M{row},"PASS","FAIL")'
    apply_body(feeders_sheet, "A4:P7")
    for row in range(4, 8):
        for column in range(7, 15):
            feeders_sheet.cell(row, column).number_format = "0.000000"
    green_font = Font(color="006100", bold=True)
    red_font = Font(color="9C0006", bold=True)
    feeders_sheet.conditional_formatting.add("O4:P7", FormulaRule(formula=['ISNUMBER(SEARCH("PASS",O4))'], fill=PatternFill("solid", fgColor=GREEN), font=green_font))
    feeders_sheet.conditional_formatting.add("O4:P7", FormulaRule(formula=['ISNUMBER(SEARCH("FAIL",O4))'], fill=PatternFill("solid", fgColor=RED), font=red_font))
    set_widths(feeders_sheet, {"A": 14, "B": 18, "C": 18, "D": 18, **{column: 12 for column in "EFGHIJKLMNOP"}})
    feeders_sheet.freeze_panes = "A4"

    cable_sheet = base_sheet(workbook, "Cabos", "Lista de cabos e rotas - comprimentos assumidos")
    write_row(cable_sheet, 3, ["Cabo", "De", "Para", "Função", "Formação", "Blindagem", "L (m)", "Condutores", "Observações", "Circuito", "Rota", "dV (%)"])
    apply_header(cable_sheet, "A3:L3")
    for row, item in enumerate(cables, start=4):
        write_row(cable_sheet, row, [item["cabo"], item["de"], item["para"], item["funcao"], item["formacao"], item["blindagem"], number(item["comprimento_assumido_m"]), item["identificacao_condutores"], item["observacoes"], item["circuito"], item["rota"], number(item["queda_pct"])])
    apply_body(cable_sheet, f"A4:L{len(cables) + 3}")
    for row in range(4, len(cables) + 4):
        cable_sheet[f"G{row}"].number_format = "0.0"
        cable_sheet[f"L{row}"].number_format = "0.000"
        for column in range(4, 10):
            cable_sheet.cell(row, column).alignment = Alignment(vertical="center", wrap_text=True)
    set_widths(cable_sheet, {"A": 15, "B": 15, "C": 15, "D": 24, "E": 30, "F": 15, "G": 15, "H": 15, "I": 34, "J": 14, "K": 14, "L": 14})
    cable_sheet.freeze_panes = "A4"

    material_sheet = base_sheet(workbook, "Materiais", "Lista consolidada de materiais - quantitativos acadêmicos")
    write_row(material_sheet, 3, ["Item", "Quantidade", "Unidade", "Descrição", "Referência", "Observações"])
    apply_header(material_sheet, "A3:F3")
    for row, item in enumerate(materials, start=4):
        write_row(material_sheet, row, [item["item"], number(item["quantidade"]), item["unidade"], item["descricao"], item["referencia"], item["observacoes"]])
    apply_body(material_sheet, f"A4:F{len(materials) + 3}")
    for row in range(4, len(materials) + 4):
        for column in range(4, 7):
            material_sheet.cell(row, column).alignment = Alignment(vertical="center", wrap_text=True)
    set_widths(material_sheet, {"A": 16, "B": 12, "C": 12, "D": 40, "E": 22, "F": 42})
    material_sheet.freeze_panes = "A4"

    audit = base_sheet(workbook, "Auditoria", "Reconciliação de totais, fases, proteção, queda e referências")
    write_row(audit, 5, ["Verificação", "Resultado"])
    apply_header(audit, "A5:B5")
    checks = ["Diferença P instalada (kW)", "Diferença S instalada (kVA)", "Diferença P demandada (kW)", "Diferença S demandada (kVA)", "Falhas Ib<=In / In<=Iz", "Quedas combinadas > 4%"]
    audit_formulas = ["='Quadro Cargas'!I20-68.495248", "='Quadro Cargas'!J20-80.277311", "='Quadro Cargas'!L20-48.068716", "='Quadro Cargas'!M20-56.289178", '=COUNTIF(Alimentadores!O4:P7,"FAIL")', '=COUNTIF(Circuitos!L4:L19,">4")']
    for row, (label, formula) in enumerate(zip(checks, audit_formulas), start=6):
        write_row(audit, row, [label, formula])
    apply_body(audit, "A6:B11")
    for row in range(6, 10):
        audit[f"B{row}"].number_format = "0.000000"
    write_row(audit, 13, ["Fase", "Corrente demandada (A)"])
    apply_header(audit, "A13:B13")
    for row, phase in enumerate(["A", "B", "C"], start=14):
        audit[f"A{row}"] = phase
    audit["B14"] = "=Alimentadores!H5+('Quadro Cargas'!M12+'Quadro Cargas'!M17)*1000/220"
    audit["B15"] = "=Alimentadores!H5+('Quadro Cargas'!M13+'Quadro Cargas'!M15+'Quadro Cargas'!M18)*1000/220"
    audit["B16"] = "=Alimentadores!H5+('Quadro Cargas'!M14+'Quadro Cargas'!M16+'Quadro Cargas'!M19)*1000/220"
    audit["A18"], audit["B18"] = "Desequilíbrio (%)", "=(MAX(B14:B16)-MIN(B14:B16))/AVERAGE(B14:B16)*100"
    apply_body(audit, "A14:B18")
    for row in range(14, 19):
        audit[f"B{row}"].number_format = "0.000000"
    write_row(audit, 5, ["Critério", "Status"], 4)
    apply_header(audit, "D5:E5")
    criteria = ["Totais reconciliados", "Proteção dos alimentadores", "Queda combinada", "Desequilíbrio <= 5%", "16 circuitos", "4 alimentadores"]
    statuses = ['=IF(MAX(ABS(B6),ABS(B7),ABS(B8),ABS(B9))<0.00001,"PASS","FAIL")', '=IF(B10=0,"PASS","FAIL")', '=IF(B11=0,"PASS","FAIL")', '=IF(B18<=5,"PASS","FAIL")', '=IF(COUNTA(\'Quadro Cargas\'!A4:A19)=16,"PASS","FAIL")', '=IF(COUNTA(Alimentadores!A4:A7)=4,"PASS","FAIL")']
    for row, (label, formula) in enumerate(zip(criteria, statuses), start=6):
        write_row(audit, row, [label, formula], 4)
    apply_body(audit, "D6:E11")
    audit.conditional_formatting.add("E6:E11", FormulaRule(formula=['ISNUMBER(SEARCH("PASS",E6))'], fill=PatternFill("solid", fgColor=GREEN), font=green_font))
    audit.conditional_formatting.add("E6:E11", FormulaRule(formula=['ISNUMBER(SEARCH("FAIL",E6))'], fill=PatternFill("solid", fgColor=RED), font=red_font))
    set_widths(audit, {"A": 34, "B": 20, "C": 3, "D": 30, "E": 14})
    audit.freeze_panes = "A6"

    return workbook


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    project = root / "05-instalacao-eletrica-industrial"
    output = args.output.resolve() if args.output else project / "tabelas-projeto-05.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook = create_workbook(project)
    workbook.save(output)
    normalize_xlsx(output)
    print(f"Workbook: {output}")
    print(f"Abas: {', '.join(workbook.sheetnames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
