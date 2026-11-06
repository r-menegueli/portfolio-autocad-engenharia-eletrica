# Auditoria do portfólio CAD — 2026-11-06

## Escopo e critério

Revisei os 12 estudos, seus 114 DXFs e os derivados A3 para identificar qualidade de
apresentação, clareza do conteúdo, consistência entre documentos e maturidade real.
As folhas são material acadêmico/conceitual. A análise não concede aprovação de
engenharia, conformidade normativa ou liberação para fabricação e obra.

Na revisão corrente, o revisor confirmou 12 projetos, 114 pranchas, 456 arquivos
gráficos e 77 CSVs, com similaridade mínima PDF/PNG de 0,981493. A validação estrita
passou em 668.075 verificações, sem erros ou avisos.

## O que funciona bem

- A estrutura por projeto, a numeração de folhas, as listas e a separação de
  potência/comando/instrumentação tornam o conjunto navegável.
- P02 (instalação residencial) e P03 (painel com CLP) são os melhores pontos de
  entrada: associam planta/arquitetura a diagramas e tabelas rastreáveis.
- P04, P06 e P10 mostram variedade de instrumentação, acionamentos e interfaces;
  P07 amplia o portfólio para sistemas veiculares; P07-11 separa o tempo RC ideal,
  o retorno dos contatores e o timeout sem afirmar validação veicular. P03-11 coloca
  lado a lado as interpretações de enchimento e esgotamento sem escolher uma lógica.
- O DXF como fonte e PDF/SVG/PNG reproduzidos a partir dele dão bons formatos de
  leitura, edição e conferência.

## Avaliação projeto a projeto

