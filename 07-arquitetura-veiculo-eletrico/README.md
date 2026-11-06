# Projeto 07 - Arquitetura elétrica acadêmica de veículo elétrico

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 11

Formato: A3 paisagem, unidades geométricas em milímetros, revisão gráfica 04 (2026-11-06)

Estado: ampliado e revisado em 2026-11-06

Este projeto apresenta a arquitetura elétrica conceitual do EV-07, um veículo elétrico
didático com bateria de tração, inversor e motor de indução. O escopo relaciona a
arquitetura física às estratégias de controle V/f e FOC estudadas no TCC do autor, sem
declarar, reproduzir ou inventar qualquer resultado experimental do trabalho acadêmico.

## Escopo

- bateria de tração, BMS, fusíveis, contatores, pré-carga e PDU de alta tensão;
- inversor trifásico e motor de indução;
- conversor CC-CC, bateria auxiliar de 12 V e distribuição de baixa tensão;
- VCU, sensores, comunicação CAN, HVIL e monitoramento de isolação;
- permissivos, desligamento de emergência e estados seguros conceituais;
- interfaces e uma matriz rastreável de dez falhas, reações propostas e pendências;
- sequência temporal conceitual da pré-carga com limiar, timeout e confirmação pendente dos contatores;
- diagramas comparativos das cadeias de controle V/f e FOC.

Não estão incluídos carregador embarcado, conector de recarga, homologação veicular,
software executável de controle, projeto mecânico, ensaios, análise térmica, EMC,
ASIL, HARA, FMEDA ou dimensionamento executivo.

## Pranchas

1. [Arquitetura geral](fonte/01_arquitetura_geral.dxf)
2. [Circuito de alta tensão](fonte/02_circuito_alta_tensao.dxf)
3. [Circuito de baixa tensão](fonte/03_circuito_baixa_tensao.dxf)
4. [Pré-carga e contatores](fonte/04_pre_carga_contatores.dxf)
5. [Inversor e motor](fonte/05_inversor_motor.dxf)
6. [Sensores e controle](fonte/06_sensores_controle.dxf)
7. [Rede de comunicação](fonte/07_rede_comunicacao.dxf)
8. [Layout dos componentes](fonte/08_layout_componentes.dxf)
9. [Interfaces e resposta conceitual a falhas](fonte/09_interfaces_resposta_falhas.dxf)
10. [Estudo paramétrico da pré-carga](fonte/10_estudo_pre_carga_parametrico.dxf)
11. [Sequência temporal da pré-carga](fonte/11_sequencia_temporal_pre_carga.dxf)

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Separação epistemológica

| Classe | Conteúdo usado neste projeto |
| --- | --- |
| Fato técnico | funções gerais de BMS, pré-carga, inversor, motor de indução, CAN e estratégias de controle, apoiadas nas referências declaradas |
| Premissa acadêmica | 400 V nominais, faixa 320-450 V, 60 kW, 60 kWh, 2.200 µF, 100 Ω, 12 V e comprimentos de cabos |
| Proposta conceitual | tags, topologia EV-07, limiares, mensagens CAN, estados e disposição física |
| Resultado experimental | nenhum; este projeto não contém medições, curvas de bancada, eficiência medida ou validação do TCC |

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- A folha 10 visualiza corrente inicial, potência instantânea e energia do resistor na faixa assumida de 320–450 Vcc; nenhum componente é selecionado por esses cálculos.
- A folha 11 aproxima a curva ideal do fluxo de estados; o tempo e a realimentação dos contatores permanecem pendentes do hardware.
- [Estratégias V/f e FOC](estrategias-controle.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Referências técnicas](referencias-normativas.md)
- [Parâmetros conceituais](parametros.csv)
- [Lista de sinais](lista-sinais.csv)
- [Matriz CAN](rede-can.csv)
- [Matriz de interfaces e falhas](matriz-interfaces-falhas.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de materiais](lista-materiais.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-arquitetura.json)
- [Validação estrita](validacao.json)

## Verificação da revisão 01

- oito fontes DXF AC1027 abertas e auditadas individualmente pelo Autodesk
  AcCoreConsole 2027, sem erro;
- 4.224 verificações específicas aprovadas, incluindo combinações de permissivos,
  pré-carga, habilitação de torque, tags, cálculos e coerência entre tabelas;
- validação estrita integrada aprovada em 272.953 verificações, sem erros nem avisos;
- 24 derivados examinados: oito PNGs de produção, oito PDFs reabertos e
  rasterizados pelo Poppler e oito SVGs abertos no Google Chrome;
