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

Os nove testes automatizados passaram. O `ezdxf 1.4.4`, quando exercitado com
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

## Auditoria CAD do Projeto 16 — 2026-11-06

As tres fontes DXF de coleta e conexao do parque eolico foram abertas e auditadas pelo
Autodesk AcCoreConsole 2027, versao de arquivo `26.0.118.0.0`, com o script
[`scripts/autocad_console.ps1`](scripts/autocad_console.ps1). As tres execucoes
retornaram `AUTOCAD_AUDIT=PASS`:

- `01_unifilar_coleta_conexao.dxf` — SHA-256 `3f141ca73bd6578aff52edbd09c9a50fb910669b16bedd298da4b17df1278389`;
- `02_layout_parque_eolico.dxf` — SHA-256 `e24440a794477ee22823f6cd80fbfc5787c8da54ec85ee5a524b58aa2a157717`;
- `03_base_calculo_interfaces.dxf` — SHA-256 `3df5aa9a6ed7ac790fd9a0aceb58736cfb78c13858099795754d3cf1cecf8bf7`.

O resultado comprova abertura e auditoria estrutural pelo AutoCAD. Não constitui
validação de projeto executivo, estudos de conexão, desempenho ou conformidade.

## Auditoria CAD do Projeto 17 — 2026-11-06

As tres fontes DXF da automacao digital da subestacao foram abertas e auditadas pelo
Autodesk AcCoreConsole 2027, versao de arquivo `26.0.118.0.0`, usando
[`scripts/autocad_console.ps1`](scripts/autocad_console.ps1). As tres execucoes
retornaram `AUTOCAD_AUDIT=PASS`:

- `01_unifilar_sas_ied.dxf` — SHA-256 `2c2920b3388a2a36febcc4b471d9aac3a0b0cc123c8f50d654d67ca69d77757e`;
- `02_rede_iec61850.dxf` — SHA-256 `7e20ca36454d3550bde900ee3576ee517e556224756987a8f4b396ccc84b0832`;
- `03_matriz_goose_testes.dxf` — SHA-256 `26ac6f7b7480e3dda32909c11a947bedfc2c1129df17e7ad68e9495687ab8f7e`.

A auditoria confirma abertura e estrutura CAD. Nenhum ensaio IEC 61850, FAT/SAT,
interoperabilidade, latencia ou funcao de protecao foi executado.

## Auditoria CAD do Projeto 18 — 2026-11-06

As tres fontes DXF da compensacao de reativos e qualidade de energia foram abertas
e auditadas pelo Autodesk AcCoreConsole 2027, versao `26.0.118.0.0`. As execucoes
retornaram `AUTOCAD_AUDIT=PASS`:

- `01_unifilar_compensacao_reativos.dxf` — SHA-256 `d3cfe9892307663e027ce4e10817107df7d87232cb69020d645ead6582e83605`;
- `02_memoria_correcao_fator_potencia.dxf` — SHA-256 `d709d54a12d25d5b544cfe10ddb0b80314ed5b75e964eeb9b516d84879ec57c6`;
- `03_medicao_controle_harmonicos.dxf` — SHA-256 `cbb78cb2452ab58a0217ab51c24c1fd56586acd3931b0d4806ae73080cedbc74`.

A auditoria comprova abertura e estrutura CAD. Nenhuma medicao de campo, selecao de
filtro, estudo de ressonancia ou verificacao de limites foi realizada.

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

## Auditoria CAD do Projeto 02

Em 2026-09-05, o Autodesk AcCoreConsole 2027, versao 26.0.118.0.0, abriu e auditou
individualmente as oito fontes em `02-projeto-eletrico-residencial/fonte/`:

- `01_planta_arquitetonica.dxf`: `PASS`;
- `02_planta_iluminacao.dxf`: `PASS`;
- `03_planta_tomadas.dxf`: `PASS`;
- `04_planta_eletrodutos.dxf`: `PASS`;
- `05_diagrama_unifilar.dxf`: `PASS`;
- `06_quadro_distribuicao.dxf`: `PASS`;
- `07_quadro_cargas.dxf`: `PASS`;
- `08_detalhes_aterramento.dxf`: `PASS`.

Poppler `pdftoppm` 26.07.0 rasterizou os oito PDFs finais para a inspeção visual. Os
SVGs foram abertos em Chromium e comparados com os PNGs de 300 dpi. Nenhum DWG foi
produzido ou versionado; DXF AC1027 permanece como fonte principal.

## Auditoria CAD do Projeto 03

Em 2026-09-06, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as oito fontes em `03-painel-automacao-clp/fonte/`:

- `01_arquitetura_automacao.dxf`: `PASS`;
- `02_alimentacao_24v.dxf`: `PASS`;
- `03_entradas_clp.dxf`: `PASS`;
- `04_saidas_clp.dxf`: `PASS`;
- `05_diagrama_comando.dxf`: `PASS`;
- `06_layout_painel.dxf`: `PASS`;
- `07_diagrama_bornes.dxf`: `PASS`;
- `08_interligacoes_campo.dxf`: `PASS`.