| Projeto | Bom | Simples ou fraco | Próxima substituição que mais agregaria |
| --- | --- | --- | --- |
| P01 — Painel com inversor | Separa RUN, STOP, reset do VFD e rearme KSR1; acrescenta sequência visual de habilitação, operação e eventos em P01-09; mantém proteção e verificação em matrizes rastreáveis. | Sem modelos/OEM, a pinagem DI/STO e os blocos de contato permanecem pendentes; Icc, curvas, coordenação e ensaios de campo não existem. P01-08 tem 13 itens, todos NÃO EXECUTADO; a sequência P01-09 é conceitual. | Substituir premissas por dados do local e modelos escolhidos; fechar os mapeamentos com os manuais, calcular e comparar curvas e anexar critérios/evidências antes de declarar seletividade, capacidade ou funcionamento. |
| P02 — Residencial | A revisão 04 acrescenta P02-10, que separa cargas 127 V fase-neutro de C6/C7 a 220 V fase-fase e calcula cotas superiores aritméticas por condutor a partir do quadro CSV. Retira a divisão agregada de demanda por 220 V e a antiga indicação de QG1 63 A. | Planta e mobiliário ainda são fictícios; dimensões e posições dos vãos são premissas. As cotas de P02-10 não são demanda nem correntes fasoriais; o método de demanda, alimentador e QG1 continuam pendentes. Ergonomia, acessibilidade e iluminação/ventilação natural não foram verificadas. | Substituir arquitetura e esquadrias por levantamento cotado; confirmar uso, cargas e simultaneidade; definir método por fase e dados de instalação antes de dimensionar alimentador, QG1, DR e proteção. |
| P03 — Painel com CLP | Onze folhas cobrem alimentação, I/O, comando, bornes, interligações, sequência, plano de verificação e a comparação P03-11 entre enchimento e esgotamento. | O sentido real, tanques e função de LSL-LL continuam pendentes; LSHH e a resposta a sensor incoerente em marcha não foram decididos. Nenhum teste de CLP ou segurança funcional foi executado. | Aprovar V01 com dados do processo, localizar cada sensor, confirmar reservatório/captação e revisar demanda/parada, LSHH, falhas, I/O e matriz antes de implementar ou ensaiar. |
| P04 — Nível | Nove folhas cobrem processo, malha, elétrica, interligações, layout, nove eventos causa–efeito, levantamento D01–D07 e o método de balanço NPSHa versus NPSHr. A revisão 05 deixa fonte, fluido, pressão, geometria e critérios sem valores inventados. | Sistema de uma bomba e um tanque com valores assumidos; fonte, vazão/carga, curva OEM, fluido e proteção não estão selecionados. P04-09 explica o método, mas não calcula NPSHa, NPSHr ou margem sem dados. Ação para LA-L/LA-H e retenção de alarmes após falta de energia dependem do processo e do PLC. | Substituir premissas por levantamento hidráulico e dados OEM; preencher D01–D07 com valores e evidências, verificar unidades e datum, avaliar combinações operacionais reais e aplicar a margem pertinente; completar respostas de processo antes da validação. |
| P05 — Instalação industrial | Traz layout, rotas, cargas, detalhes, seis pares de proteção em P05-08 e um roteiro verificável em P05-09. A P05-01 agora relaciona C01–C06, potência aparente instalada e coordenadas derivadas do croqui. | Oficina e rotas são fictícias; a tabela não acrescenta pegadas, áreas de operação, fluxo nem obstáculos. Icc, capacidade de interrupção, modelos, curvas e seletividade seguem sem resultado. | Para demonstrar implantação, substituir o croqui por levantamento cotado com envelopes OEM, folgas, acessos e fluxo. Separadamente, obter dados de rede e dispositivos para calcular Icc e comparar curvas antes de validar os pares. |
| P06 — CCM | Abrange partida direta, reversão, VFD, balanço de demanda e nove eventos; P06-10 lista individualmente os 24 bornes X3, os dez X4 e os condutores por cabo. | A demanda usa fatores assumidos e não prova simultaneidade. Proteções, capacidade de curto, método de instalação, diagnóstico KSR, falha VFD e rearme seguem sem validação executiva ou dados finais de fabricante. | Substituir fatores, Iz, disjuntor, seções e comprimentos por dados do processo, levantamento e método de instalação; escolher componentes e completar estudos de curto, coordenação e risco. |
| P07 — Veículo elétrico | Boa separação conceitual entre alta/baixa tensão, controle e comunicação; P07-09 relaciona dez falhas a sinais, estados e respostas propostas; P07-10 calcula a pré-carga ideal; P07-11 relaciona o limiar medido, feedback de KMP/KPR, READY e timeout. | A arquitetura ainda não é esquema veicular homologável nem define segurança funcional; a matriz não prova diagnóstico/desligamento seguro e os desenhos não validam resistor, contatores ou circuito real. | Substituir R/C e faixa de tensão por valores e tolerâncias de componentes escolhidos; verificar pulso, repetição, temperatura, falha de contator e critérios de isolamento com requisitos do sistema, simulação transitória e ensaios rastreáveis. |
| P08 — Fotovoltaico | Tem arranjo, circuitos CC/CA, string box e aterramento; P08-07 torna explícita a sensibilidade da energia às premissas HSP/PR e lista dados necessários para estudo local. | Não comprova produtividade, sombreamento, configuração final ou aprovação de conexão. Os extremos mostrados são parâmetros didáticos escolhidos, não climatologia nem faixa de confiança. | Substituir parâmetros genéricos por local e equipamentos selecionados; usar fonte meteorológica, levantamento de sombras e modelo de produção apropriado antes de estimar energia. |
| P09 — Fonte de bancada | Conecta diagrama funcional, frente, arranjo interno, mecânica e interligações; topologia buck, pré-dimensionamento, descarga e sensibilidade das perdas agregadas estão documentados. | Os nove pares de eficiência são didáticos e não validam perdas reais ou temperatura. KD1/RD1 e KD2/RD2 continuam sem valores, intertravamento, tolerâncias ou ratings; não há seletividade, compensação, ensaio térmico nem análise EMI. | Substituir os cenários por curvas de perdas e componentes escolhidos; separar perdas por componente, fechar limites térmicos e EMI e validar o circuito e a descarga com critérios e ensaios rastreáveis. |
| P10 — Instrumentação | Boa listagem de instrumentos, arquitetura de rede, matriz de oito eventos, cinco pontos em quatro malhas 4–20 mA e balanço visual da fonte. | Tags, faixas e correntes de carga são premissas; limiares, fail state e respostas de processo não foram implementados em protocolo ou CLP. | Substituir premissas por instrumentos e hardware escolhidos, definir respostas por processo e testar timeouts/qualidade no protocolo implantado; conferir o consumo de cada modelo e o derating da fonte. |
| P11 — Subestação | Escopo amplo: arranjo físico, proteção, aterramento e SPDA; P11-07 rastreia 22 entradas e P11-08 cruza solo/falta/geometria com quatro verificações. A P11-02 agora declara arranjo conceitual e `S/ESC.` após a correção da escala gráfica inválida. | Não há dados para resistência, GPR/toque/passo ou transferência; SPDA e classificação também não foram verificados. A planta continua sem levantamento, envelopes OEM ou rotas confirmadas. | Obter levantamento, desenhos OEM, acessos/rotas de retirada e dados de falta. Só então substituir o esquema por implantação cotada; executar e revisar a análise da malha com método e critérios aplicáveis. |
| P12 — GMG/QTA | Cobre potência, bornes, painel, implantação, sequência, nove eventos e um cadastro legível dos quatro alimentadores QCE com origem nos cabos. A P12-06 declara dimensões de estudo e `S/ESC.`. | Potências, correntes, partida, simultaneidade e prioridade não têm dados de processo/OEM; os quatro ramais ainda não foram confirmados como lista completa, e o balanço real do GMG não está fechado. A planta não mostra rotas físicas completas de ar e escape. | Substituir o esquema por arranjo do local baseado no modelo OEM, com insuflação, descarga, escape, combustível, manutenção e afastamentos. Obter placas e confirmar cargas QCE para fechar demanda, degraus e cabos. |

