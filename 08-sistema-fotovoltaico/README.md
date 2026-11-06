# Projeto 08 - Estudo acadêmico de sistema fotovoltaico residencial

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 08

Formato: A3 paisagem, unidades geométricas em milímetros, revisão 04 (2026-11-06)

Estado: ampliado e revisado em 2026-11-06

Este projeto apresenta um sistema fotovoltaico residencial conceitual, conectado à
rede, com 6,60 kWp no lado CC e inversor string acadêmico de 6 kWca em 220 V. O arranjo
usa 12 módulos de 550 Wp, divididos em duas strings independentes de seis módulos, uma
por MPPT.

O estudo não seleciona fabricante, não substitui levantamento de campo, projeto
estrutural, consulta à distribuidora, análise de sombreamento, coordenação de proteção,
comissionamento ou responsabilidade técnica.

Na revisão 04, a legenda da prancha 01 passa a corresponder à cor usada para CC, e a
prancha 06 identifica individualmente os cabos CC, CA e PE conforme
`lista-cabos.csv`, associa S1/MPPT 1 e S2/MPPT 2 e exibe os comprimentos assumidos.
As rotas são esquemáticas e não foram medidas em um imóvel; o cabo de comunicação
opcional está identificado, mas seu trajeto físico não foi definido.

A estimativa anterior de 9.770,904 kWh/ano permanece como caso didático calculado com
HSP 5,2 e PR 0,78. A nova análise mostra a sensibilidade a outros pares de parâmetros;
os intervalos escolhidos são matemáticos e não representam recurso solar de uma região,
faixa provável ou previsão de geração.

## Pranchas

1. [Disposição dos módulos](fonte/01_disposicao_modulos.dxf)
2. [Diagrama unifilar CC](fonte/02_diagrama_unifilar_cc.dxf)
3. [Diagrama unifilar CA](fonte/03_diagrama_unifilar_ca.dxf)
4. [String box](fonte/04_string_box.dxf)
5. [Aterramento e equipotencialização](fonte/05_aterramento.dxf)
6. [Layout dos equipamentos](fonte/06_layout_equipamentos.dxf)
7. [Sensibilidade da energia anual](fonte/07_sensibilidade_energia.dxf)
8. [Envelope térmico da string](fonte/08_envelope_termico_string.dxf)

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Dados declarados

| Grandeza | Valor acadêmico |
| --- | ---: |
| potência unitária do módulo | 550 Wp |
| quantidade de módulos | 12 |
| potência instalada CC | 6,60 kWp |
| strings | 2 × 6 módulos em série |
| Vmp por string em STC | 250,8 Vcc |
| Voc por string em STC | 299,4 Vcc |
| Imp por string em STC | 13,16 A |
| Isc por string em STC | 13,92 A |
| inversor adotado | INV-FV-801, classe acadêmica 6 kWca, 220 V, 2 MPPT |
| relação CC/CA | 1,10 |

Os valores completos, coeficientes térmicos e limites do inversor estão em
[Parâmetros](parametros.csv). O inversor é uma especificação funcional fictícia, não
um modelo comercial homologado.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de módulos](lista-modulos.csv)
- [Lista de proteções](lista-protecoes.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de equipamentos e materiais](lista-materiais.csv)
- [Resultados dos cálculos](resultados-calculo.csv)
- [Sensibilidade da energia](sensibilidade-energia.csv)
- [Envelope térmico calculado por string](envelope-termico.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-fotovoltaico.json)
- [Validação estrita](validacao.json)

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 08-sistema-fotovoltaico\fonte\gerar_projeto_08.py --root .
.venv\Scripts\python.exe 08-sistema-fotovoltaico\fonte\validar_projeto_08.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 08-sistema-fotovoltaico\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.

## Verificação da revisão 02