Poppler `pdftoppm` 26.07.0 rasterizou os oito PDFs finais; os oito SVGs foram abertos
em Google Chrome/Chromium headless e comparados com os PNGs de 300 dpi. A primeira
revisão visual detectou sobreposição entre as tabelas X2 e X4 na prancha 07; a origem
foi corrigida, todos os derivados foram regenerados e a segunda inspeção foi aprovada.
O validador específico aprovou 129 verificações lógicas; a validação estrita do
portfólio aprovou 121.899 verificações, sem erros ou avisos. Nove testes automatizados
passaram. Uma nova geração manteve os hashes de todos os 32 artefatos do projeto
(oito DXFs e 24 derivados), confirmando reprodutibilidade no ambiente registrado.
Nenhum DWG foi produzido ou versionado para o projeto. DXF AC1027 permanece como fonte
principal.

## Auditoria CAD do Projeto 04

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as seis fontes em `04-controle-nivel-reservatorio/fonte/`:

- `01_fluxograma_processo.dxf`: `PASS`;
- `02_pid_instrumentacao.dxf`: `PASS`;
- `03_malha_controle.dxf`: `PASS`;
- `04_diagrama_eletrico.dxf`: `PASS`;
- `05_interligacoes_instrumentos.dxf`: `PASS`;
- `06_layout_sistema.dxf`: `PASS`.

O validador específico aprovou 169 verificações de I/O, tags, tabelas, sentido da
malha e permissivos. Poppler `pdftoppm` 26.07.0 reabriu e rasterizou os seis PDFs A3;
Google Chrome 152.0.7977.77 abriu os seis SVGs; os PNGs de produção foram inspecionados
em 300 dpi. Duas colisões visuais foram corrigidas na fonte e a segunda inspeção foi
aprovada. As seis abas do workbook técnico também foram renderizadas e examinadas.

O fluxo usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. Nenhum
DWG foi produzido ou versionado; DXF AC1027 permanece como fonte principal. A
validação estrita aprovou 142.949 verificações, sem erros ou avisos; nove testes
automatizados passaram. Uma nova geração manteve hashes idênticos para os 24
artefatos do projeto (seis DXFs e 18 derivados), comprovando reprodutibilidade.

## Auditoria CAD do Projeto 05

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as sete fontes em `05-instalacao-eletrica-industrial/fonte/`:

- `01_layout_industrial.dxf`: `PASS`;
- `02_distribuicao_forca.dxf`: `PASS`;
- `03_distribuicao_iluminacao.dxf`: `PASS`;
- `04_eletrocalhas_rotas.dxf`: `PASS`;
- `05_diagrama_unifilar.dxf`: `PASS`;
- `06_quadro_cargas.dxf`: `PASS`;
- `07_detalhes_instalacao.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os sete PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome 152.0.7977.77 abriu os sete SVGs; os PNGs de
produção foram inspecionados em 300 dpi. A primeira revisão levou a ajustes de rótulos,
folgas do unifilar e intervalo visual do workbook; a segunda inspeção foi aprovada. As
sete abas do workbook técnico foram renderizadas, examinadas e não apresentaram erros
de fórmula. Na conclusão original, o gerador usava `@oai/artifact-tool` 2.8.59.

O fluxo CAD usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 294 verificações de somas, fases, proteções, quedas,
referências e listas. A validação estrita aprovou 200.489 verificações, sem erros ou
avisos. Uma reconstrução completa manteve hashes idênticos para os 28 artefatos CAD do
projeto (sete DXFs e 21 derivados). Nenhum DWG foi produzido ou versionado; DXF AC1027
permanece como fonte principal.

## Auditoria CAD do Projeto 06

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as sete fontes em `06-centro-controle-motores/fonte/`:

- `01_diagrama_unifilar_ccm.dxf`: `PASS`;
- `02_partida_direta.dxf`: `PASS`;
- `03_partida_reversora.dxf`: `PASS`;
- `04_acionamento_inversor.dxf`: `PASS`;
- `05_layout_ccm.dxf`: `PASS`;
- `06_diagrama_bornes.dxf`: `PASS`;
- `07_lista_cabos.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os sete PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome abriu os sete SVGs em modo headless; os PNGs de
produção foram inspecionados em 300 dpi. A primeira revisão levou a correções no
símbolo de motor, na separação dos condutores da partida direta, na arquitetura de
potência da reversão, nas folgas do unifilar e na altura da tabela de cabos. A segunda
inspeção foi aprovada nos 21 derivados.

O fluxo CAD usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 828 verificações de cargas, alimentador, quedas, cabos,
bornes, materiais, intertravamentos, parada comum, STO e ausência de rearme automático.
A validação estrita do portfólio aprovou 238.890 verificações sem erros ou avisos, e
nove testes automatizados passaram. Uma nova geração manteve hashes idênticos para os
28 artefatos CAD do projeto. Nenhum DWG foi produzido ou versionado; DXF AC1027
permanece como fonte principal.