## Leitura visual direta de pranchas representativas

Esta leitura separa a simplicidade gráfica da falta de informação de engenharia. Diagramas de blocos e matrizes podem ser simples por escolha e ainda assim comunicar bem; ficam fracos quando ocupam uma prancha de implantação sem mostrar a geometria que o título promete.

- **P02-01 — planta residencial:** é uma das folhas mais fáceis de ler. Planta, áreas, mobiliário, portas/janelas e cotas gerais aparecem juntos, com escala e ressalva de premissas. A principal limitação é a origem fictícia da arquitetura, não a apresentação. Para virar projeto de um imóvel, substituir a base por levantamento real e revisar vãos, circulação e conforto; não acrescentar detalhe decorativo antes disso.
- **P01-04 — layout interno do painel:** a separação dos componentes, canaletas e bornes torna o arranjo legível. O desenho funciona como estudo de ocupação, mas ainda usa blocos conceituais; dimensões de fabricante, dissipação, ventilação, acessibilidade e raios de curvatura é que determinariam se o layout cabe e pode ser montado.
- **P03-11 — alternativas de processo:** a comparação lado a lado de enchimento e esgotamento é simples e eficaz para expor a decisão que falta. Eu a manteria como folha de decisão; o próximo passo é registrar V01 e revisar a lógica, não encher a prancha com símbolos antes de saber qual processo existe.
- **P05-01 — layout industrial:** a tabela nova melhora a rastreabilidade de máquinas, circuitos, cargas e coordenadas do croqui, e cabe bem na folha. A densidade geométrica continua baixa: máquinas e quadros são símbolos sem envelopes, áreas de operação/manutenção, fluxo de material ou confronto com obstáculos. Eu a manteria como esquema didático e a substituiria por planta levantada quando houver local e equipamentos definidos.
- **P11-02 — planta da subestação:** os cubículos e o transformador são identificáveis. A revisão removeu a indicação de 1:50 incompatível com o desenho e agora declara `S/ESC.`, cotas externas como premissas e pendências de levantamento/OEM. A geometria continua esquemática; faltam afastamentos confirmados, acessos, retirada e compatibilização com dimensões reais.
- **P12-06 — sala do gerador:** agora declara `S/ESC.`, dimensões como premissas e dependência de dados do fabricante. O grupo e o painel estão localizados, mas escape, atenuadores e ventilação aparecem como elementos esquemáticos sem percurso físico completo. A substituição útil depende do modelo OEM e do local para desenhar insuflação, descarga, escape, combustível, manutenção e afastamentos.
- **P09-05 — detalhes mecânicos:** apresenta vistas frontal/lateral e posições de recortes, então já comunica a forma geral do gabinete. Ainda é simples como desenho de fabricação: não define material/espessura, tolerâncias, raios, acabamento, fixadores ou processo. Manter como conceito ou substituir por desenho cotado apenas quando houver gabinete e componentes escolhidos.
- **P08-06 — layout fotovoltaico:** separa cobertura, parede técnica e rotas CC/CA, além de enumerar critérios pendentes. Para a disposição física ainda é um esquema: faltam telhado levantado, obstáculos/sombreamento, zonas de acesso e posição confirmada dos equipamentos.

