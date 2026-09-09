import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

function argumentValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

async function loadArtifactTool() {
  try {
    return await import("@oai/artifact-tool");
  } catch (error) {
    const moduleRoot = argumentValue("--node-modules", "");
    if (!moduleRoot) {
      throw new Error(
        "@oai/artifact-tool não encontrado. Instale as dependências ou informe --node-modules <diretório>.",
        { cause: error },
      );
    }
    const entry = path.join(path.resolve(moduleRoot), "@oai", "artifact-tool", "dist", "artifact_tool.mjs");
    return import(pathToFileURL(entry).href);
  }
}

const sourceDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(argumentValue("--root", path.join(sourceDirectory, "..", "..")));
const { SpreadsheetFile, Workbook } = await loadArtifactTool();
const project = path.join(root, "05-instalacao-eletrica-industrial");
const previewDir = path.join(root, "work", "spreadsheet-p05", "previews");
await fs.mkdir(previewDir, { recursive: true });

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split(",");
  return lines.map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""]));
  });
}

const loads = parseCsv(await fs.readFile(path.join(project, "quadro-cargas.csv"), "utf8"));
const feeders = parseCsv(await fs.readFile(path.join(project, "alimentadores.csv"), "utf8"));
const cables = parseCsv(await fs.readFile(path.join(project, "lista-cabos.csv"), "utf8"));
const materials = parseCsv(await fs.readFile(path.join(project, "lista-materiais.csv"), "utf8"));

const wb = Workbook.create();
const navy = "#1F4E78";
const blue = "#D9EAF7";
const pale = "#FFF2CC";
const gray = "#E7E6E6";
const green = "#E2F0D9";
const red = "#F4CCCC";
const font = "Arial";

function baseSheet(name, subtitle) {
  const sheet = wb.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.getRange("A2").values = [[name.toUpperCase()]];
  sheet.getRange("A2").format.font = { name: font, size: 14, bold: true, color: navy };
  sheet.getRange("A3").values = [[subtitle]];
  sheet.getRange("A3").format.font = { name: font, size: 9, italic: true, color: "#666666" };
  sheet.getRange("A2:F2").format.borders = { bottom: { style: "thin", color: navy } };
  return sheet;
}