## Auditoria CAD do Projeto 07

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as oito fontes em `07-arquitetura-veiculo-eletrico/fonte/`:

- `01_arquitetura_geral.dxf`: `PASS`;
- `02_circuito_alta_tensao.dxf`: `PASS`;
- `03_circuito_baixa_tensao.dxf`: `PASS`;
- `04_pre_carga_contatores.dxf`: `PASS`;
- `05_inversor_motor.dxf`: `PASS`;
- `06_sensores_controle.dxf`: `PASS`;
- `07_rede_comunicacao.dxf`: `PASS`;
- `08_layout_componentes.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os oito PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome 152.0.7977.83 abriu os oito SVGs em modo
headless; os oito PNGs de produção foram inspecionados em 300 dpi. A primeira revisão
levou a correções na conexão do CC-CC, na cadeia física de habilitação, no estágio
trifásico e na realimentação FOC, no agrupamento dos sensores e nas folgas da tabela
CAN. Após regeneração, a segunda inspeção foi aprovada nos 24 derivados.

O fluxo CAD usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 4.224 verificações de parâmetros, cálculos, sinais,
cabos, materiais, mensagens CAN, pré-carga, habilitação de torque, conteúdo dos DXFs
e separação entre fatos, premissas e propostas. A validação estrita final aprovou 272.953
verificações sem erros ou avisos. Uma nova geração manteve hashes idênticos nos 32
artefatos CAD do projeto, e nove testes automatizados passaram. Nenhum DWG foi
produzido ou versionado; DXF AC1027 permanece como fonte principal.

### Revisão 02 do Projeto 07 — 2026-11-05

A P07-09 acrescenta uma matriz de dez eventos e rastreia sinais, estados, reações
propostas e lacunas de validação. Não declara HARA, FMEA, ASIL, diagnóstico implementado
ou desligamento seguro. As oito folhas existentes foram reemitidas em revisão 02 e
renumeradas de `NN/08` para `NN/09`.

O validador específico aprovou 4.247 verificações. O AcCoreConsole 2027 abriu e auditou
as nove fontes, `PASS` em 9/9. P07-09 foi conferida em PNG de produção, PDF rasterizado
a 150 dpi e na folha de contato das nove pranchas. O revisor consolidado confirmou 12
projetos, 93 pranchas, 372 arquivos gráficos e 65 CSVs; a validação estrita aprovou
496.492 verificações sem erros nem avisos. A inspeção visual dos SVGs no navegador
continua pendente da autorização do usuário.

## Auditoria CAD e visual do Projeto 08

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as seis fontes em `08-sistema-fotovoltaico/fonte/`:

- `01_disposicao_modulos.dxf`: `PASS`;
- `02_diagrama_unifilar_cc.dxf`: `PASS`;
- `03_diagrama_unifilar_ca.dxf`: `PASS`;
- `04_string_box.dxf`: `PASS`;
- `05_aterramento.dxf`: `PASS`;
- `06_layout_equipamentos.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os seis PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome 152.0.7977.83 abriu os seis SVGs em modo
headless; os seis PNGs de produção foram inspecionados em 300 dpi. A primeira revisão
levou a correções na legenda dos módulos, no rótulo de PE, nas descidas dos DPS, nas
folgas do aterramento e nas rotas CA/PE. Após regeneração, a segunda inspeção foi
aprovada nos 18 derivados.

O fluxo CAD usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 8.036 verificações de parâmetros, módulos, strings,
proteções, cabos, materiais, cálculos, extremos ambientais e conteúdo das seis
pranchas. A validação estrita integrada aprovou 297.598 verificações sem erros ou
avisos. Uma nova geração manteve hashes idênticos nos 24 artefatos CAD do projeto, e
nove testes automatizados passaram. Nenhum DWG foi produzido ou versionado; DXF
AC1027 permanece como fonte principal.

Para o estado normativo, foram consultadas em 2026-09-09 as fontes oficiais da ANEEL
sobre MMGD, Resolução Normativa 1.000/2021 alterada pela 1.059/2023 e Módulo 3 do
PRODIST; a Lei 14.300/2022 no Planalto; o catálogo da ABNT para NBR 16690:2019,
NBR 5410:2004 versão corrigida 2008 e série NBR 5419:2026; o Inmetro para as Portarias
140/2022 e 515/2023; e o catálogo IEC para 60364-7-712:2025, 62548-1:2023+A1:2025,
61643-31:2018/COR1:2022, 62852:2014+A1:2020 e 62446-1:2016+A1:2018. As referências
são critérios de consulta; sua aplicação executiva permanece condicionada à edição
vigente, ao acesso integral às normas e à responsabilidade profissional.

## Revisão 02 do Projeto 08 — 2026-11-05

