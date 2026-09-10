# Relatório de validação consolidada

**Data:** 2026-09-10

**Escopo:** repositório completo, Projetos P01 a P10

**Autor:** Rogério Eduardo Moreira Menegueli

**Resultado:** **PASS**

## Resumo executivo

| Verificação | Escopo | Resultado |
| --- | ---: | :---: |
| Reconstrução completa | template, carimbo e 68 pranchas | PASS |
| Validador comum estrito | 370.584 verificações | PASS |
| Validadores específicos | P02 a P10, 9 executáveis | PASS |
| Auditoria consolidada | 10 projetos, 68 pranchas, 272 arquivos e 50 CSVs | PASS |
| AutoCAD/AcCoreConsole | 70 DXFs abertos e auditados | 70/70 PASS |
| PDFs de projeto | 68 arquivos reabertos, A3 e comparados aos PNGs | 68/68 PASS |
| SVGs | 70 arquivos renderizados no Microsoft Edge | 70/70 PASS |
| PNGs de projeto | 68 arquivos em 300 dpi e proporção A3 | 68/68 PASS |
| Workbooks | 2 arquivos, 13 abas, varredura de fórmulas | PASS |
| Testes Python | 9 testes | 9 PASS |
| Compilação Python | scripts comuns e fontes P01–P10 | PASS |
| Links e privacidade | links locais, CPF, RG, telefone e endereço | PASS |
| Estado do Git após o commit | árvore de trabalho | CLEAN |

## Comandos executados

Reconstrução e validação principal:

```powershell
.\.venv\Scripts\python.exe .\scripts\construir.py --root . --strict
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

Auditoria consolidada de arquivos, tabelas, carimbos e equivalência PDF/PNG:

```powershell
.\.venv\Scripts\python.exe .\scripts\revisar_portfolio.py --root .
```

Auditoria somente leitura dos workbooks:

```powershell
.\.venv\Scripts\python.exe .\scripts\revisar_workbooks.py --root .
```

Testes e compilação:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q scripts 01-painel-motor-inversor\fonte 02-projeto-eletrico-residencial\fonte 03-painel-automacao-clp\fonte 04-controle-nivel-reservatorio\fonte 05-instalacao-eletrica-industrial\fonte 06-centro-controle-motores\fonte 07-arquitetura-veiculo-eletrico\fonte 08-sistema-fotovoltaico\fonte 09-fonte-bancada\fonte 10-rede-instrumentacao-industrial\fonte
```

A auditoria CAD chamou `scripts/autocad_console.ps1 -Action Audit` para cada um dos
70 DXFs. Os SVGs foram abertos em modo headless no Microsoft Edge 152.0.4191.66.

## Resultados dos validadores específicos

| Projeto | Validador | Verificações | Resultado |
| :---: | --- | ---: | :---: |
| P01 | validador comum + auditoria consolidada | incluído no total global | PASS |
| P02 | matemática residencial | 41 | PASS |
| P03 | lógica do CLP | 129 | PASS |
| P04 | controle de nível | 169 | PASS |
| P05 | cálculos industriais | 294 | PASS |
| P06 | integração do CCM | 828 | PASS |
| P07 | arquitetura veicular | 4.224 | PASS |
| P08 | sistema fotovoltaico | 8.036 | PASS |
| P09 | fonte de bancada | 18.554 | PASS |
| P10 | instrumentação industrial | 64.207 | PASS |

Os arquivos `validacao.json` presentes nos projetos são registros históricos do
estado global na conclusão de cada etapa. O resultado vigente do repositório é o
registrado neste relatório e deve ser reproduzido pelo comando estrito acima.

## Verificações cruzadas adicionais

O script [revisar_portfolio.py](scripts/revisar_portfolio.py) confirmou:

- 68 identificadores de prancha no formato `NN/TT` e 68 carimbos com autor;
- DXF AC1027 e `$INSUNITS = 4` em todas as fontes de projeto;
- presença dos 14 layers obrigatórios;
- igualdade do nome-base entre DXF, PDF, SVG e PNG;
- 50 CSVs não vazios, com cabeçalhos únicos e linhas de largura uniforme;
- PDFs de uma página com MediaBox A3 paisagem;
- SVGs XML válidos com `viewBox`;
- PNGs válidos, não uniformes e com largura mínima;
- similaridade visual PDF/PNG mínima de 0,9842;
- ausência de padrões de CPF e telefone nos textos examinados.

## Avisos e limitações

Os nove testes passaram com seis `DeprecationWarning` emitidos internamente pelo
`ezdxf 1.4.4` ao usar `numpy 2.5.2`. O aviso é conhecido, não altera o resultado e já
consta no relatório de ferramentas. O `ruff` não está instalado no ambiente; a
verificação sintática foi feita com `compileall` e os testes exercitam o validador.

LibreCAD, ODA File Converter e Inkscape não estão disponíveis. Essa ausência reduz a
diversidade de motores de leitura testados, mas é compensada por `ezdxf`, AutoCAD,
AcCoreConsole, PDFium, Poppler e navegador Chromium. Nenhum DWG foi criado ou
versionado.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