- nova geração com hashes idênticos em 32/32 artefatos, sendo oito DXFs e 24
  derivados;
- nove testes automatizados aprovados.

## Revisão 02

A prancha 09 consolida dez eventos de perda de permissivo, pré-carga, soldagem de
contator, plausibilidade dos pedais, timeout CAN, limites térmicos/BMS, realimentação e
alimentação LV. A matriz liga sinais e documentos existentes às reações propostas e
expõe os dados de hardware e segurança ainda ausentes. Ela não é HARA, FMEA, ASIL,
validação de software ou comprovação de desligamento seguro. As oito pranchas anteriores
foram renumeradas para `NN/09` e reemitidas na revisão gráfica 02.

- AcCoreConsole 2027 abriu e auditou individualmente os nove DXFs, `PASS` em 9/9.
- Validador específico: 4.247 verificações, 0 erros.
- Validador estrito integrado: 501.282 verificações, 0 erros e 0 avisos.
- Revisor do portfólio: 12 projetos, 94 pranchas, 376 arquivos gráficos e 66 CSVs;
  similaridade mínima PDF/PNG de 0,9842.
- P07-09 foi inspecionada no PNG de produção e em raster do PDF; a folha de contato
  permitiu conferir numeração e composição das nove pranchas.
- A inspeção visual do SVG P07-09 no navegador aguarda autorização do usuário.

## Revisão 03

A prancha 10 amplia a memória de pré-carga com a curva RC normalizada e os esforços
calculados para 320, 400 e 450 Vcc. O conjunto nominal mantém `tau=0,22 s` e `t90` ideal
de `0,506569 s`; a faixa inclui até `220,52 J` dissipados no resistor ideal até 90% e
potência instantânea inicial de `2,025 kW` no caso de 450 V. Esses resultados expõem
exigências de pulso e repetição, sem selecionar RPR-701 ou validar o circuito físico.
As dez pranchas passam a usar numeração `NN/10` na revisão gráfica 03.

- O validador específico e a auditoria AutoCAD AcCoreConsole 2027 passaram em 10/10 DXFs.
- O validador P07 passou em 4.288 verificações; a validação estrita integrada passou
  em 630.151, ambas sem erros ou avisos.
- O revisor integrado confirmou 12 projetos, 106 folhas, 424 arquivos gráficos e
  73 CSVs, com similaridade mínima PDF/PNG de 0,981493; P07-10 obteve 0,989649.
- P07-10 foi inspecionada no PNG de produção a 300 dpi e no PDF rasterizado pelo
  Poppler a 150 dpi; não foram observados cortes ou sobreposição de conteúdo.
- A inspeção visual do SVG no navegador segue aguardando autorização do usuário.
- O modelo RC ideal não considera tolerâncias, impedâncias parasitas, filtros,
  tempo mecânico do contator, repetição nem capacidade térmica do resistor.

## Revisão 04

A prancha 11 organiza a sequência temporal entre permissivos, início da pré-carga,
cruzamento medido de 90%, confirmação auxiliar de KMP, abertura de KPR e liberação de
`READY`. A curva RC indica `t90=0,506569 s` e margem ideal de `0,993431 s` até o
timeout proposto de `1,5 s`. Se o limiar não for alcançado, o fluxo vai a `FAULT` com
torque inibido. Os tempos de movimento, feedback, tolerância do sensor e ordem real de
abertura ainda dependem do hardware e de análise de segurança.

- O validador específico P07 passou em 4.313 verificações e o AcCoreConsole 2027 abriu
  e auditou 11/11 DXFs. A validação estrita global mais recente passou em 650.961
  verificações, sem erros ou avisos; o revisor confirmou 12 projetos, 111 pranchas,
  444 arquivos gráficos e 75 CSVs, com similaridade mínima PDF/PNG de 0,981493.
- P07-11 foi conferida no PNG de produção a 300 dpi e no PDF rasterizado pelo Poppler
  a 150 dpi; similaridade PDF/PNG de 0,989502. Revisei a folha de contato das onze
  pranchas. O SVG ainda aguarda autorização para inspeção no navegador.

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 07-arquitetura-veiculo-eletrico\fonte\gerar_projeto_07.py --root .
.venv\Scripts\python.exe 07-arquitetura-veiculo-eletrico\fonte\validar_projeto_07.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 07-arquitetura-veiculo-eletrico\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
