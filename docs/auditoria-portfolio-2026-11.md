# Auditoria do portfólio CAD — 2026-11-06

## Escopo e critério

Revisei os 12 estudos, seus 105 DXFs e os derivados A3 para identificar qualidade de
apresentação, clareza do conteúdo, consistência entre documentos e maturidade real.
As folhas são material acadêmico/conceitual. A análise não concede aprovação de
engenharia, conformidade normativa ou liberação para fabricação e obra.

Na revisão atual, o revisor confirmou 12 projetos, 105 pranchas, 420 arquivos gráficos
e 72 CSVs, com similaridade mínima PDF/PNG de 0,981493. A validação estrita passou em
613.579 verificações, sem erros ou avisos.

## O que funciona bem

- A estrutura por projeto, a numeração de folhas, as listas e a separação de
  potência/comando/instrumentação tornam o conjunto navegável.
- P02 (instalação residencial) e P03 (painel com CLP) são os melhores pontos de
  entrada: associam planta/arquitetura a diagramas e tabelas rastreáveis.
- P04, P06 e P10 mostram variedade de instrumentação, acionamentos e interfaces;
  P07 amplia o portfólio para sistemas veiculares sem se passar por produto validado.
- O DXF como fonte e PDF/SVG/PNG reproduzidos a partir dele dão bons formatos de
  leitura, edição e conferência.

## Avaliação projeto a projeto