## Ordem recomendada para substituir ou aprofundar

1. **Primeiro, substituir as implantações mais esquemáticas quando houver dados reais:** P05-01, P11-02 e P12-06. A tabela e as ressalvas adicionadas melhoram a leitura, mas não substituem levantamento, envelopes OEM, acessos, rotas e afastamentos cotados.
2. **Depois, trocar premissas por dados que fecham cálculos:** P02 (levantamento e cargas), P04 (fonte, vazão e curva da bomba), P05 (curto-circuito e curvas), P06 (motores, instalação e simultaneidade), P08 (local, módulos, inversor e sombras) e P12 (placas e lista completa de cargas). Até esses dados chegarem, preservar os campos como pendentes.
3. **Para fabricação e operação:** P09-05 só vira desenho de fabricação com componentes, material e tolerâncias definidos; P01 e P06 precisam de pinagem/documentação OEM e evidências de verificação antes de qualquer afirmação de funcionamento ou segurança.

**O que está mais simples hoje:** P05-01 e P11-02 em densidade geométrica; P12-06 e P09-05 em detalhamento físico. **O que está simples de propósito e funciona:** P03-11 como comparação de decisão e as folhas-matriz de verificação. A simplicidade dessas folhas de decisão comunica as pendências; aumentar a geometria só agrega quando vier de levantamento e dados de equipamento.

## Correções desta revisão

- Escureci e separei as cores ACI usadas nas layers de sinal, comando, potência,
  cabos, cotas e arquitetura para que permaneçam distinguíveis sobre folha branca.
- Reemiti os carimbos em revisão gráfica 01 para a revisão anterior e em revisão 02
  para as ampliações funcionais; P09-09 elevou o conjunto a 89 folhas e P11-07 levou
  o portfólio a 90.
- Acrescentei P03-09 com sequência de operação e matriz causa-efeito. A prancha
  deixa explícito que a ação sobre bombas já em marcha diante de sensor incoerente
  segue como decisão pendente, sem completar essa lacuna por suposição.
- Na revisão 04 do P03, corrigi a documentação para parar antes da implementação: o
  memorial dizia “enchimento”, mas a sequência LSH-inicia/LSL-encerra/LSHH-reserva pode
  corresponder a esgotamento. A prancha 09 destaca o ponto, e V01 agora exige direção,
  tanques e função dos sensores, inclusive LSL-LL. A incerteza de sensor incoerente com
  bomba em marcha continua separada e pendente.
