# Relatorio de ferramentas

Auditoria inicial executada em 2026-09-05, antes da criacao dos arquivos do
repositorio. Foram consultados PATH, metadados de executaveis, assinaturas,
Registro do Windows, associacoes de arquivo, programas instalados e os runtimes
fornecidos pelo Codex. Nenhum aplicativo CAD foi iniciado durante a auditoria
inicial.

## Resumo

| Ferramenta | Resultado | Versao / caminho principal | Limitacoes observadas |
|---|---|---|---|
| AutoCAD | encontrado | AutoCAD 2027, `R26.0.118.0.0`; `C:\Program Files\Autodesk\AutoCAD 2027\acad.exe` | fora do PATH; automacao headless testada pelo AcCoreConsole |
| AcCoreConsole | encontrado e testado | `26.0.118.0.0`; `C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe` | fora do PATH; abertura, auditoria, SAVEAS e reabertura concluidos |
| AutoCAD Electrical | encontrado | AutoCAD Electrical 2027, atualizacao `24.0.71.0` | interface instalada em ingles; usa o mesmo executavel-base |
| LibreCAD | nao encontrado | - | sem segunda implementacao CAD para teste cruzado |
| ODA File Converter | nao encontrado | - | nao ha conversor DWG independente |
| Inkscape | nao encontrado | - | SVG sera produzido por Matplotlib, sem teste pelo Inkscape |
| Python do sistema | encontrado | CPython 3.14.7 x64 | no momento da auditoria, nao possuia os pacotes tecnicos solicitados |
| Python do runtime Codex | encontrado | CPython 3.12.14 x64 | localizado em cache interno; nao deve ser dependencia permanente do projeto |
| ezdxf | ausente inicialmente | instalado depois no `.venv`: 1.4.4 | gera e audita DXF; nao grava DWG |
| matplotlib | ausente inicialmente | instalado depois no `.venv`: 3.11.1 | renderizacao pode diferir de um CAD em fontes e hachuras complexas |
| Pillow | runtime: 12.3.0 | `.venv`: 12.3.0 | validacao raster; nao valida semantica CAD |
| ReportLab | runtime: 4.4.9 | `.venv`: 5.0.1 | disponivel para PDFs programaticos; o template usa saida vetorial do Matplotlib |
| pypdf | runtime: 6.10.0 | `.venv`: 6.17.0 | valida estrutura e dimensoes do PDF, nao fidelidade visual |
| pdfplumber | runtime: 0.11.9 | `.venv`: 0.11.10 | extracao auxiliar; nao substitui a renderizacao |
| Poppler `pdftoppm` / `pdfinfo` | encontrado | 26.07.0 | `pdftocairo` nao esta disponivel |
| qpdf | nao encontrado | - | sem reparo ou linearizacao independente de PDF |
| Ghostscript | nao encontrado | - | sem backend PostScript alternativo |
| Git | encontrado | 2.53.0.windows.3 | identidade global ausente; usar identidade local nao roteavel |
| PowerShell | encontrado | 7.6.5 x64 | politica efetiva LocalMachine `RemoteSigned` |

## Evidencias do AutoCAD

- O executavel `acad.exe` tem assinatura Authenticode valida da Autodesk.
- O registro lista o produto base pt-BR `26.0.60.0` e a atualizacao AutoCAD
  2027.1 `26.0.118.0`.
- `accoreconsole.exe` tem a mesma versao de arquivo e assinatura valida.
- As extensoes `.dwg` e `.dxf` estao associadas ao AutoCAD 2027.
- A funcao interna `DwgConvert` foi localizada nos perfis, mas nao existe um
  `DWGConvert.exe` separado.
- ODA/Teigha, DWG TrueView, QCAD, BricsCAD e DraftSight tambem nao foram
  encontrados nas localizacoes usuais examinadas.

## Python e ambiente reproduzivel

Na auditoria inicial, o Python 3.14.7 do sistema nao importava `ezdxf`,
`matplotlib`, `pytest`, `reportlab`, `pypdf`, `pdfplumber`, `fitz`, `cairosvg` ou
`PIL`. O runtime temporario do Codex continha ReportLab, pypdf, pdfplumber e Pillow,
e passou em um smoke test totalmente em memoria de geracao, leitura e extracao de
texto PDF.

Foi criado posteriormente um `.venv` local, nao versionado, a partir do Python
3.14.7. As dependencias diretas e transitivas estao fixadas em
[`requirements.txt`](requirements.txt).
O projeto nao codifica caminhos do cache Codex; os scripts usam o interpretador
ativo e descoberta explicita de ferramentas externas.

