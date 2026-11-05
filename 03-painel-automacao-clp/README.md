# Projeto 03 - Painel de automação com CLP para duas bombas

Autor: **Rogério Eduardo Moreira Menegueli**

Data-base: **2026-09-06**

Revisão: **02 (sequência de operação; 2026-11-05)**

Unidades dos desenhos: **milímetros (mm)**

## Objetivo

Documentar, para fins acadêmicos, um painel de automação com CLP genérico para duas
bombas centrífugas de um reservatório. O conjunto reúne arquitetura, distribuição
24 Vcc, entradas e saídas, comando, arranjo interno, bornes, interligações de campo e
sequência visual de operação/intertravamentos em nove pranchas A3 independentes.

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
| 01/09 | [Arquitetura de automação](fonte/01_arquitetura_automacao.dxf) | [PDF](exports/01_arquitetura_automacao.pdf) | [SVG](exports/01_arquitetura_automacao.svg) | [PNG](exports/01_arquitetura_automacao.png) |
| 02/09 | [Alimentação 24 Vcc](fonte/02_alimentacao_24v.dxf) | [PDF](exports/02_alimentacao_24v.pdf) | [SVG](exports/02_alimentacao_24v.svg) | [PNG](exports/02_alimentacao_24v.png) |
| 03/09 | [Entradas do CLP](fonte/03_entradas_clp.dxf) | [PDF](exports/03_entradas_clp.pdf) | [SVG](exports/03_entradas_clp.svg) | [PNG](exports/03_entradas_clp.png) |
| 04/09 | [Saídas do CLP](fonte/04_saidas_clp.dxf) | [PDF](exports/04_saidas_clp.pdf) | [SVG](exports/04_saidas_clp.svg) | [PNG](exports/04_saidas_clp.png) |
| 05/09 | [Diagrama de comando](fonte/05_diagrama_comando.dxf) | [PDF](exports/05_diagrama_comando.pdf) | [SVG](exports/05_diagrama_comando.svg) | [PNG](exports/05_diagrama_comando.png) |
| 06/09 | [Layout do painel](fonte/06_layout_painel.dxf) | [PDF](exports/06_layout_painel.pdf) | [SVG](exports/06_layout_painel.svg) | [PNG](exports/06_layout_painel.png) |
| 07/09 | [Diagrama de bornes](fonte/07_diagrama_bornes.dxf) | [PDF](exports/07_diagrama_bornes.pdf) | [SVG](exports/07_diagrama_bornes.svg) | [PNG](exports/07_diagrama_bornes.png) |
| 08/09 | [Interligações de campo](fonte/08_interligacoes_campo.dxf) | [PDF](exports/08_interligacoes_campo.pdf) | [SVG](exports/08_interligacoes_campo.svg) | [PNG](exports/08_interligacoes_campo.png) |
| 09/09 | [Sequência de operação e intertravamentos](fonte/09_sequencia_operacao_intertravamentos.dxf) | [PDF](exports/09_sequencia_operacao_intertravamentos.pdf) | [SVG](exports/09_sequencia_operacao_intertravamentos.svg) | [PNG](exports/09_sequencia_operacao_intertravamentos.png) |

## Documentação e listas

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios técnicos e premissas](criterios-premissas.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Pseudocódigo e estados](pseudocodigo-estados.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de entradas e saídas](lista-io.csv)
- [Lista de bornes](lista-bornes.csv)
- [Lista de cabos](lista-cabos.csv)
- [Matriz causa-efeito](matriz-causa-efeito.csv)
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

As nove fontes são DXF R2013/AC1027 reais, em milímetros. PDF, SVG e PNG são
derivados do DXF; nenhum DWG integra a entrega. A nova prancha 09 explicita a sequência
normal, a resposta a falhas e pontos ainda indefinidos na lógica, em rastreabilidade com
a matriz causa-efeito. Os validadores atuais e o estado da inspeção desta revisão estão
registrados em [inspecao-visual.md](inspecao-visual.md) e nos arquivos JSON desta pasta.

## Aviso obrigatório

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