- Na revisão 03 do P04, removi do fluxograma a representação de um segundo TK-101
  e explicitei a origem a montante como limite não especificado. Corrigi a legenda
  para descrever o sinal e a HV-102 desenhada; incluí essa válvula na lista de
  materiais e no workbook, com tipo, diâmetro e pressão pendentes. As sete fontes
  passaram no AcCoreConsole 2027; a planilha conta agora 18 materiais. LA-L/LA-H,
  dimensionamento hidráulico e retenção de alarmes continuam sem decisão ou ensaio.
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
- Na revisão funcional/documental 03 do P01, separei os comandos RUN, STOP e reset do
  VFD, incluí S5 para rearme manual monitorado do KSR1 e acrescentei V13 para verificar
  que os rearmes são independentes e não produzem partida. Os 13 itens seguem
  `NÃO EXECUTADO`; o diagrama não fixa bornes sem seleção do fabricante. As oito fontes
  passaram no AcCoreConsole 2027 e no validador estrito; P01-03 e P01-08 foram conferidas
  em PNG integral e PDF rasterizado a 150 dpi.
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

## Limites e validação — relatórios históricos

Os números de validação neste bloco antecedem a revisão corrente registrada no início
deste relatório; foram mantidos como histórico de revisões anteriores. Os DXFs e
derivados PDF/SVG/PNG de P01, P02, P05, P06, P07, P08, P09, P10, P11 e P12 foram regenerados. A
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
colisões relevantes. P04-07 foi conferida em PNG e PDF rasterizado. Na revisão 03,
removi a duplicação anterior de TK-101 em P04-01; a nova folha foi conferida em PNG
integral e PDF rasterizado, e P04-02 em PNG integral. As folhas
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

### Atualização P05-09 — revisão 04

Reformulei o fluxo de cinco etapas para apontar entradas D01-D06, modelo D07, cálculo de
Icc máximo/mínimo por ponto D08, verificações D09-D11 e fechamento D12. A tabela mantém
os doze grupos `PENDENTE`. Removi de critérios, memorial, lista de materiais, unifilar e
coordenação os valores presumidos de 6 kA e Icu de 10 kA; não há fonte nem cálculo que
os sustente. O AutoCAD AcCoreConsole 2027 auditou 9/9 DXFs, todos com zero erros e zero
correções; o validador específico passou em 406 verificações. A rasterização independente
do PDF e o PNG de produção de P05-09 tiveram similaridade 0,984839; o contato das nove
folhas foi conferido. A validação estrita passou em 652.258 verificações, sem erros ou
avisos, e a inspeção visual dos SVGs pelo navegador continua aguardando autorização.

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

### Atualização P02-01 a P02-09 — revisão gráfica 03

A planta residencial agora mostra as paredes interrompidas nos vãos, acesso ao Quarto 2
e ao banheiro pela circulação, closet acessado pelo Quarto 1, mobiliário indicativo e
agenda rastreável de oito portas e sete janelas. Corrigi os arcos das portas e acrescentei
um ponto de luz e eletroduto para o closet. O quadro de cargas passou a calcular seus
totais a partir dos circuitos; apresenta 15.558,696 VA instalados e 12.595,543 VA de
demanda acadêmica. A matemática do P02 passou em 68 checagens, o AcCoreConsole 2027
auditou 9/9 DXFs e os nove PNGs integrais foram inspecionados. O revisor passou em
12 projetos, 105 folhas, 420 arquivos gráficos e 73 CSVs, sem erros, e a similaridade
mínima PDF/PNG do P02 foi 0,984878. O validador estrito aprovou 623.879 verificações,
sem erros ou avisos. Os dados arquitetônicos, cargas e proteções continuam premissas;
curto-circuito, seletividade, projeto executivo e conformidade normativa não foram
verificados. A inspeção dos SVGs no navegador aguarda autorização do usuário.

### Atualização P03-09 — revisão 04