| Projeto | Bom | Simples ou fraco | Próxima substituição que mais agregaria |
| --- | --- | --- | --- |
| P01 — Painel com inversor | Separa unifilar, potência, comando, layout e campo; P01-07 mapeia premissas de proteção e P01-08 organiza evidências para verificação. | Não há estudo de coordenação nem ensaio funcional: Icc, modelos, curvas, ratings, critérios e resultados de campo seguem ausentes. | Substituir premissas por dados do local e modelos escolhidos; calcular e comparar curvas, definir critérios e anexar registros antes de declarar seletividade, capacidade ou funcionamento. |
| P02 — Residencial | Conjunto claro para leitura rápida; P02-09 agora liga dimensões/áreas por ambiente aos pontos, potências e circuitos em CSV. | A arquitetura continua fictícia, dimensões e cargas são premissas, e ainda não há levantamento de vãos nem potência de equipamentos selecionados. | Substituir a planta por levantamento cotado com vãos e medidas internas; informar equipamentos e potências escolhidos, então recalcular as cargas e circuitos. |
| P03 — Painel com CLP | Boa cobertura de alimentação, I/O, comando, bornes, interligações, sequência causa-efeito e plano de verificação em dez folhas. | O plano registra evidências necessárias, não resultados: nenhum teste de CLP ou segurança funcional foi executado; a resposta a sensor incoerente com bomba em marcha segue sem decisão. | Escolher hardware, fechar a decisão de processo e preencher o plano com critérios e evidências reais; validar a sequência no software do fabricante. |
| P04 — Nível | Agora mostra também sequência de operação e matriz causa–efeito para nove eventos, rastreada à filosofia existente. | A arquitetura ainda simplifica a instrumentação e as condições de processo; ação operacional para alarmes de nível 15%/85% e retenção na falta de energia dependem de decisão. | Evoluir o P&ID com dados de processo, válvulas/instrumentos selecionados e folhas de dados. |
| P05 — Instalação industrial | Traz layout, rotas, cargas, detalhes, seis pares de proteção em P05-08 e o plano de dados/evidências em P05-09. | Oficina e rotas são fictícias; Icc, capacidade de interrupção, modelos, curvas e seletividade seguem sem resultado. | Substituir premissas por dados da concessionária, levantamento, cabos e dispositivos escolhidos; calcular e comparar curvas antes de validar os pares. |
| P06 — CCM | Abrange partida direta, reversão, VFD, balanço de demanda e nove eventos; P06-10 lista individualmente os 24 bornes X3, os dez X4 e os condutores por cabo. | A demanda usa fatores assumidos e não prova simultaneidade. Proteções, capacidade de curto, método de instalação, diagnóstico KSR, falha VFD e rearme seguem sem validação executiva ou dados finais de fabricante. | Substituir fatores, Iz, disjuntor, seções e comprimentos por dados do processo, levantamento e método de instalação; escolher componentes e completar estudos de curto, coordenação e risco. |
| P07 — Veículo elétrico | Boa separação conceitual entre alta/baixa tensão, controle e comunicação; P07-09 relaciona dez falhas a sinais, estados e respostas propostas. | A arquitetura ainda não é esquema veicular homologável nem define segurança funcional; a matriz não prova diagnóstico ou desligamento seguro. | Substituir propostas por requisitos rastreados, hardware selecionado, análise de riscos e validação de software/ensaios conforme o escopo real. |
| P08 — Fotovoltaico | Tem arranjo, circuitos CC/CA, string box e aterramento; P08-07 torna explícita a sensibilidade da energia às premissas HSP/PR e lista dados necessários para estudo local. | Não comprova produtividade, sombreamento, configuração final ou aprovação de conexão. Os extremos mostrados são parâmetros didáticos escolhidos, não climatologia nem faixa de confiança. | Substituir parâmetros genéricos por local e equipamentos selecionados; usar fonte meteorológica, levantamento de sombras e modelo de produção apropriado antes de estimar energia. |
| P09 — Fonte de bancada | Conecta diagrama funcional, frente, arranjo interno, mecânica e interligações; topologia buck, pré-dimensionamento, descarga e sensibilidade das perdas agregadas estão documentados. | Os nove pares de eficiência são didáticos e não validam perdas reais ou temperatura. KD1/RD1 e KD2/RD2 continuam sem valores, intertravamento, tolerâncias ou ratings; não há seletividade, compensação, ensaio térmico nem análise EMI. | Substituir os cenários por curvas de perdas e componentes escolhidos; separar perdas por componente, fechar limites térmicos e EMI e validar o circuito e a descarga com critérios e ensaios rastreáveis. |
| P10 — Instrumentação | Boa listagem de instrumentos, arquitetura de rede, matriz de oito eventos, cinco pontos em quatro malhas 4–20 mA e balanço visual da fonte. | Tags, faixas e correntes de carga são premissas; limiares, fail state e respostas de processo não foram implementados em protocolo ou CLP. | Substituir premissas por instrumentos e hardware escolhidos, definir respostas por processo e testar timeouts/qualidade no protocolo implantado; conferir o consumo de cada modelo e o derating da fonte. |
| P11 — Subestação | Escopo amplo: arranjo físico, proteção, aterramento e SPDA; P11-07 agora rastreia dados e entregáveis do estudo de aterramento. | A revisão removeu o resultado aritmético de resistência sem dados medidos. Resistividade, falta, GPR/toque/passo e transferência seguem sem resultados; SPDA e classificação também não foram verificados. | Obter dados de campo e falta, definir método e critérios, calcular a malha e revisar os resultados antes de substituir o arranjo conceitual. |
| P12 — GMG/QTA | Cobre potência, bornes, painel, implantação, sequência, nove eventos e um cadastro legível dos quatro alimentadores QCE com origem nos cabos. | Potências, correntes, partida, simultaneidade e prioridade não têm dados de processo/OEM; os quatro ramais ainda não foram confirmados como lista completa, e o balanço real do GMG não está fechado. | Substituir os campos pendentes e extensões assumidas por dados de placa e levantamento; confirmar a abrangência do QCE e calcular demanda, degraus de carga e cabos antes de validar o conjunto e a sequência. |

## Correções desta revisão

- Escureci e separei as cores ACI usadas nas layers de sinal, comando, potência,
  cabos, cotas e arquitetura para que permaneçam distinguíveis sobre folha branca.
- Reemiti os carimbos em revisão gráfica 01 para a revisão anterior e em revisão 02
  para as ampliações funcionais; P09-09 elevou o conjunto a 89 folhas e P11-07 levou
  o portfólio a 90.
- Acrescentei P03-09 com sequência de operação e matriz causa-efeito. A prancha
  deixa explícito que a ação sobre bombas já em marcha diante de sensor incoerente
  segue como decisão pendente, sem completar essa lacuna por suposição.
