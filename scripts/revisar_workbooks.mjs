/** Auditoria somente leitura dos workbooks auxiliares do portfolio. */

import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

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
        "@oai/artifact-tool nao encontrado; informe --node-modules <diretorio>.",
        { cause: error },
      );
    }
    const entry = path.join(
      path.resolve(moduleRoot),
      "@oai",
      "artifact-tool",
      "dist",
      "artifact_tool.mjs",
    );
    return import(pathToFileURL(entry).href);
  }
}

function safeName(value) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

const root = path.resolve(argumentValue("--root", "."));
const outputRoot = path.join(root, "work", "revisao-workbooks");
const workbookPaths = [
  "04-controle-nivel-reservatorio/tabelas-projeto-04.xlsx",
  "05-instalacao-eletrica-industrial/tabelas-projeto-05.xlsx",
];
const { FileBlob, SpreadsheetFile } = await loadArtifactTool();
const summaries = [];
let hasFormulaErrors = false;

await fs.mkdir(outputRoot, { recursive: true });

for (const relativePath of workbookPaths) {
  const workbookPath = path.join(root, relativePath);
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
  const workbookName = path.basename(relativePath, ".xlsx");
  const workbookOutput = path.join(outputRoot, workbookName);
  await fs.mkdir(workbookOutput, { recursive: true });

  const summary = await workbook.inspect({
    kind: "workbook,sheet,table,formula",
    maxChars: 30000,
    tableMaxRows: 40,
    tableMaxCols: 24,
    tableMaxCellChars: 120,
  });
  const formulaErrors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
    options: { useRegex: true, maxResults: 500 },
    summary: "formula error scan",
  });
  await fs.writeFile(
    path.join(workbookOutput, "inspecao.ndjson"),
    `${summary.ndjson}\n${formulaErrors.ndjson}\n`,
    "utf8",
  );

  const errorLines = formulaErrors.ndjson
    .split(/\r?\n/)
    .filter((line) => /#(?:REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(line));
  hasFormulaErrors ||= errorLines.length > 0;

  const sheetNames = workbook.worksheets.items.map((sheet) => sheet.name);
  for (const sheetName of sheetNames) {
    const preview = await workbook.render({
      sheetName,
      autoCrop: "all",
      scale: 1,
      format: "png",
    });
    await fs.writeFile(
      path.join(workbookOutput, `${safeName(sheetName)}.png`),
      new Uint8Array(await preview.arrayBuffer()),
    );
  }

  summaries.push({
    path: relativePath.replaceAll("\\", "/"),
    bytes: (await fs.stat(workbookPath)).size,
    sheets: sheetNames,
    formulaErrors: errorLines.length,
  });
  console.log(
    `WORKBOOK ${relativePath} | abas=${sheetNames.length} erros_formula=${errorLines.length}`,
  );
}

await fs.writeFile(
  path.join(outputRoot, "resultado.json"),
  `${JSON.stringify({ status: hasFormulaErrors ? "FAIL" : "PASS", workbooks: summaries }, null, 2)}\n`,
  "utf8",
);
console.log(`WORKBOOK_REVIEW=${hasFormulaErrors ? "FAIL" : "PASS"}`);
if (hasFormulaErrors) process.exit(1);