- validador específico: consulte [validacao-fotovoltaico.json](validacao-fotovoltaico.json);
- validação estrita integrada: consulte [validacao.json](validacao.json);
- AutoCAD AcCoreConsole 2027: os sete DXFs da revisão 02 foram abertos e auditados, `PASS` em 7/7;
- derivados: 21 arquivos gerados (sete PDF, sete SVG e sete PNG); as sete PNGs e os sete PDFs foram inspecionados visualmente;
- PDFs: uma página A3 por prancha, reabertos e rasterizados pelo Poppler;
- os SVGs da revisão 02 foram gerados; a inspeção adicional em navegador permanece pendente de autorização;
- reprodutibilidade: consulte o registro de hashes atualizado no manifesto de renders.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Revisão 03

A prancha 08 torna visível a correção de Vmp e Voc em `-5 °C`, STC e `70 °C`, junto
à faixa MPPT `90–550 V` e ao limite CC de `600 V` propostos para INV-FV-801. Para a
string de seis módulos, `Voc fria=324,5496 V` e `Vmp quente=216,942 V`. A `Isc` corrigida
em 1.100 W/m² varia de `15,08232 A` a `15,65652 A`; a comparação com o limite de curto
do MPPT ainda usa valores fictícios. `Isc` não substitui a corrente operacional `Imp`:
esta precisa ser confirmada com curvas/dados OEM do módulo e do inversor.

- A tabela reproduzível está em `envelope-termico.csv` e é gerada a partir de
  `parametros.csv`; todas as entradas continuam classificadas como premissas/propostas.
- O validador P08 passou em 8.119 verificações, sem erros; o AutoCAD AcCoreConsole
  2027 auditou 8/8 DXFs. A validação estrita integrada mais recente passou em 650.961
  verificações, sem erros ou avisos.
- O revisor mais recente confirmou 12 projetos, 111 folhas, 444 arquivos gráficos e
  75 CSVs; similaridade mínima PDF/PNG de 0,981493; P08-08 obteve 0,989722.
- P08-08 e o contato das oito folhas foram examinados em PNG; a folha nova também foi
  inspecionada em PDF rasterizado independentemente a 150 dpi, sem cortes ou colisões.
- Os SVGs reemitidos ainda aguardam inspeção visual no navegador.
- Os limites do inversor não são de fabricante e a folha não comprova compatibilidade,
  dimensionamento, operação real, proteção ou conformidade do sistema.
- Verificação CAD/visual: consulte [inspeção visual](inspecao-visual.md) e
  [validação específica](validacao-fotovoltaico.json).

## Revisão 04

A prancha 01 corrige a legenda para que a cor CC corresponda aos cabos turquesa
renderizados. A prancha 06 substitui a rota agregada `R-CC-801/802` por dois percursos e referências
de cabo distintos: `FV-S1 / R-CC-801` até SB-FV-801 e `FV-S2 / R-CC-802` até SB-FV-801;
as saídas da caixa são indicadas separadamente para MPPT 1 e MPPT 2. Também são
identificados `CA-INV / R-CA-801`, `CA-PCC / R-CA-802`, os dois condutores PE e o cabo
`COM-INV` opcional. Os comprimentos vêm da lista de cabos e continuam como hipóteses,
sem levantamento de campo. A comunicação opcional não tem trajeto físico definido.

- O validador P08 passou em 8.131 verificações; o AcCoreConsole 2027 abriu e auditou
  8/8 DXFs, todos com `PASS`.
- Foram gerados os 24 derivados da revisão 04. P08-01 e P08-06 foram examinadas nas
  PNGs a 300 dpi e nos PDFs A3 rasterizados independentemente pelo Poppler a 150 dpi;
  o contato das oito folhas também foi conferido.
- P08-06 obteve similaridade PDF/PNG de 0,989889. O revisor integrado passou em 12
  projetos, 114 folhas, 456 arquivos gráficos e 77 CSVs, com mínimo de 0,981493.
- A validação estrita passou em 674.521 verificações, sem erros nem avisos.
- Os SVGs foram gerados, mas sua inspeção em navegador aguarda autorização. Não foi
  executada simulação elétrica; as rotas e extensões seguem como premissas conceituais.