A revisão ampliou o P08 para sete pranchas e acrescentou P08-07, uma comparação
paramétrica da energia anual para 6,60 kWp. A grade de 12 cenários usa HSP de 3 a
6 h/dia e PR de 0,70 a 0,86; seus extremos calculados são 5.058,900 e 12.430,440
kWh/ano. São combinações matemáticas escolhidas para estudo, sem dados meteorológicos,
probabilidade ou previsão de um local. O caso didático existente permanece em
9.770,904 kWh/ano (HSP 5,2; PR 0,78).

O validador específico aprovou 8.073 verificações, incluindo as 13 linhas do CSV e as
fórmulas da grade. O AutoCAD AcCoreConsole 2027 abriu e auditou os sete DXFs, `PASS`
em 7/7. As sete PNGs de produção e os sete PDFs rasterizados a 150 dpi foram
inspecionados; a composição das sete folhas também foi conferida. A validação estrita
integrada do portfólio aprovou 496.492 verificações, sem erros ou avisos; o revisor
consolidado confirmou 12 projetos, 93 pranchas, 372 derivados e 65 CSVs, com similaridade
mínima PDF/PNG de 0,9842. A inspeção visual em navegador dos SVGs da revisão 02 aguarda
autorização do usuário. Nenhum DWG foi produzido; DXF AC1027 permanece como fonte.

## Auditoria CAD e visual do Projeto 09

Em 2026-09-09, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as seis fontes em `09-fonte-bancada/fonte/`:

- `01_diagrama_blocos.dxf`: `PASS`;
- `02_diagrama_eletrico.dxf`: `PASS`;
- `03_painel_frontal.dxf`: `PASS`;
- `04_layout_interno.dxf`: `PASS`;
- `05_detalhes_mecanicos.dxf`: `PASS`;
- `06_interligacoes.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os seis PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome 152.0.7977.83 abriu os seis SVGs em modo
headless; os seis PNGs de produção foram inspecionados em 300 dpi. A primeira revisão
levou à correção de uma linha sobre o quadro de limites, entidades duplicadas no
painel frontal, cotas junto às legendas, notas sobre tabelas e um rótulo atravessado
por condutor. Após regeneração, a inspeção final foi aprovada nos 18 derivados.

O fluxo CAD usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 18.554 verificações de parâmetros, cálculos, listas,
extremos de tensão e frequência de entrada, grade tensão-corrente de saída, conteúdo
e metadados dos seis DXFs. A validação estrita integrada aprovou 330.795 verificações,
sem erros ou avisos, e nove testes automatizados passaram. Uma reconstrução
consecutiva manteve hashes SHA-256 idênticos para os 24 artefatos do projeto. Nenhum
DWG foi produzido ou versionado; DXF AC1027 permanece como fonte principal.

Para o estado normativo, foram consultados em 2026-09-09 o catálogo oficial da IEC
para IEC 61010-1:2010+A1:2016, IEC 60445:2021, IEC 60320-1:2021,
IEC 61558-2-16:2021 e IEC 60529, além da página oficial da NR-10 no Ministério do
Trabalho e Emprego. Essas referências orientam a análise acadêmica e não constituem
certificação, ensaio ou liberação do equipamento para fabricação.

## Auditoria CAD e visual do Projeto 10

Em 2026-09-10, o Autodesk AcCoreConsole 2027, versão 26.0.118.0.0, abriu e auditou
individualmente as seis fontes em `10-rede-instrumentacao-industrial/fonte/`:

- `01_arquitetura_rede.dxf`: `PASS`;
- `02_diagrama_instrumentacao.dxf`: `PASS`;
- `03_diagrama_interligacao.dxf`: `PASS`;
- `04_topologia_comunicacao.dxf`: `PASS`;
- `05_painel_instrumentacao.dxf`: `PASS`;
- `06_lista_instrumentos.dxf`: `PASS`.

Poppler `pdfinfo` e `pdftoppm` 26.07.0 reabriram os seis PDFs A3 de uma página e os
rasterizaram a 150 dpi. Google Chrome 152.0.7977.83 abriu os seis SVGs em modo
headless; os seis PNGs de produção foram examinados a 300 dpi. A primeira revisão
detectou a invasão de uma tabela sobre a legenda/carimbo e o contato entre uma faixa
de cálculo e uma tabela. A posição dos elementos foi corrigida na fonte, a cor da
comunicação foi alinhada à legenda e a segunda inspeção aprovou os 18 derivados.

O fluxo usou ezdxf 1.4.4, Matplotlib 3.11.1, Pillow 12.3.0 e pypdf 6.17.0. O
validador específico aprovou 64.207 verificações de documentos, tags, I/O, cabos,
bornes, endereços, balanço 24 Vcc, escalas analógicas, estrutura CAD e derivados.
O validador estrito integrado aprovou 370.524 verificações, sem erros ou avisos, e
os nove testes automatizados passaram. Uma reconstrução consecutiva preservou os
hashes SHA-256 dos 24 artefatos do projeto (seis DXFs e 18 derivados).
Nenhum DWG foi produzido ou versionado; DXF AC1027 permanece como fonte principal.

Foram consultadas em 2026-09-10 as páginas oficiais da IEC para IEC 60381-1:1982,
IEC 61326-1:2020, IEC 61131-2:2017, IEC 61158-2:2023 e IEC 60445:2021, a página da
ISA para ANSI/ISA-5.1-2024 e a página oficial da NR-10 no Ministério do Trabalho e
Emprego. As referências orientam a análise acadêmica e não representam certificação
ou liberação executiva.

## Limitacoes permanentes

O `ezdxf` nao produz DWG e seus limites de texto dependem de metricas de fonte. A
renderizacao Matplotlib nao equivale ao motor grafico do AutoCAD. Por isso, a cadeia
combina auditoria estrutural, verificacao geometrica, abertura no AutoCAD quando
possivel, validacao dos derivados e inspecao visual humana. A ausencia de LibreCAD,
ODA e Inkscape reduz a diversidade de implementacoes testadas e deve permanecer
visivel neste relatorio.

## Revisão consolidada de 2026-09-10

As ferramentas críticas foram verificadas novamente durante a revisão completa do
portfólio:

- AutoCAD 2027 `R26.0.118.0.0` e AcCoreConsole `26.0.118.0.0`;
- Python 3.14.7, ezdxf 1.4.4, Matplotlib 3.11.1 e Pillow 12.3.0;
- pypdf 6.17.0, pdfplumber 0.11.10, PDFium 5.13.0 e Poppler 26.07.0;
- Microsoft Edge 152.0.4191.66 e Google Chrome 152.0.7977.83;
- Node.js 24.19.0 e `@oai/artifact-tool` 2.8.59, usados na revisão visual registrada;
- Git 2.53.0.windows.3 e PowerShell 7.6.5.

O AcCoreConsole abriu e auditou 70/70 DXFs. O Edge abriu e rasterizou 70/70 SVGs;
PDFium reabriu os 68 PDFs de projeto e a comparação com os PNGs teve similaridade
mínima de 0,9842. Os dois workbooks, com 13 abas ao todo, foram importados sem erros
de fórmula. LibreCAD, ODA File Converter e Inkscape continuam ausentes.

Os detalhes e comandos reproduzíveis estão no
[relatório de validação consolidada](relatorio-validacao.md).

## Preparação para publicação pública em 2026-09-10

O pacote `@oai/artifact-tool` não está disponível no registro público npm. Para não
publicar uma dependência inacessível, o gerador do workbook P05 e o auditor dos dois
workbooks foram migrados para Python com `openpyxl 3.1.5` e `et-xmlfile 2.0.0`, ambos
disponíveis publicamente sob licença MIT. O `package.json` deixou de ser necessário.

O workbook P05 regenerado preservou sete abas e 209 fórmulas, passou nas 294
verificações específicas e foi novamente renderizado e inspecionado com a ferramenta
disponível no ambiente de revisão. Duas execuções independentes do novo gerador
produziram o mesmo SHA-256 após a normalização dos metadados internos.

## Revisão 02 do Projeto 01 — 2026-11-05

O P01 passou a sete folhas; as seis fontes anteriores foram reemitidas em `/07` e
revisão gráfica 02. A nova P01-07 apresenta a cadeia QDG–Q0–Q1–VFD1–M1 e organiza em
sete linhas os dados necessários para revisar Icc, seccionador, disjuntor, VFD/motor,
fonte auxiliar, DPS e cabos. O CSV vinculado mantém cada premissa, dado substituto e
análise pendente. A comparação aritmética 10 kA/5 kA está explicitamente marcada como
insuficiente para provar coordenação.

O AcCoreConsole do AutoCAD 2027 auditou 7/7 DXFs. P01-07 foi conferida no PNG de
produção a 300 dpi, em PDF rasterizado pelo Poppler a 150 dpi e na folha de contato das
sete páginas. Não observei corte ou colisão relevante. O revisor atribuiu similaridade
PDF/PNG de 0,987268 à nova folha. A validação estrita integrada aprovou 501.282
verificações, sem erros nem avisos; a revisão consolidada aprovou 12 projetos, 94
pranchas, 376 arquivos gráficos e 66 CSVs, com similaridade mínima de 0,9842.

A inspeção visual dos SVGs no navegador segue pendente da autorização do usuário. A
revisão confirma integridade CAD e apresentação, mas não dimensionamento ou coordenação
elétrica para execução.

## Atualização P01-08 — 2026-11-05

A prancha P01-08 acrescenta um plano de verificação com cinco etapas e doze pontos de
fechamento, rastreando dados, evidências e estado. A matriz vinculada mantém todos os
itens como `NÃO EXECUTADO`; não há resultados de campo nem aprovação implícita. O
gerador valida o cabeçalho, a unicidade dos códigos e as doze linhas completas do CSV.

As oito fontes DXF foram regeneradas deterministicamente: uma segunda execução
reproduziu os oito SHA-256. O AutoCAD AcCoreConsole 2027 abriu e auditou 8/8 fontes. As
oito folhas foram renderizadas em PDF, SVG e PNG; o contato atualizado do P01 foi
conferido e P01-08 foi examinada integralmente no PNG de produção a 300 dpi e em raster
independente do PDF, feito pelo Poppler a 150 dpi. Não observei cortes ou colisões
relevantes na nova folha; sua similaridade PDF/PNG foi 0,984095.

A validação estrita integrada passou por 509.704 verificações, sem erros nem avisos.
O revisor confirmou 12 projetos, 95 pranchas, 380 arquivos gráficos e 67 CSVs; a
similaridade mínima PDF/PNG foi 0,984095. A inspeção visual dos SVGs em navegador
continua pendente de autorização.

## Atualização P02-09 — 2026-11-05

A revisão gráfica 02 amplia o P02 para nove folhas e acrescenta uma rastreabilidade
por ambiente ligada à lista de pontos e ao quadro de cargas. O CSV declara como
`PREMISSA` dimensões, usos, equipamentos ainda não selecionados e potências atribuídas;
os 19 pontos somam 15.548,913 VA em oito ambientes e 75 m². O validador específico
passou em 63 verificações, sem erros.

O AutoCAD AcCoreConsole 2027 abriu e auditou os nove DXFs. A regeneração repetida
reproduziu os nove hashes SHA-256. As nove folhas foram renderizadas em PDF, SVG e PNG;
conferi o contato atualizado, P02-01 no PNG integral a 300 dpi e P02-09 no PNG integral
e PDF rasterizado independentemente pelo Poppler a 150 dpi. A similaridade mínima
PDF/PNG do projeto foi 0,986556. O navegador não foi usado para inspecionar os SVGs
desta revisão; a etapa aguarda autorização.

A validação estrita integrada passou por 521.224 verificações, sem erros nem avisos.
O revisor confirmou 12 projetos, 96 pranchas, 384 arquivos gráficos e 68 CSVs; a
similaridade mínima PDF/PNG do portfólio foi 0,984095.

## Atualização P03-10 — 2026-11-05

O Projeto 03 passou a dez pranchas na revisão 03. A nova folha organiza doze pontos de
verificação para processo, hardware, alimentação, I/O, permissivos, sequência, falhas,
rearme e entrega. Todos permanecem `NÃO EXECUTADO`; as premissas de tempo precisam de
confirmação e a resposta a sensor incoerente com bomba em marcha continua pendente.

O validador lógico específico passou em 232 verificações. O AutoCAD AcCoreConsole 2027
abriu e auditou 10/10 DXFs. Conferi a folha de contato P03 com dez folhas, o PNG de
produção a 300 dpi e o PDF rasterizado pelo Poppler a 150 dpi; não observei cortes na
tabela, carimbo ou aviso. Os SVGs não foram inspecionados em navegador nesta etapa.

A reconstrução completa do portfólio e a validação estrita passaram por 529.645
verificações, sem erros nem avisos. O revisor confirmou 12 projetos, 97 pranchas, 388
arquivos gráficos e 69 CSVs, com similaridade mínima PDF/PNG de 0,984061.

## Revisão 05 do Projeto 10 — 2026-11-06

O AcCoreConsole 2027 abriu e auditou 10/10 DXFs P10. A folha nova P10-10 foi
renderizada em PDF/SVG/PNG; Poppler `pdftoppm` 26.07.0 rasterizou o PDF
independentemente a 150 dpi e a inspeção não encontrou cortes ou colisões. O PNG de
produção a 300 dpi e o contato das dez folhas também foram conferidos. O validador
específico passou em 64.395 verificações; o estrito passou em 613.579 sem erros ou
avisos. O revisor integrado confirmou 12 projetos, 105 pranchas, 420 arquivos
gráficos e 72 CSVs, com similaridade mínima de 0,981493; P10-10 obteve 0,988205.
Edge/Chrome não foram usados para inspeção visual dos SVGs; essa etapa segue
aguardando autorização do usuário.

## Atualização P01-09 — revisão 04 — 2026-11-06

A nova sequência operacional foi gerada em `09_sequencia_operacional_estados.dxf`, com
`sequencia-estados.csv` como fonte dos estados e eventos. A segunda geração do P01
reproduziu os nove SHA-256. O AutoCAD AcCoreConsole 2027 abriu e auditou 9/9 DXFs.

O PNG de produção, o contato das nove folhas e a rasterização independente do PDF pelo
Poppler a 150 dpi foram inspecionados; não encontrei cortes ou colisões. A similaridade
PDF/PNG de P01-09 foi 0,990330. A revisão integrada passou: 12 projetos, 114 folhas,
456 arquivos gráficos, 77 CSVs e similaridade mínima de 0,981493. O validador estrito
passou por 663.880 verificações, sem erros ou avisos. A inspeção de SVGs no navegador
continua aguardando autorização.

## Auditoria CAD — P05 revisão 05, P11/P12 revisão 04 — 2026-11-06

O AutoCAD AcCoreConsole 2027 (26.0.118.0.0) abriu e auditou os 26 DXFs dos projetos
P05, P11 e P12. A execução em lote registrou zero erros encontrados e zero corrigidos.
Os geradores P11/P12 agora gravam DXF em LF, conforme `.gitattributes`; os 26 hashes de
origem no manifesto conferem com os arquivos que serão versionados.
Os três renders de produção P05-01, P11-02 e P12-06 foram comparados a PDFs rasterizados
independentemente pelo `pypdfium2`; também conferi o PNG integral e o contato do
respectivo conjunto. Não encontrei cortes ou colisões relevantes.

P05-01 obteve similaridade PDF/PNG de 0,992284; P11-02, 0,990676; P12-06, 0,991573.
Os validadores específicos passaram (P05: 443 verificações; P11: oito folhas, 23
materiais, 17 cabos e 22 entradas pendentes; P12: nove folhas, nove eventos, quatro
alimentadores QCE, 24 materiais e 15 cabos). A revisão integrada confirmou 12 projetos,
114 folhas, 456 arquivos gráficos e 77 CSVs; validação estrita: 668.075 verificações,
zero erros e zero avisos. Essas verificações não demonstram dimensionamento ou aptidão
executiva. A inspeção de SVGs no navegador continua aguardando autorização.

## P09 revisão 05 — detalhamento mecânico — 2026-11-06

P09-05 passou a desenhar cada registro de `lista-recortes.csv`; a geometria é gerada
diretamente dos centros, dimensões e classificações do CSV. A prancha separa dez itens
frontais e seis traseiros, incluindo LED-CV, LED-CC e FAN1-H1 a FAN1-H4. A origem de
coordenadas, a unidade e o caráter proposto aparecem na folha; materiais, tolerâncias,
acabamento e processo continuam indefinidos.

O validador específico passou em 18.916 verificações. O AcCoreConsole 2027 abriu/auditou
10/10 DXFs P09 com resultado `PASS`. P09-05 foi conferida no PNG a 300 dpi, no PDF
rasterizado independentemente pelo Poppler 26.07.0 a 150 dpi e no contato das dez folhas.
Não observei cortes ou colisões relevantes. O revisor integrado aprovou 12 projetos,
114 folhas, 456 arquivos gráficos e 77 CSVs; validação estrita: 673.894 verificações,
zero erros e zero avisos. O teste visual de SVGs no navegador ainda aguarda autorização;
simulação elétrica não foi executada.

## P08 revisão 04 — rotas do sistema fotovoltaico — 2026-11-06

A legenda de P08-01 agora corresponde à camada CC turquesa. P08-06 separa os dois
percursos de string, associa cada saída ao MPPT correto, identifica rotas CA/PE e
registra a comunicação opcional sem inventar um trajeto físico. Os comprimentos são
marcados como assumidos. O validador P08 passou em 8.131 verificações; o AcCoreConsole
2027 auditou 8/8 DXFs. As folhas P08-01 e P08-06 foram conferidas em PNG a 300 dpi e
PDF A3 rasterizado pelo Poppler a 150 dpi. A revisão integrada confirmou 12 projetos,
114 folhas, 456 arquivos gráficos e 77 CSVs; P08-06 teve similaridade de 0,989889. A
validação estrita passou em 674.521 verificações, sem erros ou avisos. A inspeção SVG
em navegador continua aguardando autorização do usuário.

## Projeto P19 — alimentação HVSC no cais — 2026-11-06

Foram geradas três pranchas A3 sobre o fornecimento de energia do terminal ao navio:
unifilar, implantação esquemática e sequência/intertravamentos conceituais. O validador
P19 passou em 62 verificações. A repetição do gerador reproduziu os três SHA-256 e o
AutoCAD AcCoreConsole 2027 (26.0.118.0.0) abriu/auditou 3/3 DXFs com `PASS`:

- `01_unifilar_hvsc_cais.dxf` — `25dbe1656124f89b350aebee39d81e07b868d0414e46dd2544fd93f5a65a5828`
- `02_implantacao_eletrica_cais.dxf` — `97f9edb2b6c01043f6eacb9e79d20f569e022fc911d05cdbacf855e2b111fd7b`
- `03_sequencia_intertravamentos_hvsc.dxf` — `d495500a1f4c73c0b8f82b5e33f2955bc9abf1fac89aa50e2b08ecbdf1018aeb`

Os três PNGs de produção (4960 × 3507 px, 300 dpi) foram inspecionados. PDFium
rasterizou os PDFs independentemente em 4961 × 3508 px; a comparação na área comum
resultou em similaridades de 0,992812, 0,993874 e 0,989953. A validação estrita do
portfólio passou em 760.998 verificações, sem erros ou avisos. As premissas de 13,8/6,6
kV e 3,2 MVA são didáticas; nenhum estudo de compatibilidade com navio, proteção,
aterramento, cabo, intertravamento ou operação foi executado. A inspeção no navegador
nativo permanece aguardando autorização do usuário.

## Projeto P20 — tração ferroviária CC 750 V — 2026-11-06

Foram produzidas três folhas A3 para uma subestação retificadora e alimentação por
terceiro trilho: unifilar, zonas de alimentação/retorno e matriz conceitual de
proteção/supervisão. A premissa de 750 Vcc e 1 MW resulta em 1.333,3 A pela conta
ideal P/V; isso não dimensiona os equipamentos ou a instalação.

O validador específico passou em 57 verificações. A repetição do gerador manteve os
hashes dos três DXFs já auditados pelo AutoCAD AcCoreConsole 2027 (26.0.118.0.0),
que os abriu e auditou com `PASS`:

- `01_unifilar_subestacao_tracao.dxf` — `158f9b2b240f0abf90a4d562625bd3c731e6bc1e741673ff401fd73b2643ec50`
- `02_zonas_alimentacao_retorno_tracao.dxf` — `aeef58ac53609f6326d77c8f3ddbb32b81db6b5d7f283c68357cc29d0d75e5ae`
- `03_matriz_protecao_supervisao_tracao_cc.dxf` — `ea1249c0fc5d1dc6399970a8218e7edadf3bb4d5baebe65aabb1f16ee0201b4a`

As três folhas foram inspecionadas nos PNGs de produção (4960 × 3507 px) e
comparadas com PDFs rasterizados independentemente pelo PDFium (4961 × 3508 px);
similaridades: 0,992628, 0,993066 e 0,990771. O validador estrito passou em 771.522
verificações, zero erros e zero avisos. Permanecem pendentes estudos de proteção,
retorno, correntes vagantes, desempenho e validação de campo. A inspeção no navegador
nativo continua aguardando autorização do usuário.

## Projeto P21 — clínica ambulatorial — 2026-11-06

Foram produzidas três pranchas A3 para uma clínica fictícia: planta elétrica
esquemática, unifilar de rede normal/gerador/UPS e matriz preliminar de continuidade.
O validador específico passou em 62 verificações. O AutoCAD AcCoreConsole 2027
(26.0.118.0.0) abriu/auditou os três DXFs, sem erros encontrados ou corrigidos.
Uma segunda execução do gerador reproduziu os mesmos hashes nos arquivos auditados:

- `01_planta_eletrica_clinica.dxf` — `d5cadac23114a21d99bb5b122275c88e8703b3e83021e360dbb605683c998610`
- `02_unifilar_fontes_quadro_clinica.dxf` — `86ee1e24981371e2aa4ac82f9676c79ab1f953f8b5a6bf8afe61a17faed80043`
- `03_matriz_continuidade_e_transferencia.dxf` — `279641dd382d9cd9d84c8d3d7bb1f972ea14fc0b57e99629a09a96a025e0fd01`

Inspecionei os três PNGs a 300 dpi e comparei-os com PDFs rasterizados independentemente
pelo PDFium. Similaridades: 0,992654, 0,992662 e 0,986103. O revisor integrado confirmou
os 21 projetos e 141 pranchas; a validação estrita passou em 784.335 verificações,
zero erros e zero avisos. Nenhum local médico foi classificado; fontes, cargas e
transferência permanecem premissas. Não foram feitos cálculos, aprovação sanitária,
ensaios ou verificação de campo. O teste pelo navegador nativo continua aguardando
autorização do usuário.

## Projeto P22 — auxílios visuais luminosos de aeródromo — 2026-11-06

Foram produzidas três pranchas A3 conceituais: arranjo indicativo de pista/taxiway,
circuitos série com CCR e matriz de controle/ensaios. O validador específico passou em
59 verificações. O AutoCAD AcCoreConsole 2027 (26.0.118.0.0) abriu/auditou os três DXFs
com `PASS`; uma segunda geração reproduziu os mesmos SHA-256:

- `01_layout_luminoso_pista_taxi.dxf` — `6666a6290f4de8be788f24cc1a25decf5102dc677c8361205a497f363c23920c`
- `02_unifilar_circuitos_serie_ccr.dxf` — `65cdef786aaeb4a33228e63bef8abb47c4653cf1dce781eed03933ef28d57463`
- `03_controle_monitoracao_e_ensaios.dxf` — `75b6119cca7fa9ac95bb51ea8ca4f0473fd0008f81de191b3f3abc1f9d90c85f`

As três folhas foram inspecionadas nos PNGs de produção (4960 × 3507 px, 300 dpi) e
comparadas com rasterizações independentes dos PDFs pelo PDFium; similaridades:
0,993205, 0,992555 e 0,986812. A revisão integrada confirmou 22 projetos, 144
pranchas, 576 arquivos gráficos e 111 CSVs, sem erros. A validação estrita passou em
794.464 verificações, sem erros ou avisos. O estudo não define geometria operacional,
fotometria, seleção, dimensionamento, aprovação aeroportuária ou liberação operacional.
Inspeção no navegador nativo continua aguardando autorização.