- Acrescentei P04-07 com a sequência de partida e matriz de nove eventos e respostas,
  conforme a filosofia existente. A retenção de alarmes após perda de energia
  permanece dependente do PLC a selecionar; as respostas a LA-L/LA-H seguem pendentes.
- P09 recebeu as folhas 07 (topologia buck síncrona CC/CV), 08 (ondulação e
  pré-dimensionamento) e 09 (equações e estados paramétricos de descarga), além das
  listas de cálculo. LM5190 segue como candidato, não circuito validado.
- Em P09, 42 V aparece apenas como cenário de sensibilidade e a saída regulada inicia
  em 0,8 V. A folha 09 mantém as capacitâncias, tensões de falha, V_SAFE, tempo e
  ratings pendentes; K1 aberto não garante tensão zero, e KD2 depende de uma porta
  sem fonte externa e de intertravamento ainda não especificado.
- Acrescentei a P12-07, uma sequência visual com confirmação de falha, partidas,
  espera entre tentativas, transferência aberta, retorno e arrefecimento.
- Acrescentei P12-08 com nove eventos, resposta conceitual, alarme e retorno/limites.
  Corrigi a condição de rede para indicar duração superior a 3 s, conforme as
  premissas, e aumentei a tipografia da tabela para 1,45 mm. A causa de nível baixo
  de combustível e várias respostas da USCA/OEM continuam sem decisão documentada.
- Acrescentei P12-09 e `cadastro-cargas-qce.csv`, rastreando os quatro ramais QCE
  presentes em `lista-cabos.csv`. Potência, corrente, partida, regime e prioridade
  ficam `PENDENTE`; a prancha não inventa demanda nem afirma que os ramais listados
  sejam completos. A linha da moldura foi afastada da tabela após a inspeção de contato.
- Acrescentei P06-08 com nove eventos para emergência, sobrecargas, fins de curso,
  VFD, conflito de sentido e retorno de energia. Diagnóstico de KSR/VFD, sinalização
  e rearme de campo continuam dependentes dos dispositivos selecionados.
- Acrescentei P10-07 com oito eventos de qualidade analógica, perda de loop/remotas,
  SCADA, dados obsoletos, falha de 24 Vcc e DI. A matriz registra limites pendentes;
  não atribui diagnóstico, fail state ou ação final ao hardware ainda não selecionado.
- Acrescentei P10-08 com cinco pontos lineares em cada uma das quatro faixas 4–20 mA.
  Os valores são cálculos ideais derivados das faixas declaradas; não são calibração,
  ensaio de bancada ou critérios de aceitação.
- Acrescentei P10-09 para visualizar os sete grupos de carga existentes, a fonte proposta,
  a soma de 3,10 A e o saldo aritmético de 6,90 A. A reserva auxiliar de 1,05 A já está
  incluída na carga prevista; o desenho não atribui ramais nem seleciona proteções.
- Alinhei desenhos e simulação QTA nos tempos de referência e corrigi alegações de
  transferências impossíveis, polos e estados sem correspondência.
- Removi da documentação P11 os resultados PASS e a aprovação implícita do
  aterramento/SPDA; a estimativa restante da revisão anterior foi identificada como
  preliminar e acabou removida do desenho e da memória na revisão 02.
- Na revisão 02 do P11, removi da prancha 05 e da memória de cálculo a estimativa de
  resistência baseada em valores hipotéticos. A folha 07 e um CSV com 22 linhas agora
  registram as entradas e evidências ainda pendentes, sem produzir resultado de segurança.
- Na revisão 02 do P05, acrescentei P05-08 e uma matriz rastreável com seis pares de
  proteção; Icc, Icu/Ics, curvas, retaguarda e energia passante continuam pendentes.
- Na revisão 02 do P08, acrescentei uma prancha de sensibilidade com 12 cenários e o
  caso-base. HSP e PR são intervalos didáticos, sem dados meteorológicos nem previsão local.
- Na revisão 02 do P07, acrescentei a folha 09 e uma matriz CSV com dez eventos, detecção,
  estado, resposta proposta, pendência e rastreio. A matriz organiza interfaces; não é
  HARA/FMEA nem valida função de segurança. As outras oito folhas foram reemitidas como `/09`.
