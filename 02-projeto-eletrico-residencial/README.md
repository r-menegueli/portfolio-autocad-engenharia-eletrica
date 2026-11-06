# Projeto 02 - Projeto elétrico residencial

- **Autor:** Rogério Eduardo Moreira Menegueli
- **Data de criação:** 2026-09-05
- **Revisão:** 04 (corrente por fase; 2026-11-06)
- **Estado:** estudo conceitual; demanda, QG1 e alimentador ainda sem dimensionamento
- **Unidades:** milímetros no DXF; metros, volts, ampères, watts e volt-ampères quando indicados

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Objetivo e escopo

Documentar uma residência térrea original e inteiramente fictícia, com 75 m², alimentação
127/220 V, duas fases, neutro e condutor de proteção, quadro QD1 e oito circuitos finais.
O conjunto demonstra planta arquitetônica mobiliada, vãos e acessos, iluminação, tomadas,
eletrodutos, diagrama unifilar, quadro de distribuição, quadro de cargas, detalhes de
aterramento e rastreabilidade das cargas por ambiente.

O projeto representa DR de 30 mA, DPS tipo 2, disjuntores de circuitos, barramentos N e
PE separados, identificação de circuitos, potência atribuída, seções assumidas e lista
de materiais. A revisão 04 retira a corrente nominal do disjuntor geral e a seção do
alimentador como seleções. Não inclui levantamento de campo, projeto estrutural,
aprovação de concessionária, cálculo de curto-circuito, seletividade, ensaio de solo,
coordenação de DPS nem autorização para execução.

## Índice das pranchas

| Prancha | Fonte DXF | Tema |
| ---: | --- | --- |
| 01/10 | [01_planta_arquitetonica.dxf](fonte/01_planta_arquitetonica.dxf) | ambientes mobiliados, vãos identificados, dimensões e quadros de ambientes/esquadrias |
| 02/10 | [02_planta_iluminacao.dxf](fonte/02_planta_iluminacao.dxf) | pontos de luz, interruptores, comandos e circuitos C1/C2 |
| 03/10 | [03_planta_tomadas.dxf](fonte/03_planta_tomadas.dxf) | TUG, TUE e circuitos C3 a C8 |
| 04/10 | [04_planta_eletrodutos.dxf](fonte/04_planta_eletrodutos.dxf) | rotas conceituais, caixas e diâmetros assumidos |
| 05/10 | [05_diagrama_unifilar.dxf](fonte/05_diagrama_unifilar.dxf) | entrada, QG1 e oito saídas, com calibre geral pendente |
| 06/10 | [06_quadro_distribuicao.dxf](fonte/06_quadro_distribuicao.dxf) | arranjo frontal conceitual de QD1, 24 módulos |
| 07/10 | [07_quadro_cargas.dxf](fonte/07_quadro_cargas.dxf) | cargas e correntes dos circuitos; demanda/alimentador pendentes |
| 08/10 | [08_detalhes_aterramento.dxf](fonte/08_detalhes_aterramento.dxf) | esquema TN-S, equipotencialização e eletrodo indicativo |
| 09/10 | [09_rastreabilidade_ambientes_cargas.dxf](fonte/09_rastreabilidade_ambientes_cargas.dxf) | áreas, cargas atribuídas e circuitos por ambiente, ligados aos CSVs |
| 10/10 | [10_corrente_por_fase.dxf](fonte/10_corrente_por_fase.dxf) | cota superior aritmética sem diversidade e comparação com a antiga premissa de QG1 |

Cada DXF tem correspondente PDF, SVG e PNG em [exports](exports/). Os desenhos são
pranchas A3 paisagem de 420 x 297 mm e usam DXF R2013/AC1027 como fonte principal.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Quadro de cargas em CSV](quadro-cargas.csv)
- [Análise de corrente por fase em CSV](analise-corrente-por-fase.csv), gerada a partir do quadro de cargas
- [Rastreabilidade de ambientes e cargas em CSV](rastreabilidade-ambientes.csv)
- [Lista de pontos em CSV](lista-pontos.csv)
- [Lista de materiais em CSV](lista-materiais.csv)
- [Quadro de esquadrias e dimensões adotadas em CSV](esquadrias.csv)
- [Inspeção visual](inspecao-visual.md)

## Reprodução

A partir da raiz do repositório, com o ambiente virtual preparado:

```powershell
.\.venv\Scripts\python.exe .\02-projeto-eletrico-residencial\fonte\gerar_projeto_02.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --dpi 300
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

O fluxo completo pode ser repetido com:

```powershell
.\.venv\Scripts\python.exe .\scripts\construir.py --root . --strict
```

## Base normativa e limites

Foram consultadas as edições identificadas em [referencias-normativas.md](referencias-normativas.md).
A consulta de títulos e vigência não equivale à aquisição nem à verificação integral do
conteúdo das normas. Os critérios numéricos deste estudo são premissas acadêmicas
explicitadas, não declaração de conformidade normativa.

## Validação

Revisão de projeto em 2026-11-06:

- validador matemático do P02: `PASS`, 98 verificações e 0 erros; os oito ambientes,
  pontos, cargas e cotas por fase são rastreados, com arquitetura e potências marcadas
  como premissas;
- as 10 folhas A3, seus DXFs e derivados PDF/SVG/PNG foram regenerados; o CSV
  `analise-corrente-por-fase.csv` é a base rastreável de P02-10;
- AutoCAD AcCoreConsole 2027 abriu e auditou os dez DXFs: `PASS` em 10/10, com zero
  erros encontrados e zero corrigidos;
- o validador estrito passou em 656.386 verificações, sem erros nem avisos;
- conferi o contato atualizado das dez folhas e a rasterização integral de P02-10:
  moldura, tabela, gráfico, limites do cálculo e carimbo rev. 04/10 estão legíveis e
  sem cortes aparentes;
- a similaridade independente PDF/PNG de P02-10 foi 0,989581; a menor similaridade
  entre as dez folhas P02 foi 0,984878. O revisor integrado passou em 12 projetos,
  112 pranchas, 448 arquivos gráficos e 76 CSVs, com mínimo geral de 0,981493.

Os relatórios processáveis são [validacao-matematica.json](validacao-matematica.json) e
[validacao.json](validacao.json). Nenhum DWG foi gerado ou incluído.

Esta revisão não transforma a planta fictícia, os vãos, mobiliário nem as potências
assumidas em dados de campo. O CSV de esquadrias e as geometrias do gerador devem ser
conferidos após mudanças coordenadas. A inspeção visual dos SVGs no navegador permanece
pendente de autorização; os registros anteriores do Chromium cobrem revisões históricas.