Os sete testes automatizados passaram. O `ezdxf 1.4.4`, quando exercitado com
`numpy 2.5.2` nos casos artificiais de transformacao de blocos, emite um aviso de
depreciacao interno do NumPy; o aviso nao afeta a geracao nem a validacao desta
entrega, mas deve ser reavaliado antes de atualizar qualquer uma das dependencias.

## Ambiente do sistema

- Windows 11 Pro x64, versao 10.0.26200, build 26200.
- Volume de destino: NTFS saudavel, fora do OneDrive.
- Caminhos longos do Windows habilitados; `core.longpaths` do Git nao definido.
- Sistema de arquivos sem diferenciacao de maiusculas/minusculas.
- Cultura de interface `pt-BR`, fuso de Sao Paulo e codificacao de saida UTF-8.
- `core.autocrlf=true` no Git do runtime; [`.gitattributes`](.gitattributes) fixa
  os finais de linha relevantes.

## Capacidade e politica de formatos

- **DXF:** disponivel e principal; gerado como R2013/AC1027 verdadeiro, UTF-8 e mm.
- **SVG:** disponivel via backend vetorial Matplotlib.
- **PDF:** disponivel via backend vetorial Matplotlib; estrutura verificada por
  pypdf/pdfinfo e aparencia por rasterizacao Poppler.
- **PNG:** disponivel a 300 dpi via Matplotlib/Pillow.
- **DWG:** disponivel como derivado opcional pelo AutoCAD/AcCoreConsole. A cadeia foi
  comprovada por conversao real, assinatura, auditoria e reabertura. Renomear DXF
  para DWG continua proibido.

## Teste funcional do AutoCAD

Depois da auditoria somente leitura, o DXF definitivo foi submetido em 2026-09-05 ao
[`scripts/autocad_console.ps1`](scripts/autocad_console.ps1):

- abertura do `templates/template-a3.dxf`: `PASS`;
- comando `AUDIT`: 0 erros encontrados e 0 corrigidos;
- SHA-256 do DXF testado:
  `af5734384bbba9f68059db032425a2475cb5cedaa679f1f6bec919a1fac6edc2`;
- conversao real com `SAVEAS` pelo AcCoreConsole 26.0.118.0.0: `PASS`;
- assinatura do arquivo temporario: `AC1032` (DWG 2018);
- reabertura e nova auditoria do DWG: `PASS`, exit code 0;
- SHA-256 do DWG temporario:
  `9600158dd7ab86e2627c8843b848c1b7d44e8f70761bc4c997a6d6bd4354faa9`.

O DWG de teste permanece apenas em `work/`, diretorio ignorado, pois DXF e a fonte
principal e esta etapa nao exige distribuir DWG. Uma futura saida DWG deve conservar
o arquivo de evidencia `.dwg.validacao.json` produzido pelo script.

A cadeia completa foi executada duas vezes consecutivas. Os hashes de ambos os
DXFs, ambos os SVGs, do PDF e do PNG permaneceram identicos, comprovando a
reprodutibilidade dos artefatos com as versoes fixadas.

## Auditoria CAD do Projeto 01

Em 2026-09-05, o Autodesk AcCoreConsole 2027, versao 26.0.118.0.0, abriu e auditou
individualmente as seis fontes em `01-painel-motor-inversor/fonte/`:

- `01_diagrama_unifilar.dxf`: `PASS`;
- `02_diagrama_potencia.dxf`: `PASS`;
- `03_diagrama_comando.dxf`: `PASS`;
- `04_layout_interno_painel.dxf`: `PASS`;
- `05_diagrama_bornes.dxf`: `PASS`;
- `06_interligacoes_campo.dxf`: `PASS`.

Nenhum DWG foi produzido ou versionado para o projeto. DXF AC1027 permanece como fonte
principal; PDF, SVG e PNG sao derivados de visualizacao.

## Limitacoes permanentes

O `ezdxf` nao produz DWG e seus limites de texto dependem de metricas de fonte. A
renderizacao Matplotlib nao equivale ao motor grafico do AutoCAD. Por isso, a cadeia
combina auditoria estrutural, verificacao geometrica, abertura no AutoCAD quando
possivel, validacao dos derivados e inspecao visual humana. A ausencia de LibreCAD,
ODA e Inkscape reduz a diversidade de implementacoes testadas e deve permanecer
visivel neste relatorio.
