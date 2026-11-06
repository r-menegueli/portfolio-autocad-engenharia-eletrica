# Projeto 09 - Fonte de bancada ajustável

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 10

Formato: A3 paisagem, geometria em milímetros, revisão 05 (2026-11-06)

Estado: estudo acadêmico em revisão 05; P09-05 agora representa os 16 recortes propostos com centros, dimensões e status rastreáveis. Sem liberação para fabricação.

Este projeto apresenta a documentação eletromecânica acadêmica de uma fonte de
bancada ajustável. A arquitetura proposta recebe 90 a 264 Vca, 47 a 63 Hz, e fornece
saída isolada da rede e flutuante em relação ao chassi, regulável de 0,8 a 30 Vcc e
limitada a 5 A, com potência máxima de 150 W. K1 abre somente o condutor positivo e
desabilita a entrega de potência, mas a tensão residual nos bornes não é garantida.
A revisão 03 separa o nó interno e a porta X2 para estudo paramétrico de descarga;
nenhum componente ou requisito de tensão/tempo foi definido. O ramo da porta não pode
fechar com fonte externa conectada. A revisão 04 mostra uma varredura das perdas
agregadas de PS1 e REG1 em nove combinações de eficiência assumidas. Os cenários não
são dados OEM, medições, curvas térmicas ou previsões de temperatura.
A revisão 05 completa a representação mecânica dos 16 registros de `lista-recortes.csv`
na prancha 05, incluindo os indicadores LED e os quatro furos do ventilador. Centros,
dimensões e classificações aparecem individualmente; continuam como propostas sujeitas
à confirmação dos fabricantes, sem tolerâncias ou detalhes de fabricação.
O controlador não regula até zero. A conversão combina uma fonte AC/DC
isolada de 36 Vcc e um buck síncrono CC/CV com LM5190 como candidato de referência.

O estudo cobre proteção de entrada, conversão, regulação, medição, comandos,
conectores, ventilação, painel frontal, organização interna e interligações. Não
define PCB, firmware, isolamento construtivo, categoria de sobretensão, coordenação
de fusíveis, compatibilidade eletromagnética, calibração, ensaios térmicos, MOSFETs
finais, redes passivas, compensação das malhas ou homologação de componentes.

## Pranchas

1. [Diagrama de blocos](fonte/01_diagrama_blocos.dxf)
2. [Diagrama elétrico](fonte/02_diagrama_eletrico.dxf)
3. [Painel frontal](fonte/03_painel_frontal.dxf)
4. [Layout interno](fonte/04_layout_interno.dxf)
5. [Detalhes mecânicos](fonte/05_detalhes_mecanicos.dxf)
6. [Interligações](fonte/06_interligacoes.dxf)
7. [Topologia do buck síncrono CC/CV](fonte/07_topologia_regulador_cc_cv.dxf)
8. [Pré-dimensionamento do estágio buck](fonte/08_predimensionamento_buck.dxf)
9. [Análise paramétrica da descarga da saída](fonte/09_descarga_saida_parametrica.dxf)
10. [Matriz paramétrica de perdas e carga térmica](fonte/10_matriz_perdas_termicas_parametrica.dxf)

Cada DXF tem derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Características declaradas

| Grandeza | Valor acadêmico |
| --- | ---: |
| entrada | 90-264 Vca, 47-63 Hz, L/N/PE |
| classe construtiva proposta | classe I, chassi metálico ligado ao PE |
| saída regulada | 0,8-30 Vcc; até 5 A; 150 W máximo |
| saída desabilitada | K1 abre o condutor positivo; a tensão residual nos bornes não é garantida |
| modo de regulação | CC/CV síncrono; U1 LM5190 apenas como candidato de arquitetura |
| estágio isolado PS1 | 36 Vcc, 7 A, 252 W |
| regulador REG1 | buck síncrono CC/CV, 150 W propostos; U1 LM5190 como candidato de referência |
| saída em relação ao chassi | flutuante; negativo não ligado internamente ao PE |
| invólucro de referência | 320 × 150 × 260 mm |
| ambiente de premissa | interno, seco, 0-40 °C, até 2.000 m |

Os valores e sua classificação epistemológica estão em [Parâmetros](parametros.csv) e
no [pré-dimensionamento](dimensionamento-regulador.csv). U1 LM5190 é candidato de
referência; MOSFETs, passivos, compensação, layout e validação do estágio completo
continuam pendentes. Nenhum conjunto foi declarado certificado.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de equipamentos](lista-equipamentos.csv)
- [Lista de proteções](lista-protecoes.csv)
- [Lista de interligações](lista-interligacoes.csv)
- [Lista de recortes](lista-recortes.csv)
- [Lista de materiais](lista-materiais.csv)
- [Resultados dos cálculos](resultados-calculo.csv)
- [Pré-dimensionamento do regulador](dimensionamento-regulador.csv)
- [Dimensionamento paramétrico da descarga](dimensionamento-descarga.csv)
- [Cenários paramétricos de perdas](dimensionamento-termico-parametrico.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-fonte.json)
- [Validação estrita](validacao.json)

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 09-fonte-bancada\fonte\gerar_projeto_09.py --root .
.venv\Scripts\python.exe 09-fonte-bancada\fonte\validar_projeto_09.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 09-fonte-bancada\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.
As expressões RC usam uma aproximação ideal e permanecem sem resultados numéricos até
que capacitâncias máximas, tensões iniciais, limite residual, tempo e capacidade de
pulso sejam especificados. Também faltam validação do intertravamento, comportamento
sob falha, energia por evento, repetição e aquecimento. A varredura de perdas cobre
somente POUT=150 W e eficiências hipotéticas; perdas por componente, Rθ admissível,
fluxo de ar e temperaturas seguem sem dados. Ela não demonstra capacidade térmica.
A prancha não declara tensão segura, descarga garantida ou aptidão para montagem.

## Resultado de qualidade

- o validador específico aprovou 18.916 verificações, sem erros;
- as dez folhas DXF foram geradas pelo script, verificadas pelo validador do projeto e
  abertas/auditadas 10/10 no AutoCAD AcCoreConsole 2027, resultado `PASS`;
- os 30 derivados da revisão 05 foram reconstruídos: dez PDFs, dez SVGs e dez PNGs;
- o revisor conferiu 12 projetos, 114 folhas, 456 arquivos gráficos e 77 CSVs; a
  similaridade mínima entre PDF e PNG foi 0,9815;
- a validação estrita do portfólio aprovou 673.894 verificações, sem erros ou avisos;
- o contato atualizado das dez folhas P09 foi conferido. P09-05 foi examinada no PNG
  integral de 4.960 × 3.507 px e no PDF rasterizado pelo Poppler 26.07.0 a 150 dpi
  (2.481 × 1.754 px), sem cortes ou sobreposição relevante;
- a inspeção visual dos SVGs no navegador e a simulação elétrica continuam pendentes.
  A auditoria AcCoreConsole confirma abertura/integridade CAD, não conformidade,
  dimensionamento ou funcionamento elétrico.

Nenhum DWG foi criado ou distribuído. O projeto continua acadêmico, conceitual, sem
certificação e sem liberação para fabricação ou uso em rede elétrica.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