A folha e os documentos agora apresentam um ponto de parada formal: a descrição anterior
previa enchimento, mas a sequência LSH inicia / LSL encerra / LSHH chama a reserva pode
corresponder a esgotamento. A V01 exige a direção real do processo, os tanques de
origem/destino e a localização/função dos sensores, incluindo LSL-LL, antes da
implementação. O comportamento diante de sensor incoerente com bomba em marcha continua
pendente de decisão. P03-09 foi inspecionada no PNG de produção a 300 dpi e em PDF
rasterizado a 150 dpi; o AutoCAD AcCoreConsole 2027 auditou 10/10 fontes DXF do projeto,
incluindo a folha atualizada. O validador específico passou em 235 verificações e o
estrito em 624.834, ambos sem erros ou avisos. O revisor confirmou 12 projetos, 105
pranchas, 420 arquivos gráficos e 73 CSVs, com similaridade mínima PDF/PNG de 0,981493.
Os 12 itens de verificação seguem `NÃO EXECUTADO`; a inspeção do SVG no navegador
continua aguardando autorização.

### Atualização P07-10 — revisão gráfica 03

A nova folha apresenta a resposta RC normalizada e cálculos a 320/400/450 V com as
premissas já publicadas (100 Ω, 2,2 mF, limite de 90% e timeout de 1,5 s). O tempo ideal
para 90% é 0,506569 s; em 450 V a corrente inicial é 4,50 A, a potência instantânea
inicial 2,025 kW e a energia dissipada até 90% é 220,52 J. Esse resultado recomenda
priorizar a seleção do resistor por energia de pulso, repetição e condições térmicas;
não confirma qualquer modelo comercial nem a segurança do veículo. O validador
específico passou em 4.288 verificações e o AcCoreConsole 2027 abriu/auditou 10/10 DXFs.
P07-10 foi inspecionada no PNG de produção a 300 dpi e no PDF rasterizado a 150 dpi.
O revisor integrado confirmou 12 projetos, 106 folhas, 424 arquivos gráficos e 73 CSVs,
com similaridade mínima PDF/PNG de 0,981493; P07-10 obteve 0,989649. A validação estrita
passou em 630.151 verificações, sem erros ou avisos àquela revisão. A inspeção do SVG no
navegador permanece pendente de autorização.

### Atualização P08-08 — revisão gráfica 03

A prancha nova transforma as premissas térmicas já existentes em curvas e tabela por
string: Voc/Vmp a -5 °C, STC e 70 °C, mais Isc corrigida em 1.100 W/m². Para as seis
unidades em série, Voc fria é 324,5496 V, Vmp quente 216,942 V e Isc no caso quente
15,65652 A. A Isc não representa a Imp operacional; faltam módulos e inversor reais,
curva I-V, dados OEM e validação da entrada de corrente do MPPT.

O validador específico passou em 8.119 verificações; o AcCoreConsole 2027 abriu e
auditou 8/8 DXFs. P08-08 foi inspecionada no PNG a 300 dpi, PDF rasterizado independente
a 150 dpi e contato das oito folhas; similaridade PDF/PNG da nova folha: 0,989722.
O revisor confirmou 12 projetos, 107 folhas, 428 arquivos gráficos e 74 CSVs; o mínimo
global de similaridade permaneceu 0,981493. A validação estrita passou em 634.464
verificações, sem erros ou avisos. A inspeção de SVGs no navegador aguarda autorização.

### Atualização P07-11 — revisão gráfica 04

A nova prancha separa a resposta RC ideal da sequência de confirmação dos contatores.
Com R=100 ohm, C=2,2 mF e limiar proposto de 90%, `t90=0,506569 s` e a margem
aritmética até o timeout de 1,5 s é `0,993431 s`. A sequência deixa explícitos o
fechamento solicitado de KMP, o retorno auxiliar ainda sem tempo definido, a abertura
de KPR antes de `READY` e o ramo `FAULT` por timeout, mantendo torque inibido.

