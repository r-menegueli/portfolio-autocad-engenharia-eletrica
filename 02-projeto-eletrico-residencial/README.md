# Projeto 02 - Projeto elétrico residencial

- **Autor:** Rogério Eduardo Moreira Menegueli
- **Data:** 2026-09-05
- **Revisão:** 02 (gráfica; 2026-11-05)
- **Estado:** estudo conceitual; revisão gráfica 02 e validação matemática/documental
- **Unidades:** milímetros no DXF; metros, volts, ampères, watts e volt-ampères quando indicados

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Objetivo e escopo

Documentar uma residência térrea original e inteiramente fictícia, com 75 m², alimentação
127/220 V, duas fases, neutro e condutor de proteção, quadro QD1 e oito circuitos finais.
O conjunto demonstra planta arquitetônica, iluminação, tomadas, eletrodutos, diagrama
unifilar, quadro de distribuição, quadro de cargas, detalhes de aterramento e rastreabilidade das cargas por ambiente.

O projeto inclui DR de 30 mA, DPS tipo 2, disjuntor geral, disjuntores de circuitos,
barramentos N e PE separados, identificação de circuitos, potência atribuída, seções
assumidas e lista de materiais. Não inclui levantamento de campo, projeto estrutural,
aprovação de concessionária, cálculo de curto-circuito, seletividade, ensaio de solo,
coordenação de DPS nem autorização para execução.

## Índice das pranchas

| Prancha | Fonte DXF | Tema |
| ---: | --- | --- |
| 01/09 | [01_planta_arquitetonica.dxf](fonte/01_planta_arquitetonica.dxf) | planta-base fictícia, ambientes, vãos e dimensões |
| 02/09 | [02_planta_iluminacao.dxf](fonte/02_planta_iluminacao.dxf) | pontos de luz, interruptores, comandos e circuitos C1/C2 |
| 03/09 | [03_planta_tomadas.dxf](fonte/03_planta_tomadas.dxf) | TUG, TUE e circuitos C3 a C8 |
| 04/09 | [04_planta_eletrodutos.dxf](fonte/04_planta_eletrodutos.dxf) | rotas conceituais, caixas e diâmetros assumidos |
| 05/09 | [05_diagrama_unifilar.dxf](fonte/05_diagrama_unifilar.dxf) | entrada, QG1, DPS1, DR1 e oito saídas |
| 06/09 | [06_quadro_distribuicao.dxf](fonte/06_quadro_distribuicao.dxf) | arranjo frontal conceitual de QD1, 24 módulos |
| 07/09 | [07_quadro_cargas.dxf](fonte/07_quadro_cargas.dxf) | cargas, correntes, condutores, proteção e balanço |
| 08/09 | [08_detalhes_aterramento.dxf](fonte/08_detalhes_aterramento.dxf) | esquema TN-S, equipotencialização e eletrodo indicativo |
| 09/09 | [09_rastreabilidade_ambientes_cargas.dxf](fonte/09_rastreabilidade_ambientes_cargas.dxf) | áreas, cargas atribuídas e circuitos por ambiente, ligados aos CSVs |

Cada DXF tem correspondente PDF, SVG e PNG em [exports](exports/). Os desenhos são
pranchas A3 paisagem de 420 x 297 mm e usam DXF R2013/AC1027 como fonte principal.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Quadro de cargas em CSV](quadro-cargas.csv)
- [Rastreabilidade de ambientes e cargas em CSV](rastreabilidade-ambientes.csv)
- [Lista de pontos em CSV](lista-pontos.csv)
- [Lista de materiais em CSV](lista-materiais.csv)
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

Resultado da revisão em 2026-11-05:

- validador matemático do P02: `PASS`, 63 verificações e 0 erros; os oito
  ambientes, 19 linhas de pontos e 15.548,913 VA estão rastreados, mas marcados
  como premissas;
- validação estrita do portfólio: `PASS`, 521.224 verificações, 0 erros e 0 avisos;
- nove DXFs abertos e auditados no Autodesk AcCoreConsole 2027: `PASS`;
- nove folhas renderizadas em PDF, SVG e PNG; o contato atualizado foi conferido;
  P02-01 foi inspecionada integralmente no PNG de produção, e P02-09 no PNG de
  produção e em PDF rasterizado independentemente a 150 dpi;
- o revisor encontrou similaridade mínima PDF/PNG de 0,986556 no conjunto P02;
- o gerador repetido produziu hashes idênticos nos nove DXFs.

Os relatórios processáveis são [validacao-matematica.json](validacao-matematica.json) e
[validacao.json](validacao.json). Nenhum DWG foi gerado ou incluído.

Esta revisão não transforma a planta fictícia nem as potências assumidas em dados de
campo. A inspeção visual dos SVGs da revisão 02 no navegador continua pendente de
autorização; a inspeção anterior em Chromium é histórica e se refere à revisão 00.