function header(range) {
  range.format = {
    fill: navy,
    font: { name: font, size: 10, bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
    horizontalAlignment: "center",
    borders: { preset: "all", style: "thin", color: "#B4C6E7" },
  };
}

function body(range) {
  range.format.font = { name: font, size: 10, color: "#1F1F1F" };
  range.format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
  range.format.verticalAlignment = "center";
}

const summary = baseSheet("Resumo", "Projeto 05 - instalação elétrica industrial | revisão 00 | 2026-09-09");
summary.getRange("A5:B5").values = [["Indicador", "Resultado"]];
header(summary.getRange("A5:B5"));
summary.getRange("A6:A14").values = [
  ["Potência ativa instalada (kW)"],
  ["Potência aparente instalada (kVA)"],
  ["Potência ativa demandada (kW)"],
  ["Potência aparente demandada (kVA)"],
  ["Corrente equivalente (A)"],
  ["Maior corrente de fase (A)"],
  ["Desequilíbrio total (%)"],
  ["Maior queda combinada (%)"],
  ["Circuitos / alimentadores"],
];
summary.getRange("B6:B14").formulas = [
  ["='Quadro Cargas'!I20"],
  ["='Quadro Cargas'!J20"],
  ["='Quadro Cargas'!L20"],
  ["='Quadro Cargas'!M20"],
  ["='Quadro Cargas'!M20*1000/(SQRT(3)*380)"],
  ["=MAX(Auditoria!B14:B16)"],
  ["=Auditoria!B18"],
  ["=MAX(Circuitos!L4:L19)"],
  ["=16&\" / \"&4"],
];
body(summary.getRange("A6:B14"));
summary.getRange("B6:B13").format.numberFormat = "0.000";
summary.getRange("B14").format.horizontalAlignment = "center";
summary.getRange("D5:H5").values = [["Quadro", "P inst. kW", "S inst. kVA", "P dem. kW", "S dem. kVA"]];
header(summary.getRange("D5:H5"));
summary.getRange("D6:D9").values = [["QDF-05"], ["QDL-05"], ["QADM-05"], ["TOTAL"]];
summary.getRange("E6:H6").formulas = [["=SUM('Quadro Cargas'!I4:I11)", "=SUM('Quadro Cargas'!J4:J11)", "=SUM('Quadro Cargas'!L4:L11)", "=SUM('Quadro Cargas'!M4:M11)"]];
summary.getRange("E7:H7").formulas = [["=SUM('Quadro Cargas'!I12:I16)", "=SUM('Quadro Cargas'!J12:J16)", "=SUM('Quadro Cargas'!L12:L16)", "=SUM('Quadro Cargas'!M12:M16)"]];
summary.getRange("E8:H8").formulas = [["=SUM('Quadro Cargas'!I17:I19)", "=SUM('Quadro Cargas'!J17:J19)", "=SUM('Quadro Cargas'!L17:L19)", "=SUM('Quadro Cargas'!M17:M19)"]];
summary.getRange("E9:H9").formulas = [["='Quadro Cargas'!I20", "='Quadro Cargas'!J20", "='Quadro Cargas'!L20", "='Quadro Cargas'!M20"]];
body(summary.getRange("D6:H9"));
summary.getRange("D9:H9").format = { fill: gray, font: { name: font, size: 10, bold: true }, borders: { preset: "all", style: "thin", color: "#A6A6A6" } };
summary.getRange("E6:H9").format.numberFormat = "0.000";
summary.getRange("A16:H18").merge();
summary.getRange("A16").values = [["Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado."]];
summary.getRange("A16:H18").format = { fill: pale, font: { name: font, size: 10, bold: true, color: "#7F6000" }, wrapText: true, verticalAlignment: "center", horizontalAlignment: "left", borders: { preset: "outside", style: "thin", color: "#BF9000" } };
summary.getRange("A:A").format.columnWidth = 38;
summary.getRange("B:B").format.columnWidth = 18;
summary.getRange("C:C").format.columnWidth = 3;
summary.getRange("D:D").format.columnWidth = 14;
summary.getRange("E:H").format.columnWidth = 16;
summary.freezePanes.freezeRows(5);

const loadSheet = baseSheet("Quadro Cargas", "Entradas do CSV e fórmulas de potência/corrente; valores em kW, kVA, V e A");
const loadHeaders = ["Circuito", "Quadro", "Descrição", "Fases", "V", "P saída", "η", "fp", "P inst.", "S inst.", "fd", "P dem.", "S dem.", "Ib"];
loadSheet.getRange("A3:N3").values = [loadHeaders];
header(loadSheet.getRange("A3:N3"));
loads.forEach((r, index) => {
  const row = index + 4;
  loadSheet.getRange(`A${row}:H${row}`).values = [[r.circuito, r.quadro, r.descricao, r.fases, Number(r.tensao_v), Number(r.potencia_saida_kw), Number(r.rendimento), Number(r.fator_potencia)]];
  loadSheet.getRange(`K${row}`).values = [[Number(r.fator_demanda)]];
  loadSheet.getRange(`I${row}:N${row}`).formulas = [[`=F${row}/G${row}`, `=I${row}/H${row}`, "", `=I${row}*K${row}`, `=J${row}*K${row}`, `=IF(D${row}=\"ABC\",J${row}*1000/(SQRT(3)*E${row}),J${row}*1000/E${row})`]];
});
loadSheet.getRange("A20:H20").values = [["TOTAL", "", "", "", "", "", "", ""]];
loadSheet.getRange("I20:N20").formulas = [["=SUM(I4:I19)", "=SUM(J4:J19)", "", "=SUM(L4:L19)", "=SUM(M4:M19)", ""]];
body(loadSheet.getRange("A4:N20"));
loadSheet.getRange("A20:N20").format = { fill: gray, font: { name: font, size: 10, bold: true }, borders: { preset: "all", style: "thin", color: "#A6A6A6" } };
loadSheet.getRange("E4:F19").format.numberFormat = "0.000";
loadSheet.getRange("G4:H19").format.numberFormat = "0.000";
loadSheet.getRange("I4:J20").format.numberFormat = "0.000000";
loadSheet.getRange("K4:K19").format.numberFormat = "0.00";
loadSheet.getRange("L4:M20").format.numberFormat = "0.000000";
loadSheet.getRange("N4:N19").format.numberFormat = "0.000";
loadSheet.getRange("A:A").format.columnWidth = 10;
loadSheet.getRange("B:B").format.columnWidth = 12;
loadSheet.getRange("C:C").format.columnWidth = 34;
loadSheet.getRange("D:D").format.columnWidth = 9;
loadSheet.getRange("E:N").format.columnWidth = 12;
loadSheet.getRange("C4:C19").format.wrapText = true;
loadSheet.freezePanes.freezeRows(3);

const circuitSheet = baseSheet("Circuitos", "Dimensionamento preliminar e queda combinada; rho = 0,0225 ohm.mm²/m");
circuitSheet.getRange("A3:L3").values = [["Circuito", "Quadro", "Descrição", "Ib (A)", "L (m)", "S (mm²)", "PE (mm²)", "In (A)", "Iz (A)", "dV circ. (%)", "dV aliment. (%)", "dV total (%)"]];
header(circuitSheet.getRange("A3:L3"));
loads.forEach((r, index) => {
  const row = index + 4;
  const qrow = row;
  circuitSheet.getRange(`A${row}:I${row}`).values = [[r.circuito, r.quadro, r.descricao, null, Number(r.comprimento_m), Number(r.condutor_mm2), Number(r.pe_mm2), Number(r.disjuntor_a), Number(r.iz_assumida_a)]];
  circuitSheet.getRange(`D${row}`).formulas = [[`='Quadro Cargas'!N${qrow}`]];
  circuitSheet.getRange(`J${row}:L${row}`).formulas = [[
    `=100*IF('Quadro Cargas'!D${qrow}=\"ABC\",SQRT(3),2)*0.0225*E${row}*D${row}/F${row}/'Quadro Cargas'!E${qrow}`,
    `=IF(B${row}=\"QDF-05\",Alimentadores!N5,IF(B${row}=\"QDL-05\",Alimentadores!N6,Alimentadores!N7))`,
    `=J${row}+K${row}+Alimentadores!N4`,
  ]];
});
body(circuitSheet.getRange("A4:L19"));
circuitSheet.getRange("D4:L19").format.numberFormat = "0.000";
circuitSheet.getRange("L4:L19").conditionalFormats.add("cellIs", { operator: "greaterThan", formula: 4, format: { fill: red, font: { color: "#9C0006", bold: true } } });
circuitSheet.getRange("L4:L19").conditionalFormats.add("cellIs", { operator: "lessThanOrEqual", formula: 4, format: { fill: green, font: { color: "#006100" } } });
circuitSheet.getRange("A:A").format.columnWidth = 10;
circuitSheet.getRange("B:B").format.columnWidth = 12;
circuitSheet.getRange("C:C").format.columnWidth = 34;
circuitSheet.getRange("D:L").format.columnWidth = 13;
circuitSheet.getRange("C4:C19").format.wrapText = true;
circuitSheet.freezePanes.freezeRows(3);

const feederSheet = baseSheet("Alimentadores", "Corrente de projeto, proteção, ampacidade e queda de tensão");
feederSheet.getRange("A3:P3").values = [["Alimentador", "De", "Para", "Quadro", "Sistema", "V ref.", "S dem. kVA", "Ib (A)", "L (m)", "S (mm²)", "PE (mm²)", "In (A)", "Iz (A)", "dV (%)", "Ib<=In", "In<=Iz"]];
header(feederSheet.getRange("A3:P3"));
feeders.forEach((r, index) => {
  const row = index + 4;
  feederSheet.getRange(`A${row}:G${row}`).values = [[r.alimentador, r.de, r.para, r.quadro_destino, r.fases, Number(r.tensao_v), null]];
  feederSheet.getRange(`I${row}:M${row}`).values = [[Number(r.comprimento_m), Number(r.condutores_fase_neutro_mm2), Number(r.pe_mm2), Number(r.disjuntor_a), Number(r.iz_assumida_a)]];
});
feederSheet.getRange("G4:H4").formulas = [["='Quadro Cargas'!M20", "=H5+('Quadro Cargas'!M13+'Quadro Cargas'!M15+'Quadro Cargas'!M18)*1000/220"]];
feederSheet.getRange("G5:H5").formulas = [["=SUM('Quadro Cargas'!M4:M11)", "=G5*1000/(SQRT(3)*380)"]];
feederSheet.getRange("G6:H6").formulas = [["=SUM('Quadro Cargas'!M12:M16)", "=('Quadro Cargas'!M13+'Quadro Cargas'!M15)*1000/220"]];
feederSheet.getRange("G7:H7").formulas = [["=SUM('Quadro Cargas'!M17:M19)", "='Quadro Cargas'!M17*1000/220"]];
for (let row = 4; row <= 7; row += 1) {
  feederSheet.getRange(`N${row}:P${row}`).formulas = [[
    `=100*IF(A${row}=\"AL-QDF\",SQRT(3),2)*0.0225*I${row}*H${row}/J${row}/IF(A${row}=\"AL-QDF\",380,220)`,
    `=IF(H${row}<=L${row},\"PASS\",\"FAIL\")`,
    `=IF(L${row}<=M${row},\"PASS\",\"FAIL\")`,
  ]];
}
body(feederSheet.getRange("A4:P7"));
feederSheet.getRange("G4:N7").format.numberFormat = "0.000000";
feederSheet.getRange("O4:P7").conditionalFormats.add("containsText", { text: "PASS", format: { fill: green, font: { color: "#006100", bold: true } } });
feederSheet.getRange("O4:P7").conditionalFormats.add("containsText", { text: "FAIL", format: { fill: red, font: { color: "#9C0006", bold: true } } });
feederSheet.getRange("A:A").format.columnWidth = 14;
feederSheet.getRange("B:D").format.columnWidth = 18;
feederSheet.getRange("E:P").format.columnWidth = 12;
feederSheet.freezePanes.freezeRows(3);

const cableSheet = baseSheet("Cabos", "Lista de cabos e rotas - comprimentos assumidos");
const cableHeaders = ["Cabo", "De", "Para", "Função", "Formação", "Blindagem", "L (m)", "Condutores", "Observações", "Circuito", "Rota", "dV (%)"];
cableSheet.getRange("A3:L3").values = [cableHeaders];
header(cableSheet.getRange("A3:L3"));
cables.forEach((r, index) => cableSheet.getRange(`A${index + 4}:L${index + 4}`).values = [[r.cabo, r.de, r.para, r.funcao, r.formacao, r.blindagem, Number(r.comprimento_assumido_m), r.identificacao_condutores, r.observacoes, r.circuito, r.rota, Number(r.queda_pct)]]);
body(cableSheet.getRange(`A4:L${cables.length + 3}`));
cableSheet.getRange(`G4:G${cables.length + 3}`).format.numberFormat = "0.0";
cableSheet.getRange(`L4:L${cables.length + 3}`).format.numberFormat = "0.000";
cableSheet.getRange("A:C").format.columnWidth = 15;
cableSheet.getRange("D:D").format.columnWidth = 24;
cableSheet.getRange("E:E").format.columnWidth = 30;
cableSheet.getRange("F:H").format.columnWidth = 15;
cableSheet.getRange("I:I").format.columnWidth = 34;
cableSheet.getRange("J:L").format.columnWidth = 14;
cableSheet.getRange(`D4:I${cables.length + 3}`).format.wrapText = true;
cableSheet.freezePanes.freezeRows(3);

const materialSheet = baseSheet("Materiais", "Lista consolidada de materiais - quantitativos acadêmicos");
materialSheet.getRange("A3:F3").values = [["Item", "Quantidade", "Unidade", "Descrição", "Referência", "Observações"]];
header(materialSheet.getRange("A3:F3"));
materials.forEach((r, index) => materialSheet.getRange(`A${index + 4}:F${index + 4}`).values = [[r.item, Number(r.quantidade), r.unidade, r.descricao, r.referencia, r.observacoes]]);
body(materialSheet.getRange(`A4:F${materials.length + 3}`));
materialSheet.getRange("A:A").format.columnWidth = 16;
materialSheet.getRange("B:C").format.columnWidth = 12;
materialSheet.getRange("D:D").format.columnWidth = 40;
materialSheet.getRange("E:E").format.columnWidth = 22;
materialSheet.getRange("F:F").format.columnWidth = 42;
materialSheet.getRange(`D4:F${materials.length + 3}`).format.wrapText = true;
materialSheet.freezePanes.freezeRows(3);

const audit = baseSheet("Auditoria", "Reconciliação de totais, fases, proteção, queda e referências");
audit.getRange("A5:B5").values = [["Verificação", "Resultado"]];
header(audit.getRange("A5:B5"));
audit.getRange("A6:A11").values = [["Diferença P instalada (kW)"], ["Diferença S instalada (kVA)"], ["Diferença P demandada (kW)"], ["Diferença S demandada (kVA)"], ["Falhas Ib<=In / In<=Iz"], ["Quedas combinadas > 4%"]];
audit.getRange("B6:B11").formulas = [["='Quadro Cargas'!I20-68.495248"], ["='Quadro Cargas'!J20-80.277311"], ["='Quadro Cargas'!L20-48.068716"], ["='Quadro Cargas'!M20-56.289178"], ["=COUNTIF(Alimentadores!O4:P7,\"FAIL\")"], ["=COUNTIF(Circuitos!L4:L19,\">4\")"]];
body(audit.getRange("A6:B11"));
audit.getRange("B6:B9").format.numberFormat = "0.000000";
audit.getRange("A13:B13").values = [["Fase", "Corrente demandada (A)"]];
header(audit.getRange("A13:B13"));
audit.getRange("A14:A16").values = [["A"], ["B"], ["C"]];
audit.getRange("B14:B16").formulas = [["=Alimentadores!H5+('Quadro Cargas'!M12+'Quadro Cargas'!M17)*1000/220"], ["=Alimentadores!H5+('Quadro Cargas'!M13+'Quadro Cargas'!M15+'Quadro Cargas'!M18)*1000/220"], ["=Alimentadores!H5+('Quadro Cargas'!M14+'Quadro Cargas'!M16+'Quadro Cargas'!M19)*1000/220"]];
audit.getRange("A18").values = [["Desequilíbrio (%)"]];
audit.getRange("B18").formulas = [["=(MAX(B14:B16)-MIN(B14:B16))/AVERAGE(B14:B16)*100"]];
body(audit.getRange("A14:B18"));
audit.getRange("B14:B18").format.numberFormat = "0.000000";
audit.getRange("D5:E5").values = [["Critério", "Status"]];
header(audit.getRange("D5:E5"));
audit.getRange("D6:D11").values = [["Totais reconciliados"], ["Proteção dos alimentadores"], ["Queda combinada"], ["Desequilíbrio <= 5%"], ["16 circuitos"], ["4 alimentadores"]];
audit.getRange("E6:E11").formulas = [["=IF(MAX(ABS(B6),ABS(B7),ABS(B8),ABS(B9))<0.00001,\"PASS\",\"FAIL\")"], ["=IF(B10=0,\"PASS\",\"FAIL\")"], ["=IF(B11=0,\"PASS\",\"FAIL\")"], ["=IF(B18<=5,\"PASS\",\"FAIL\")"], ["=IF(COUNTA('Quadro Cargas'!A4:A19)=16,\"PASS\",\"FAIL\")"], ["=IF(COUNTA(Alimentadores!A4:A7)=4,\"PASS\",\"FAIL\")"]];
body(audit.getRange("D6:E11"));
audit.getRange("E6:E11").conditionalFormats.add("containsText", { text: "PASS", format: { fill: green, font: { color: "#006100", bold: true } } });
audit.getRange("E6:E11").conditionalFormats.add("containsText", { text: "FAIL", format: { fill: red, font: { color: "#9C0006", bold: true } } });
audit.getRange("A:A").format.columnWidth = 34;
audit.getRange("B:B").format.columnWidth = 20;
audit.getRange("C:C").format.columnWidth = 3;
audit.getRange("D:D").format.columnWidth = 30;
audit.getRange("E:E").format.columnWidth = 14;
audit.freezePanes.freezeRows(5);

wb.recalculate();

const keyRanges = ["Resumo!A5:H18", "Quadro Cargas!A3:N20", "Circuitos!A3:L19", "Alimentadores!A3:P7", "Auditoria!A5:E18"];
const inspectionParts = [];
for (const range of keyRanges) {
  const result = await wb.inspect({ kind: "table", range, include: "values,formulas", tableMaxRows: 30, tableMaxCols: 18 });
  inspectionParts.push(result.ndjson);
}
const inspection = inspectionParts.join("\n");
const errorResult = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
const errors = errorResult.ndjson;
await fs.writeFile(path.join(root, "work", "spreadsheet-p05", "inspection.ndjson"), `${inspection}\n${errors}\n`, "utf8");

for (const name of ["Resumo", "Quadro Cargas", "Circuitos", "Alimentadores", "Cabos", "Materiais", "Auditoria"]) {
  const preview = await wb.render({ sheetName: name, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${name.toLowerCase().replaceAll(" ", "-")}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(path.join(project, "tabelas-projeto-05.xlsx"));
console.log(`Workbook: ${path.join(project, "tabelas-projeto-05.xlsx")}`);
console.log(`Sheets: ${wb.worksheets.items.map((sheet) => sheet.name).join(", ")}`);
