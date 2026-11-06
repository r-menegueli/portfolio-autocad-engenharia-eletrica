# Projeto 03 - Painel de automação com CLP para duas bombas

Autor: **Rogério Eduardo Moreira Menegueli**

Data-base: **2026-09-06**

Revisão: **05 (comparação das filosofias de processo; 2026-11-06)**

Unidades dos desenhos: **milímetros (mm)**

## Objetivo

Documentar, para fins acadêmicos, um painel de automação com CLP genérico para duas
bombas centrífugas de um reservatório. O conjunto reúne arquitetura, distribuição
24 Vcc, entradas e saídas, comando, arranjo interno, bornes, interligações de campo,
comparação da filosofia de processo, sequência de operação/intertravamentos e plano de verificação em onze pranchas
A3 independentes.

## Escopo representado

- alimentação assumida de 220 V, trifásica, 60 Hz, esquema TN-S;
- duas bombas M1/M2 de 3 kW, contatores KM1/KM2 e relés de sobrecarga RT1/RT2;
- fonte PSU1 de 24 Vcc / 10 A, CLP1 genérico com 16 DI e 16 DO PNP;
- sensores de nível baixo-baixo, baixo, alto e alto-alto;
- modos manual e automático, alternância por ciclo e entrada da bomba de reserva;
- parada de emergência em dois canais por KSR1, independente do programa do CLP;
- relé KDRY de proteção contra funcionamento a seco em série com as bobinas;
- sinalização, alarme sonoro, réguas X1 a X4 e cabos W01 a W12.

O escopo exclui levantamento de campo, curva das bombas, cálculo hidráulico, estudo
de curto-circuito e seletividade, coordenação definitiva das proteções, análise de
risco, definição de categoria/PL/SIL, projeto térmico, fabricação, instalação,
programação vinculada a fabricante e comissionamento.

## Pranchas e derivados

| Prancha | Fonte DXF | PDF | SVG | PNG |
|---|---|---|---|---|
| 01/11 | [Arquitetura de automação](fonte/01_arquitetura_automacao.dxf) | [PDF](exports/01_arquitetura_automacao.pdf) | [SVG](exports/01_arquitetura_automacao.svg) | [PNG](exports/01_arquitetura_automacao.png) |
| 02/11 | [Alimentação 24 Vcc](fonte/02_alimentacao_24v.dxf) | [PDF](exports/02_alimentacao_24v.pdf) | [SVG](exports/02_alimentacao_24v.svg) | [PNG](exports/02_alimentacao_24v.png) |
| 03/11 | [Entradas do CLP](fonte/03_entradas_clp.dxf) | [PDF](exports/03_entradas_clp.pdf) | [SVG](exports/03_entradas_clp.svg) | [PNG](exports/03_entradas_clp.png) |
| 04/11 | [Saídas do CLP](fonte/04_saidas_clp.dxf) | [PDF](exports/04_saidas_clp.pdf) | [SVG](exports/04_saidas_clp.svg) | [PNG](exports/04_saidas_clp.png) |
| 05/11 | [Diagrama de comando](fonte/05_diagrama_comando.dxf) | [PDF](exports/05_diagrama_comando.pdf) | [SVG](exports/05_diagrama_comando.svg) | [PNG](exports/05_diagrama_comando.png) |
| 06/11 | [Layout do painel](fonte/06_layout_painel.dxf) | [PDF](exports/06_layout_painel.pdf) | [SVG](exports/06_layout_painel.svg) | [PNG](exports/06_layout_painel.png) |
| 07/11 | [Diagrama de bornes](fonte/07_diagrama_bornes.dxf) | [PDF](exports/07_diagrama_bornes.pdf) | [SVG](exports/07_diagrama_bornes.svg) | [PNG](exports/07_diagrama_bornes.png) |
| 08/11 | [Interligações de campo](fonte/08_interligacoes_campo.dxf) | [PDF](exports/08_interligacoes_campo.pdf) | [SVG](exports/08_interligacoes_campo.svg) | [PNG](exports/08_interligacoes_campo.png) |
| 09/11 | [Sequência de operação e intertravamentos](fonte/09_sequencia_operacao_intertravamentos.dxf) | [PDF](exports/09_sequencia_operacao_intertravamentos.pdf) | [SVG](exports/09_sequencia_operacao_intertravamentos.svg) | [PNG](exports/09_sequencia_operacao_intertravamentos.png) |
| 10/11 | [Plano de verificação e evidências](fonte/10_plano_verificacao_evidencias.dxf) | [PDF](exports/10_plano_verificacao_evidencias.pdf) | [SVG](exports/10_plano_verificacao_evidencias.svg) | [PNG](exports/10_plano_verificacao_evidencias.png) |
| 11/11 | [Alternativas da filosofia de processo](fonte/11_alternativas_filosofia_processo.dxf) | [PDF](exports/11_alternativas_filosofia_processo.pdf) | [SVG](exports/11_alternativas_filosofia_processo.svg) | [PNG](exports/11_alternativas_filosofia_processo.png) |