- Na revisão 02 do P01, acrescentei P01-07 e P01-08. As duas matrizes CSV rastreiam
  dados de proteção e evidências de verificação; nenhum item é declarado aprovado e
  nenhum ensaio de campo é apresentado como executado.
- Na revisão 02 do P02, acrescentei P02-09 e uma rastreabilidade por ambiente: oito
  áreas e 19 linhas de pontos totalizam as cargas atribuídas e remetem a lista de pontos
  e quadro de cargas. Os valores seguem como `PREMISSA`; a prancha não substitui a
  planta real nem um levantamento de equipamentos.
- Na revisão 03 do P03, acrescentei a prancha 10 e `plano-verificacao.csv` com 12
  pontos de verificação e evidências requeridas. Todos permanecem `NÃO EXECUTADO`; os
  tempos de premissa e a decisão sobre sensor incoerente não foram tratados como aprovados.
- Reemiti as oito folhas P05 na revisão 02 e conferi P05-08 em PNG integral e PDF
  rasterizado a 150 dpi; a folha de contato atual mostra as oito composições.
- Na revisão 03 do P05, acrescentei P05-09 e `dados-estudo-coordenacao.csv` com doze
  grupos de entradas, cálculos, comparações e evidências para os seis pares de proteção.
  Todos permanecem `PENDENTE`; nenhuma corrente de curto nem seletividade foi inventada.
- A revisão 02 reemitiu as sete folhas P11 como `/07`; a folha 05 deixa explícito que
  não há resultado da malha e P11-07 organiza os dados e entregáveis para o próximo estudo.
- Identifiquei relatórios de 2026-09-10 como históricos, pois cobrem P01–P10 e 68
  folhas. Os registros não validam a revisão atual nem P11/P12.

## Limites e validação

Os DXFs e derivados PDF/SVG/PNG de P01, P02, P05, P06, P07, P08, P09, P10, P11 e P12 foram regenerados. A
validação estrita aprovou 606.218 verificações, sem erros nem avisos. O revisor aprovou
12 projetos, 104 pranchas, 416 arquivos gráficos e 72 CSVs, com similaridade mínima
PDF/PNG de 0,981493. As 12 folhas de contato foram regeneradas; revisei as composições
P01 (oito folhas), P03 (dez), P04 (sete), P05 (nove), P06 (dez), P07 (nove), P08
(sete), P09 (dez), P10 (nove), P11 (sete) e P12 (nove).
O contato P02 foi conferido após a expansão para nove folhas. P02-01 foi conferida no
PNG integral; P02-09 foi inspecionada em PNG integral e PDF rasterizado a 150 dpi. O
AutoCAD AcCoreConsole 2027 auditou 9/9 DXFs P02 e o validador específico passou em 63
verificações, sem erros. A inspeção de SVGs P02-09 no navegador aguarda autorização.
A prancha P03-09 foi inspecionada no PNG integral de produção e em PDF
rasterizado a 150 dpi; tabela, fluxo, aviso e carimbo não apresentam cortes nem
colisões relevantes. P04-07 foi conferida em PNG e PDF rasterizado; também encontrei
e corrigi a tag TK-100 incoerente no fluxograma P04-01. As folhas
novas P09-07 e P09-08 foram inspecionadas em PNG integral e em PDF rasterizado a 150
dpi; na revisão 03, P09-06 e P09-09 foram inspecionadas no PNG integral e no PDF
rasterizado, e o contato atualizado das nove folhas P09 foi conferido. P07-09 foi
inspecionada no PNG de produção a 300 dpi e em PDF rasterizado a 150 dpi; o contato atual
das nove folhas P07 também foi conferido. O parser aceitou os
SVGs e seus viewBox; a inspeção visual no navegador dos SVGs P09, P03-09 e P04-07 está
pendente da autorização do usuário. P11-05 e P11-07 foram inspecionadas em PNG integral
e PDF rasterizado a 150 dpi; o contato das sete folhas confirmou revisão, numeração e
composição geral das demais. P08-07 foi inspecionada em PNG a 300 dpi e PDF rasterizado
a 150 dpi; conferi também a composição e a numeração das sete folhas no contato atualizado.
P12-07 e P12-08 foram
reinspecionadas em PNG e PDF rasterizado a 150 dpi; P12-09 foi inspecionada em PNG
integral, PDF rasterizado a 150 dpi e no contato atualizado das nove folhas. A inspeção
do contato revelou que a linha inferior do quadro tangenciava a última linha; ajustei a
tabela e regenerei PNG, PDF e SVG antes de validar. O AcCoreConsole 2027 auditou 9/9
DXFs P12, e o validador específico confirmou nove folhas, nove eventos, quatro ramais,
24 materiais e 15 cabos. P06-08 havia sido inspecionada em PNG integral e PDF rasterizado a
150 dpi; na revisão 03, P06-09 foi conferida em PNG integral e PDF rasterizado a 150 dpi,
e o contato atualizado das nove pranchas foi conferido. O AcCoreConsole 2027 abriu e
auditou 9/9 DXFs P06; o validador específico passou em 864 verificações, sem erros.
P10-07 foi
inspecionada em PNG de produção e PDF rasterizado a 150 dpi; as oito linhas cabem sem
cortes. Na revisão 04, P10-09 foi conferida no PNG de produção e em PDF rasterizado a
150 dpi; tabela, barra de carga, textos, notas e carimbo não apresentam cortes nem
colisões visíveis; o carimbo descreve corretamente o balanço da revisão. O contato das
nove folhas P10 foi conferido. O AcCoreConsole 2027 abriu e auditou 9/9 DXFs P10; o
validador específico passou com 64.353 verificações,
sem erros ou avisos. A inspeção de SVGs no navegador permanece pendente da autorização
do usuário. A matriz evita inventar estados de falha, timeouts ou respostas de processo
sem hardware definido.

