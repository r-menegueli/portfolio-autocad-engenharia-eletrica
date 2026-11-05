# Projeto 01 - Painel de acionamento de motor com inversor

Autor: **Rogério Eduardo Moreira Menegueli**

Data-base: **2026-09-05**

Revisão: **02 (gráfica; 2026-11-05)**

Unidades dos desenhos: **milímetros (mm)**

## Objetivo

Documentar, para fins acadêmicos, um painel de acionamento de um motor de indução
trifásico de 7,5 kW por inversor de frequência. O conjunto reúne potência, comando,
segurança funcional conceitual, terminais, arranjo interno e interfaces de campo em
sete pranchas A3 independentes.

## Escopo representado

- alimentação 380 V, trifásica, 60 Hz, esquema TN-S assumido;
- seccionamento Q0, disjuntor Q1, DPS1 e proteção eletrônica do motor no VFD1;
- inversor de frequência VFD1 e motor de indução M1;
- emergência S0 em dois canais, relé KSR1 e entradas STO-A/STO-B;
- partida, parada, rearme e seleção local/remoto em 24 Vcc;
- referência local de 0-10 V e remota de 4-20 mA;
- sinalização de painel energizado, pronto, marcha e falha;
- bornes X1, X2 e X3, barra PE e cabos W01 a W06 identificados.

O escopo exclui levantamento de campo, estudo de curto-circuito, seletividade,
coordenação completa de proteção, análise de risco, validação de nível de desempenho,
projeto térmico definitivo, parametrização vinculada a fabricante, fabricação,
instalação e comissionamento.

## Pranchas e derivados

| Prancha | Fonte DXF | PDF | SVG | PNG |
|---|---|---|---|---|
| 01/07 | [Diagrama unifilar](fonte/01_diagrama_unifilar.dxf) | [PDF](exports/01_diagrama_unifilar.pdf) | [SVG](exports/01_diagrama_unifilar.svg) | [PNG](exports/01_diagrama_unifilar.png) |
| 02/07 | [Diagrama de potência](fonte/02_diagrama_potencia.dxf) | [PDF](exports/02_diagrama_potencia.pdf) | [SVG](exports/02_diagrama_potencia.svg) | [PNG](exports/02_diagrama_potencia.png) |
| 03/07 | [Diagrama de comando](fonte/03_diagrama_comando.dxf) | [PDF](exports/03_diagrama_comando.pdf) | [SVG](exports/03_diagrama_comando.svg) | [PNG](exports/03_diagrama_comando.png) |
| 04/07 | [Layout interno](fonte/04_layout_interno_painel.dxf) | [PDF](exports/04_layout_interno_painel.pdf) | [SVG](exports/04_layout_interno_painel.svg) | [PNG](exports/04_layout_interno_painel.png) |
| 05/07 | [Diagrama de bornes](fonte/05_diagrama_bornes.dxf) | [PDF](exports/05_diagrama_bornes.pdf) | [SVG](exports/05_diagrama_bornes.svg) | [PNG](exports/05_diagrama_bornes.png) |
| 06/07 | [Interligações de campo](fonte/06_interligacoes_campo.dxf) | [PDF](exports/06_interligacoes_campo.pdf) | [SVG](exports/06_interligacoes_campo.svg) | [PNG](exports/06_interligacoes_campo.png) |
| 07/07 | [Proteção e dados para coordenação](fonte/07_protecao_coordenacao.dxf) | [PDF](exports/07_protecao_coordenacao.pdf) | [SVG](exports/07_protecao_coordenacao.svg) | [PNG](exports/07_protecao_coordenacao.png) |

## Documentação

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios técnicos e premissas](criterios-premissas.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Relação conceitual entre V/f e FOC](controle-vf-foc.md)
- [Registro de inspeção visual](inspecao-visual.md)
- [Lista de cabos](lista-cabos.csv)
- [Lista de materiais](lista-materiais.csv)
- [Matriz de proteção e dados pendentes](protecao-coordenacao.csv)
- [Script-fonte](fonte/gerar_projeto_01.py)
- [Relatório de validação](validacao.json)

## Reprodução

Na raiz do repositório, com o ambiente descrito no README principal:

```powershell
.\.venv\Scripts\python.exe .\01-painel-motor-inversor\fonte\gerar_projeto_01.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --dpi 300
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict --format json --report .\01-painel-motor-inversor\validacao.json
```

O comando integrado também regenera a infraestrutura compartilhada:

```powershell
.\.venv\Scripts\python.exe .\scripts\construir.py --root . --strict
```

## Estado de qualidade

As sete fontes são DXF R2013/AC1027 reais, em milímetros, com os layers obrigatórios.
PDF, SVG e PNG são derivados do DXF. As sete fontes passaram pela auditoria do AutoCAD
2027 na revisão 02. A folha 07 organiza os dados ainda necessários para selecionar e
coordenar as proteções, sem substituir cálculo ou documentação de fabricante. A validação
estrita e a inspeção visual desta revisão estão aprovadas; os resultados são
registrados em `validacao.json` e em [inspecao-visual.md](inspecao-visual.md).

## Aviso obrigatório

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