## Documentação e listas

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios técnicos e premissas](criterios-premissas.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Comparação de alternativas de processo](fonte/11_alternativas_filosofia_processo.dxf)
- [Pseudocódigo e estados](pseudocodigo-estados.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de entradas e saídas](lista-io.csv)
- [Lista de bornes](lista-bornes.csv)
- [Lista de cabos](lista-cabos.csv)
- [Matriz causa-efeito](matriz-causa-efeito.csv)
- [Plano de verificação](plano-verificacao.csv) — 12 itens, todos não executados
- [Lista de materiais](lista-materiais.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação lógica](validacao-logica.json)
- [Validação do portfólio](validacao.json)
- [Script-fonte](fonte/gerar_projeto_03.py)
- [Validador específico](fonte/validar_projeto_03.py)

## Reprodução

Na raiz do repositório:

```powershell
.\.venv\Scripts\python.exe .\03-painel-automacao-clp\fonte\gerar_projeto_03.py --root .
.\.venv\Scripts\python.exe .\03-painel-automacao-clp\fonte\validar_projeto_03.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --dpi 300
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict --format json --report .\03-painel-automacao-clp\validacao.json
```

O fluxo integrado é `python scripts/construir.py --root . --strict`.

## Estado de qualidade

As onze fontes são DXF R2013/AC1027 reais, em milímetros. PDF, SVG e PNG são
derivados do DXF; nenhum DWG integra a entrega. A revisão 02 acrescentou a prancha 09
com a sequência normal, a resposta a falhas e pendências rastreadas à matriz causa-efeito.
A revisão 03 acrescentou a prancha 10 com dados e evidências necessários; os 12 itens
seguem como `NÃO EXECUTADO`. A revisão 04 destaca na prancha 09 a divergência entre a
descrição anterior de enchimento e a sequência LSH-inicia/LSL-encerra/LSHH-reserva.
Na revisão 05, P03-11 compara duas interpretações: enchimento com LSL-inicia/LSH-encerra
e esgotamento com LSH-inicia/LSL-encerra. Os exemplos não aprovam nenhuma delas; tanques,
localização/função dos sensores, ação de LSHH e relação de LSL-LL com a sucção precisam
ser confirmados em V01. A resposta a sensor incoerente com bomba em marcha também
continua pendente. O validador P03 passou em 246 verificações e o AcCoreConsole 2027
auditou 11/11 DXFs. P03-11 foi conferida no PNG de produção a 300 dpi, no PDF
rasterizado pelo Poppler a 150 dpi e no contato das onze folhas; sua similaridade PDF/PNG
foi 0,987946. A validação estrita passou em 646.736 verificações, sem erros ou avisos;
o revisor integrado confirmou 12 projetos, 110 folhas, 440 arquivos gráficos e 75 CSVs,
com similaridade mínima de 0,981493. A inspeção dos SVGs no navegador permanece pendente
da autorização do usuário. Os validadores e a inspeção desta revisão estão registrados em
[inspecao-visual.md](inspecao-visual.md) e nos arquivos JSON desta pasta.

## Aviso obrigatório

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