O AutoCAD AcCoreConsole 2027 abriu e auditou os nove DXFs do P07 e os sete do P08, `PASS`
em 9/9 e 7/7. Essa auditoria confirma abertura e integridade CAD, sem validar projeto
elétrico ou normas.
O AutoCAD AcCoreConsole 2027 abriu e auditou 8/8 fontes do P01. P01-08 foi inspecionada
em PNG integral a 300 dpi e em PDF rasterizado independentemente pelo Poppler a 150 dpi;
também conferi o contato atualizado das oito folhas. Sua similaridade PDF/PNG foi
0,984095. O navegador ainda não foi usado para conferir SVGs; essa etapa aguarda
autorização do usuário. P02, P03 e P05 também foram abertos e auditados no AcCoreConsole;
P09 também foi auditado em 10/10 DXFs na revisão 04. Os demais projetos não foram
reabertos no AutoCAD nesta revisão. Essas auditorias confirmam abertura/integridade CAD,
sem validar projeto elétrico, dimensionamento ou conformidade normativa.
O mesmo cuidado vale para FreeCAD, KiCad e uma IDE de CLP: seus artefatos não foram
aprovados dentro dos aplicativos nativos.

Use esta auditoria para priorizar o próximo ciclo; não use nenhuma das folhas como
documento de execução. Os próximos avanços de maior valor são fechar a coordenação de
P05 com curvas e impedâncias reais, fazer análise local de produção e sombras para P08,
concluir verificações térmicas/EMI em P09 e obter dados de campo para o estudo de
segurança da malha de P11.

### Atualização P03-10 — revisão 03

A nova prancha foi conferida no PNG de produção a 300 dpi, no PDF rasterizado pelo
Poppler a 150 dpi e na composição atual das dez folhas. Os doze itens são legíveis e
estão marcados `NÃO EXECUTADO`; o status não afirma resultados de campo. A planilha
mantém como decisão pendente a resposta a sensor incoerente com bomba em marcha. O
AcCoreConsole 2027 abriu e auditou os dez DXFs do P03, e o validador lógico passou em
232 verificações. A revisão integral passou em 544.721 verificações; o revisor confirmou
99 pranchas, 396 arquivos gráficos, 71 CSVs e similaridade mínima PDF/PNG de 0,984061.
O SVG ainda aguarda inspeção visual no navegador, conforme a autorização pendente.