O validador específico P07 passou em 4.313 verificações e o AcCoreConsole 2027 abriu e
auditou 11/11 DXFs. P07-11 foi conferida no PNG a 300 dpi, PDF rasterizado pelo Poppler
a 150 dpi e contato das onze folhas; a similaridade PDF/PNG foi 0,989502. A revisão
integrada confirmou 12 projetos, 108 folhas, 432 arquivos gráficos e 74 CSVs, com
similaridade mínima de 0,981493. A validação estrita passou em 637.814 verificações,
sem erros ou avisos. Tempos de contatores, retorno auxiliar e critérios de segurança
seguem pendentes de hardware e validação veicular; SVGs aguardam autorização para
inspeção no navegador.

### Atualização P03-11 — revisão 05

P03-11 compara dois exemplos condicionais para a instalação de duas bombas: demanda em
LSL e parada em LSH para enchimento; demanda em LSH e parada em LSL para esgotamento.
Nenhuma alternativa foi selecionada. Ação de LSHH, localização de LSL-LL e resposta a
sensor incoerente com bomba em marcha continuam pendentes de V01.

O validador específico passou em 246 verificações; o AcCoreConsole 2027 abriu e auditou
11/11 DXFs. Conferi P03-11 no PNG de produção a 300 dpi, PDF rasterizado pelo Poppler a
150 dpi e no contato das onze folhas; similaridade PDF/PNG: 0,987946. A revisão estrita
passou em 641.852 verificações sem erros ou avisos; o revisor confirmou 12 projetos,
109 folhas, 436 arquivos gráficos e 74 CSVs, com similaridade mínima de 0,981493. Os
SVGs permanecem pendentes de inspeção no navegador até autorização.

### Atualização P04-08 — revisão gráfica 04

P04-08 registra D01–D05 para levantar a fonte, seus níveis ou pressões de operação,
a geometria da sucção, as curvas Q-H/NPSHr e a necessidade de proteção contra fonte
baixa ou perda de sucção. Os valores permanecem vazios e os cinco grupos PENDENTE;
nenhuma fonte, bomba ou proteção foi selecionada.

O validador P04 passou em 260 verificações. O AutoCAD AcCoreConsole 2027 abriu e
auditou 8/8 DXFs. Conferi P04-08 no PNG de produção a 300 dpi, em PDF rasterizado pelo
Poppler a 150 dpi e no contato das oito folhas; não há cortes nem colisões aparentes,
e a similaridade PDF/PNG foi 0,99014. A revisão estrita passou em 646.736 verificações
sem erros ou avisos; o revisor confirmou 12 projetos, 110 pranchas, 440 arquivos
gráficos e 75 CSVs, com similaridade mínima de 0,981493. SVGs continuam aguardando
autorização para inspeção no navegador.

### Atualização P04-09 — revisão gráfica 05

P04-08 foi expandida para D01–D07: além de fonte, regime, geometria, bomba e proteção,
agora solicita propriedades do fluido/temperatura e pressão absoluta ou barométrica.
D03 pede área da fonte quando necessária para velocidade superficial, acessórios,
unidades e datum. Todos os sete grupos permanecem PENDENTE e `valor_registrado` vazio.

P04-09 apresenta a equação paramétrica de NPSHa, o balanço das perdas na sucção e a
comparação com NPSHr de curva OEM e margem aplicável. O desenho não contém cálculo
numérico, seleção de bomba ou resultado de cavitação. O validador P04 passou em 279
verificações; o AutoCAD AcCoreConsole 2027 auditou 9/9 DXFs. P04-08 e P04-09 foram
conferidas no PNG de produção, PDF rasterizado pelo Poppler a 150 dpi e contato das nove
folhas; similaridades PDF/PNG: 0,989404 e 0,989947. A revisão estrita passou em 650.961
verificações, sem erros ou avisos; o revisor confirmou 12 projetos, 111 pranchas, 444
arquivos gráficos e 75 CSVs, com similaridade mínima de 0,981493. A inspeção de SVGs no
navegador continua aguardando autorização.

### Atualização P02-10 — revisão gráfica 04