### Atualização P05-09 — revisão 03

A prancha foi conferida no PNG de produção a 300 dpi, no PDF rasterizado pelo Poppler a
150 dpi e no contato das nove folhas P05. Fluxo e tabela cabem na folha; os doze grupos
de dados continuam `PENDENTE`. O AutoCAD AcCoreConsole 2027 abriu e auditou 9/9 DXFs
P05; o validador específico passou em 378 verificações. A validação estrita atual passou
em 544.721 verificações e o revisor confirmou 99 pranchas, 396 arquivos gráficos e 71
CSVs. A inspeção visual dos SVGs no navegador continua aguardando autorização.

### Atualização P09-10 — revisão 04

A matriz cruza nove pares de eficiência hipotéticos a POUT=150 W e separa perdas
agregadas em PS1 e REG1. O cenário central totaliza 31,2 W; a varredura vai de 50,5 W
a 14,5 W. Esses resultados são apenas balanços paramétricos, não medições, curvas de
fabricante ou estimativas térmicas. A inspeção no PNG a 300 dpi, PDF rasterizado a 150
dpi e contato atualizado das dez folhas não encontrou cortes ou colisões após mover os
quadros inferiores para fora da área da legenda. O validador específico passou em
18.846 verificações e o AcCoreConsole 2027 abriu/auditou 10/10 DXFs P09. A validação
estrita passou em 544.721 verificações; o revisor confirmou 12 projetos, 99 folhas,
396 arquivos gráficos, 71 CSVs e similaridade mínima PDF/PNG de 0,984061. A inspeção
visual dos SVGs no navegador permanece aguardando autorização do usuário.

### Atualização P10-08 — revisão 03

A nova matriz mostra TT-101, PT-102, FT-103 e LT-104 em 4, 8, 12, 16 e 20 mA,
com valores convertidos nas unidades de engenharia declaradas. A verificação de
16.001 pontos por malha e a matriz de 20 linhas passaram; os cálculos são lineares e
ideais, sem alegação de calibração ou ensaio. A fonte e os derivados foram regenerados;
na inspeção do PNG a 300 dpi, do PDF rasterizado a 150 dpi e do contato das oito folhas,
os dados, marcadores, notas e carimbo ficaram dentro da moldura sem colisões visíveis.
O texto da tabela foi ampliado para 1,8 mm após a primeira inspeção. O AcCoreConsole
2027 abriu e auditou 8/8 DXFs P10; o validador específico passou em 64.309 verificações.
O portfólio passou em 549.703 verificações estritas, sem erros ou avisos. A revisão
integrada confirmou 12 projetos, 100 folhas, 400 arquivos gráficos, 71 CSVs e
similaridade mínima PDF/PNG de 0,984061. A inspeção visual do SVG no navegador segue
pendente da autorização do usuário.

### Atualização P10-09 — revisão 04

A prancha transforma o conteúdo de `lista-alimentacao.csv` em uma tabela e uma barra
de capacidade: sete grupos totalizam 3,10 A / 74,40 W diante da fonte proposta de
10 A / 240 W. O gráfico separa 31% de carga prevista de 69% de saldo aritmético. A
reserva auxiliar prevista de 1,05 A já está incluída nos 3,10 A. Não foi criada
distribuição por ramais nem seleção de fusíveis. Os resultados da inspeção visual e das
validações são: 64.353 verificações do P10 e 555.195 no validador estrito, ambos sem
erros ou avisos; 9/9 DXFs abertos e auditados no AcCoreConsole 2027. A prancha foi
conferida no PNG a 300 dpi, em PDF rasterizado a 150 dpi e no contato das nove folhas,
sem cortes ou colisões visíveis. A inspeção de SVGs no navegador segue aguardando
autorização do usuário. O revisor integrado confirmou 12 projetos, 101 folhas, 404
arquivos gráficos, 71 CSVs e similaridade mínima PDF/PNG de 0,984061.

### Atualização P06-09 — revisão 03

A nova folha consolida os fatores de demanda registrados por motor, potências ativa
e aparente instaladas e demandadas e as correntes de projeto dos ramais. O W600 usa
19,133709 kVA demandados para obter 29,070663 A; o disjuntor de 50 A e Iz de 57 A são
dados assumidos dos CSVs. A relação aritmética `Ib <= In <= Iz` não valida instalação,
capacidade térmica, correções, Icc ou seletividade. P06-09 foi inspecionada no PNG a
300 dpi, no PDF rasterizado a 150 dpi e no contato das nove folhas, sem cortes ou
colisões visíveis. O AcCoreConsole 2027 auditou 9/9 DXFs; o validador P06 passou em
864 verificações e o estrito em 566.931, sem erros ou avisos. O revisor integrado
confirmou 12 projetos, 103 folhas, 412 arquivos gráficos e 72 CSVs, com similaridade
mínima PDF/PNG de 0,984061. A inspeção visual dos SVGs no navegador permanece pendente
de autorização do usuário.

### Atualização P06-10 — revisão 04

A nova prancha lista os 24 bornes X3 e dez bornes X4 individualmente, com condutor,
função, cabo e destino. Corrigi a atribuição do W604 para os dois canais físicos de
emergência, separei STO A/B como ligação interna KSR-601–VFD-603 e alinhei W605–W608
com as posições do quadro X3/X4. O validador P06 passou em 912 verificações; o estrito
passou em 606.218 sem erros ou avisos. O AcCoreConsole 2027 auditou 10/10 DXFs. P06-05,
P06-06 e P06-10 foram conferidas em PDF rasterizado a 150 dpi e o contato atualizado das
dez folhas foi inspecionado. O revisor integrado confirmou 12 projetos, 104 folhas,
416 arquivos gráficos e 72 CSVs, com similaridade mínima PDF/PNG de 0,981493. Os modelos
de fabricante, cores dos condutores, dimensionamento, ajustes e validação funcional
continuam pendentes; a inspeção de SVGs no navegador aguarda autorização.

### Atualização P10-10 — revisão 05

Corrigi a identificação genérica `X2` dos alimentadores P24-201/202 para X2:03/04 e
X2:05/06 e reconciliei cada cabo com PE-101, a lista de bornes e uma nova prancha de
interligação. Também separei FU1 (PLC/SW) de FU4 (distribuição comum de campo em
X2:01/02), removendo a ambiguidade anterior. O validador P10 passou em 64.395
verificações; o portfólio passou em 613.579 verificações estritas, sem erros ou avisos.
O revisor confirmou 12 projetos, 105 pranchas, 420 arquivos gráficos e 72 CSVs; a
similaridade mínima PDF/PNG foi 0,981493 e P10-10 obteve 0,988205. O AcCoreConsole
2027 auditou 10/10 DXFs P10. A nova folha e as folhas 01/03 foram conferidas na
produção; P10-10 também foi conferida em rasterização independente do PDF a 150 dpi e
no contato das dez folhas, sem cortes ou colisões relevantes. Ratings, coordenação,
dimensionamento e seleção final de proteção seguem pendentes. A inspeção visual dos
SVGs no navegador continua aguardando autorização.

### Atualização P12-09 — revisão 03

A prancha e o CSV apresentam os quatro alimentadores de cargas essenciais encontrados
na lista de cabos: iluminação/rotas, bomba de incêndio, UPS da sala de servidores e
utilidades. As formações e extensões são transcritas como premissas existentes; os
dados de potência, corrente, partida, simultaneidade e prioridade permanecem pendentes.
P12-09 foi conferida no PNG de produção a 300 dpi, em PDF rasterizado independentemente
a 150 dpi e no contato das nove folhas. O AcCoreConsole 2027 auditou 9/9 DXFs P12; o
validador específico passou com nove pranchas, quatro ramais QCE, nove eventos, 24
materiais e 15 cabos. O validador estrito aprovou 566.931 verificações; o revisor
confirmou 12 projetos, 103 folhas, 412 arquivos gráficos e 72 CSVs, similaridade
mínima de 0,984061. A inspeção dos SVGs no navegador segue aguardando autorização.