A revisão retirou a divisão agregada de 12.595,543 VA por 220 V e a indicação de QG1
63 A: o cálculo misturava circuitos 127 V fase-neutro com cargas 220 V fase-fase e não
comprovava a corrente de serviço. A nova P02-10 separa os circuitos por condutor e
calcula apenas cotas superiores aritméticas sem diversidade: 65,29 A para A e 67,56 A
para B. Elas não representam demanda nem correntes fasoriais. O dimensionamento de
QG1, DR, alimentador e simultaneidade depende de método e dados reais.

O validador matemático P02 passou em 98 verificações. O AutoCAD AcCoreConsole 2027
abriu e auditou os 10/10 DXFs, com zero erros encontrados e zero corrigidos. Conferi
o contato das dez folhas e a rasterização integral da P02-10; a tabela, o gráfico, o
aviso de limites e o carimbo 04/10 estão dentro da moldura. A similaridade PDF/PNG da
nova folha foi 0,989581. A revisão integrada confirmou 12 projetos, 112 folhas, 448
arquivos gráficos e 76 CSVs; a validação estrita passou em 656.386 verificações, sem
erros ou avisos. A inspeção de SVGs no navegador continua pendente de autorização.
As alterações foram enviadas no commit `c79c7101cdc16853ceccb1820494b2bbe7bfe447`;
o PR #1 foi atualizado e segue aberto como rascunho, sem merge.

### Atualização P11-08 — revisão gráfica 03

A nova prancha transforma os dados pendentes do P11-07 em uma matriz de quatro
verificações: condutor/conexões, resposta da malha por cenário, exposição a potenciais
de toque/passo e transferência para interfaces remotas. Cada linha relaciona o
resultado esperado às entradas e evidências necessárias; todas continuam pendentes.
O desenho explica `I_f` e `S_g` e não define método, limites, resultados calculados ou
aprovação. IEEE Std 80-2013 e IEEE Std 81-2025 aparecem como referências suplementares,
com aviso para confirmar edições e critérios aplicáveis.

O validador P11 passou com oito folhas, 23 materiais, 17 cabos e 22 entradas pendentes.
O AutoCAD AcCoreConsole 2027 auditou 8/8 DXFs com zero erros encontrados e zero
corrigidos. O contato das oito folhas e a rasterização independente do PDF da P11-08
foram inspecionados, sem cortes aparentes; sua similaridade PDF/PNG foi 0,988037,
também a mínima entre as oito folhas P11. A revisão integrada confirmou 12 projetos,
113 pranchas, 452 arquivos gráficos e 76 CSVs. A validação estrita passou em 660.601
verificações, sem erros ou avisos. A inspeção de SVGs no navegador continua aguardando
autorização do usuário.

### Atualização P01-09 — revisão 04

A prancha 09 organiza quatro estados de habilitação, o ciclo PRONTO–PARTIDA–MARCHA–
PARADA e quatro eventos: emergência, falha do VFD, falta de energia e troca de modo/
perda de sinal. `sequencia-estados.csv` fornece os rótulos e descrições. A folha distingue
S5/KSR1 do reset S4/X3:9 do VFD e declara que rearmar não inicia o motor. A ação para
perda remota de 4–20 mA continua hipótese a confirmar no equipamento selecionado; não
há categoria/PL/SIL, tempo de parada ou resultado de campo declarado.

Inspecionei o PNG de produção a 300 dpi, a folha de contato do P01 e o PDF rasterizado
independentemente pelo Poppler a 150 dpi. Não encontrei cortes ou colisões; a similaridade
PDF/PNG de P01-09 foi 0,990330. O AcCoreConsole 2027 auditou 9/9 DXFs P01 e uma segunda
geração reproduziu os nove SHA-256. A validação estrita passou em 663.880 verificações,
sem erros ou avisos; a revisão integrada confirmou 12 projetos, 114 folhas, 456 arquivos
gráficos e 77 CSVs. Os SVGs continuam aguardando autorização para inspeção no navegador.
