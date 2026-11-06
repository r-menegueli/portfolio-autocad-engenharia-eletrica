# Plano original dos dez projetos acadêmicos

Autor: Rogério Eduardo Moreira Menegueli
Estado: P01 a P10 concluídos

## Propósito

Este documento registra o plano original de dez projetos acadêmicos de Engenharia
Elétrica, do desenho de baixa tensão à integração de sistemas industriais. P11 e
P12 foram acrescentados depois e não fazem parte do plano original; a lista atual
de doze estudos está no [README do repositório](../README.md#projetos).

As regras permanentes estão no [AGENTS.md](../AGENTS.md), e os critérios comuns
estão descritos no [padrão gráfico](./padrao-grafico.md) e nos
[critérios técnicos](./criterios-tecnicos.md). A organização prevista para as
pastas de trabalho está resumida em [projetos/README.md](../projetos/README.md).

## Aviso obrigatório

O texto abaixo deverá constar, sem abreviações, nas notas de todas as pranchas,
no README e no memorial descritivo de cada projeto:

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Nenhum documento deverá conter CPF, RG, telefone ou endereço residencial do
autor.

## Base comum de cada projeto

Cada projeto deverá declarar finalidade, escopo, exclusões, unidades, normas e
edições adotadas, fontes dos dados, hipóteses de cálculo e limitações. Os valores
de entrada deverão ser fictícios ou devidamente anonimizados.

Todos os projetos deverão usar folha A3 em paisagem, moldura, carimbo, autor,
data, revisão, número da prancha, legenda, notas técnicas, layers e símbolos
padronizados. O DXF verdadeiro será a fonte principal; renomear um DXF para DWG
é proibido. Um DWG só poderá ser incluído após conversão real e verificação de
abertura.

Entregáveis mínimos por projeto:

- `README.md`, com objetivo, escopo, instruções de reprodução e índice de
  pranchas;
- `memorial-descritivo.md` e `criterios-premissas.md`;
- memória de cálculo rastreável quando houver dimensionamento;
- scripts-fonte determinísticos para gerar ou atualizar os desenhos;
- uma ou mais pranchas DXF, numeradas e validadas;
- visualizações correspondentes em PDF, SVG e PNG;
- `lista-materiais.csv`, com cabeçalhos, unidades e quantidades;
- relatório de validação automática e registro de inspeção visual.

A estrutura interna e os nomes exatos deverão seguir o
[guia da pasta de projetos](../projetos/README.md). Um projeto somente avança de
rascunho para concluído quando todos os entregáveis correspondem à mesma revisão.

## Sequência recomendada

| Ordem | Código | Projeto | Competência principal | Dependência recomendada |
| ---: | :---: | --- | --- | --- |
| 1 | P01 | Painel de motor com inversor de frequência | potência, comando, STO, bornes e integração | infraestrutura do portfólio |
| 2 | P02 | Projeto elétrico residencial | baixa tensão residencial, cargas, proteção e aterramento | infraestrutura do portfólio |
| 3 | P03 | Painel de automação com CLP para duas bombas | I/O, alternância, segurança e interfaces | P01 |
| 4 | P04 | Controle de nível de reservatório | instrumentação, PI, VFD e intertravamentos | P01 e P03 |
| 5 | P05 | Instalação elétrica industrial | cargas, distribuição, iluminação e encaminhamento | P01 e P02 |
| 6 | P06 | Centro de Controle de Motores | partida direta, reversão, VFD e integração | P01, P03 e P05 |
| 7 | P07 | Arquitetura elétrica de veículo elétrico | tração HV, baixa tensão, controle V/f e FOC | P01, P03 e P06 |
| 8 | P08 | Sistema fotovoltaico residencial conectado à rede | arranjo FV, proteções CC/CA, conexão e aterramento | P02 |
| 9 | P09 | Fonte de bancada ajustável | conversão, regulação, medição e integração eletromecânica | P01 |
| 10 | P10 | Rede acadêmica de instrumentação industrial | instrumentação, I/O, comunicação e rastreabilidade | P03 e P04 |

## P01 — Painel de motor com inversor de frequência

**Objetivo.** Documentar um painel acadêmico de acionamento de motor de indução
trifásico com inversor de frequência, estabelecendo a primeira aplicação completa do
fluxo de geração, renderização e validação.

**Escopo.** Alimentação trifásica, seccionamento, proteção, VFD, motor, emergência em
dois canais com STO conceitual, partida/parada, seleção local/remoto, referência de
velocidade, sinalização, bornes, aterramento, cabos e layout interno.

**Pranchas e dados específicos.** Diagramas unifilar, de potência, de comando e de
bornes; layout interno; interligações de campo; listas de cabos e materiais; sequência
funcional e relação conceitual entre V/f e FOC.

**Marco inicial.** Concluído na revisão 00 com seis DXFs AC1027 auditados no AutoCAD
2027, derivados PDF/SVG/PNG inspecionados e validação estrita aprovada.

**Situação atual — revisão funcional/documental 03 (2026-11-06).** Oito folhas AC1027;
P01-03 agora separa RUN, STOP e reset de falha do VFD, e mostra S5 como rearme manual
monitorado de KSR1, distinto de S4/X3:9. P01-08 e `plano-verificacao.csv` rastreiam
treze verificações, todas `NÃO EXECUTADO`. O AutoCAD AcCoreConsole 2027 auditou as oito
fontes, e a validação estrita e a inspeção visual de P01-03/P01-08 passaram. A pinagem
DI/STO, os contatos de S3, a coordenação e os ensaios seguem pendentes de modelos,
documentação OEM e dados reais.

## P02 — Projeto elétrico residencial

**Objetivo.** Documentar uma residência térrea original e fictícia, com arquitetura,
iluminação, tomadas, eletrodutos, proteção, distribuição e aterramento conceitual.

**Escopo.** Alimentação 127/220 V, QD1, oito circuitos, TUG, TUE, DR, DPS,
disjuntores, condutores, queda de tensão simplificada, rotas de eletrodutos,
barramentos N/PE e detalhes de equipotencialização e eletrodo.

**Pranchas e dados específicos.** Planta arquitetônica mobiliada e esquadrias,
iluminação, tomadas, eletrodutos, diagrama unifilar, quadro de distribuição, quadro de
cargas, detalhes de aterramento, rastreabilidade de cargas por ambiente e análise
aritmética por condutor; listas CSV de pontos, cargas, materiais, esquadrias e corrente
por fase.

**Marco de aceitação.** Dez folhas AC1027 com PDF/SVG/PNG, rastreabilidade por CSV e
auditoria DXF no AutoCAD AcCoreConsole 2027 (10/10, zero erros). Revisão estrita do
portfólio e revisor integrado passaram sem erros; limites acadêmicos permanecem
explícitos.

**Revisão gráfica 03 (2026-11-06).** A planta agora representa os vãos com interrupções
nas paredes, mostra acesso ao Quarto 2 e ao banheiro pela circulação e acesso ao closet
pelo Quarto 1, além de mobiliário/aparelhos de referência. O CSV `esquadrias.csv` registra oito
portas e sete janelas. Oito ambientes somam 75 m², 20 pontos totalizam 15.558,6955 VA,
com dimensões, aberturas e cargas marcadas como premissas. As nove folhas integrais
foram inspecionadas; os DXFs são reproduzíveis, auditados e validados. O SVG ainda
aguarda inspeção no navegador mediante autorização.

**Revisão 04 (2026-11-06).** Acrescentada P02-10 com cotas superiores aritméticas de
corrente por condutor, separando os circuitos de 127 V fase-neutro dos ramais C6/C7 de
220 V fase-fase. A corrente agregada anterior de 57,252 A e a indicação de QG1 63 A
foram retiradas; a divisão por 220 V misturava tensões e não demonstrava corrente de
serviço. P02-10 usa a soma de magnitudes S/V sem diversidade, não é demanda nem corrente
fasorial exata. A seleção de QG1, alimentador, DR e simultaneidade permanece pendente.

## P03 — Painel de automação com CLP para duas bombas

**Objetivo.** Documentar um painel acadêmico de nível com duas bombas, CLP genérico,
alternância automática e operação manual protegida. O sentido do processo (enchimento
ou esgotamento) e os tanques de origem/destino estão pendentes em V01.

**Escopo.** Alimentação 220 V trifásica, fonte 24 Vcc, 16 DI, 16 DO, contatores,
sobrecargas, relés de interface, níveis baixo-baixo/baixo/alto/alto-alto, emergência em
dois canais, bloqueio físico por funcionamento a seco, sinalização e alarme remoto.

**Pranchas e dados específicos.** Arquitetura de automação; alimentação 24 Vcc;
entradas; saídas; comando; layout do painel; bornes; interligações de campo; sequência;
plano CSV de verificação e evidências com 12 itens ainda não executados; listas CSV de
I/O, bornes, cabos e materiais; estados e pseudocódigo.

**Marco de aceitação.** Concluído na revisão 00. Oito DXFs AC1027 auditados no AutoCAD
2027, derivados PDF/SVG/PNG inspecionados, invariantes lógicos e validação estrita
aprovados.

**Revisão 02 (2026-11-05).** Acrescentada a prancha 09 com sequência visual de
operação/intertravamentos e a matriz causa-efeito em CSV. A tabela distingue as
respostas definidas das decisões de processo ainda pendentes, como a reação a sensores
incoerentes durante uma marcha. As nove folhas foram regeneradas; a nova revisão não
foi reaberta no AutoCAD nesta rodada.

**Revisão 03 (2026-11-05).** Acrescentada a prancha 10 com plano de verificação e
evidências para processo, hardware, I/O, permissivos, falhas e entrega. Todos os 12
itens permanecem `NÃO EXECUTADO`; a resposta à incoerência de sensores com bomba em
marcha continua bloqueada por decisão formal do processo.

**Revisão 04 (2026-11-06).** A prancha 09 e V01 destacam uma divergência: a descrição
anterior dizia enchimento, enquanto a lógica LSH-inicia/LSL-encerra/LSHH-reserva pode
corresponder a esgotamento. O sentido, tanques e origem de LSL-LL precisam ser aprovados
antes de implementar. Os 12 itens seguem `NÃO EXECUTADO`.

## P04 — Controle de nível de reservatório

**Objetivo.** Documentar uma malha acadêmica de nível com bomba, instrumentação,
CLP e inversor de frequência, deixando explícitas a dinâmica e as limitações.

**Escopo.** Reservatório TK-101, bomba P-101/M-101, LT-101, chaves LSL/LSH/LSHH,
controlador LIC-101 no PLC-101, VFD-101, alarmes, permissivos, I/O, cabos e bornes.
A variável controlada é o nível; a variável manipulada é a frequência do inversor;
a vazão de consumo é a perturbação principal.

**Pranchas e dados específicos.** Fluxograma do processo; P&ID; malha de controle;
diagrama elétrico; interligações dos instrumentos; layout do sistema; sequência de
operação e matriz causa–efeito; listas de instrumentos, I/O, cabos, bornes e materiais.

**Marco de aceitação.** Revisão 02 com sete DXFs AC1027 e derivados PDF/SVG/PNG;
validadores funcionais e estrito devem passar. A revisão local de PNG e PDF é
registrada em `inspecao-visual.md`; a abertura dos SVGs atuais no navegador e a
reabertura no AutoCAD ainda são verificações pendentes.

## P05 — Instalação elétrica industrial

**Objetivo.** Documentar uma oficina metalmecânica fictícia com dimensões e cargas
declaradas, mostrando a passagem do levantamento de cargas para distribuição,
encaminhamento e detalhes de instalação.

**Escopo.** Galpão de 30 x 18 m, alimentação 380/220 V, QGBT-05, QDF-05, QDL-05,
QADM-05, cinco máquinas trifásicas, solda, tomadas industriais, iluminação,
alimentadores, eletrocalhas, circuitos C01 a C16 e critérios preliminares de proteção,
ampacidade e queda de tensão.

**Pranchas e dados específicos.** Layout industrial; distribuição de força;
distribuição de iluminação; eletrocalhas e rotas; diagrama unifilar; quadro de cargas;
detalhes de instalação; quadro de cargas, alimentadores, cabos e materiais em CSV e
workbook técnico. A revisão 03 acrescenta P05-09, um roteiro de dados e evidências
para calcular curto-circuito, verificar cabos e comparar os seis pares de proteção;
todos os grupos permanecem pendentes até que existam dados rastreáveis.

**Marco de aceitação.** Concluído na revisão 00. Sete DXFs AC1027, derivados
PDF/SVG/PNG, validação dos cálculos, auditoria CAD e inspeção visual devem permanecer
coerentes.

**Revisão 03 (2026-11-05).** Acrescentada P05-09 e `dados-estudo-coordenacao.csv`
com doze grupos para entradas da concessionária e dos equipamentos, modelo de faltas,
Icc máximo/mínimo, verificação térmica, curvas, seletividade e revisão documental.
Não foram criados valores de curto-circuito, modelos de proteção ou resultados de
coordenação; os doze grupos continuam `PENDENTE`.

**Revisão 04 (2026-11-06).** O fluxo de P05-09 agora identifica as entradas D01-D06,
o modelo D07, o cálculo de Icc máximo/mínimo por ponto D08, as verificações de
capacidade/suportabilidade e curvas/pares D09-D11 e o fechamento documental D12. Foram
removidas as referências didáticas de 6 kA e Icu de 10 kA, pois os dados da rede e os
dispositivos não estão selecionados. Todos os dados continuam pendentes; nenhum
resultado de curto-circuito, interrupção ou seletividade foi criado.

## P06 — Centro de Controle de Motores

**Objetivo.** Integrar em um CCM acadêmico três cargas industriais com métodos de
acionamento distintos e uma arquitetura comum de proteção, comando e segurança.

**Escopo.** Bomba com partida direta, esteira com reversão eletricamente e
mecanicamente intertravada e ventilador com inversor de frequência e STO. Inclui
alimentador, proteções, aterramento, layout, bornes, cabos e sequência funcional.

**Pranchas e dados específicos.** Unifilar do CCM; partida direta; partida reversora;
acionamento por inversor; layout funcional interno do CCM; interfaces de potência;
detalhamento individual de 51 bornes de potência, campo e controle; lista de cabos;
matriz causa-efeito e balanço de demanda; listas estruturadas de cargas, alimentador,
bornes, cabos e materiais.

**Marco de aceitação.** Dez DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar as
listas estruturadas e cada condutor de campo com um borne. Devem mostrar os totais
instalados e demandados sem somar correntes de ramais para representar W600, e
documentar a exclusão mútua dos contatores reversores, a parada comum e a ausência de
rearme automático.

**Revisão 03.** Acrescentada P06-09 com a comparação das três cargas, fatores de
demanda, totais P/S instalados e demandados e corrente equivalente de W600. Os dados
de proteção e fatores continuam premissas; a relação aritmética não valida o método
de instalação, fatores de correção, capacidade térmica, Icc ou seletividade.

**Revisão 04.** Corrigida a correspondência dos cabos W604-W608 com X3/X4, incluídos
os oito condutores de W607 e o sinal local/remoto DI3, e separados os pares do botão
de emergência dos fios internos STO A/B. A P06-10 registra os bornes individualmente;
P06-05 identifica os componentes por função sem fingir dimensões de fabricante.

## P07 — Arquitetura elétrica acadêmica de veículo elétrico

**Objetivo.** Representar a arquitetura de um veículo elétrico conceitual com bateria
de tração, barramento de alta tensão, inversor e motor de indução, relacionando o
projeto ao estudo acadêmico de controle escalar V/f e controle vetorial FOC.

**Escopo.** BMS, fusíveis, contatores positivo e negativo, pré-carga, inversor,
motor de indução, conversor CC-CC, bateria auxiliar, VCU, sensores, CAN, HVIL,
monitoramento de isolação, intertravamentos e desconexão de emergência.

**Pranchas e dados específicos.** Arquitetura geral; circuitos de alta e baixa tensão;
pré-carga e contatores; inversor e motor; sensores e controle; rede de comunicação;
layout conceitual dos componentes; interfaces e matriz de dez eventos; parâmetros,
sinais, mensagens, cabos e materiais.

**Marco de aceitação.** Nove DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar as
tabelas estruturadas, demonstrar uma sequência de pré-carga segura por construção,
separar fatos de premissas e propostas e explicar V/f e FOC sem atribuir resultados
experimentais ao TCC do autor.

**Situação.** Revisado na revisão gráfica 02 em 2026-11-05: nove DXFs auditados no
AcCoreConsole, matriz conceitual de interfaces e falhas, e revisão visual das folhas.
HARA, FMEA, software, segurança funcional e ensaios veiculares continuam fora do escopo.

## P08 — Sistema fotovoltaico residencial conectado à rede

**Objetivo.** Representar um sistema fotovoltaico residencial acadêmico desde a
disposição dos módulos até o ponto de conexão interno, com cálculos rastreáveis e
limites de aplicação explícitos.

**Escopo.** Doze módulos em duas strings, inversor string conceitual, circuitos CC e
CA, string box, fusíveis gPV, DPS, seccionamento, quadro dedicado, medição,
equipotencialização e interface com aterramento e SPDA existentes.

**Pranchas e dados específicos.** Disposição dos módulos; unifilares CC e CA;
detalhamento da string box; aterramento; layout de equipamentos; parâmetros,
módulos, proteções, cabos, cálculos e materiais em CSV.

**Marco de aceitação.** Seis DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar
potências, strings, tensões corrigidas, correntes, limites do inversor e proteções,
sem apresentar o estudo como liberado para instalação ou conexão.

**Situação.** Concluído na revisão 00 em 2026-09-09, com validação específica,
auditoria dos seis DXFs no AutoCAD, inspeção visual dos 18 derivados e validação
estrita integrada aprovadas.

## P09 — Fonte de bancada ajustável

**Objetivo.** Documentar a arquitetura elétrica e mecânica de uma fonte de bancada
acadêmica, desde a entrada de rede até a interface de saída ajustável.

**Escopo.** Entrada universal 90-264 Vca, proteção, fonte AC/DC isolada de 36 V,
regulador buck CC/CV, saída flutuante regulada de 0,8-30 Vcc e até 5 A, limitada a
150 W, medição,
comandos, ventilação, painel frontal, gabinete, organização interna e PE de chassi.

**Pranchas e dados específicos.** Diagrama de blocos; diagrama elétrico; painel
frontal; layout interno; detalhes mecânicos; interligações; parâmetros, cálculos,
equipamentos, proteções, recortes, condutores, materiais e matriz paramétrica de
perdas térmicas em CSV.

**Marco de aceitação.** Seis DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar
tensões, correntes, potência, perdas, ventilação, tags, recortes e interligações,
sem apresentar o equipamento como certificado ou pronto para fabricação.

**Situação.** Concluído na revisão 00 em 2026-09-09, com validação específica,
auditoria dos seis DXFs no AutoCAD e inspeção visual dos 18 derivados aprovadas.

**Revisão 04 (2026-11-05).** Acrescentada a prancha 10 e uma matriz CSV com nove
combinações hipotéticas de eficiência de PS1 e REG1 em POUT=150 W. O balanço mostra
perdas agregadas e margem de potência, sem atribuir eficiências a componentes reais ou
estimar temperaturas. Perdas por componente, Rθ, fluxo de ar e ensaios seguem pendentes.

## P10 — Rede acadêmica de instrumentação industrial

**Objetivo.** Documentar de ponta a ponta uma arquitetura fictícia de instrumentação,
distinguindo energia, medição analógica, estados digitais e comunicação industrial.

**Escopo.** TT-101, PT-102, FT-103 e LT-104 em 4–20 mA; LSH-105 e PSL-106 como
entradas digitais 24 Vcc; PLC-101; remotas RIO-201 e RIO-202; switch SW-101;
SCADA-101; fonte PS1; bornes, cabos, shield, PE e endereçamento documental.

**Pranchas e dados específicos.** Arquitetura da rede; diagrama de instrumentação;
diagrama de interligação; topologia de comunicação; painel de instrumentação; lista
de instrumentos; matriz causa–efeito; matriz de cinco pontos de escala para cada uma
das quatro malhas analógicas; balanço visual da alimentação 24 Vcc; detalhe dos
bornes de alimentação das remotas; tabelas de I/O, cabos, bornes, rede, alimentação
e materiais.

**Verificação documental.** Dez DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar
tags, canais, cabos, bornes, faixas e endereços; quatro escalas lineares são
verificadas nos extremos e em três pontos intermediários; o balanço deve reconciliar
as sete cargas da lista e separar saldo aritmético de reserva auxiliar prevista.

**Situação.** Revisão 05 em 2026-11-06: dez folhas, vinte pontos de conversão
analógica, balanço gráfico da fonte 24 Vcc e interligação dos dois alimentadores
remotos. Os valores são resultados matemáticos
das premissas, não calibração, ensaio de bancada ou dimensionamento térmico. Validação,
auditoria CAD e inspeção visual estão registradas no README e em `inspecao-visual.md`.

## Fases e portões de qualidade

Cada projeto seguirá estas fases:

1. **Definição:** congelar escopo, dados fictícios, unidades, normas e critérios.
2. **Modelagem:** criar dados estruturados, cálculos e biblioteca de símbolos.
3. **Geração:** produzir DXF e derivados exclusivamente por fluxo documentado.
4. **Validação:** executar verificações automáticas de arquivos, layers, limites,
   moldura, textos, links e entregáveis.
5. **Inspeção visual:** revisar PDF, SVG e PNG em escala legível, corrigindo cortes,
   desalinhamentos, colisões e hierarquia gráfica.
6. **Congelamento:** alinhar revisão, data e número de prancha, registrar o
   resultado e fazer commit local com a árvore limpa.

O projeto seguinte poderá começar antes do congelamento do anterior apenas para
pesquisa e coleta de requisitos; componentes gráficos só serão promovidos à base
comum depois de aprovados nos dois portões de qualidade.

## Evolução da biblioteca comum

- P01 estabelece símbolos de potência, comando, instrumentação, bornes e interligações
  de campo para acionamentos com inversor.
- P02 acrescenta arquitetura residencial, luminárias, tomadas, eletrodutos, quadros,
  cargas e detalhes de aterramento.
- P03 acrescenta CLP, cartões de I/O, sensores de nível, relés de interface, estados,
  alternância de bombas e permissivos físicos.
- P04 acrescenta tanque, tubulações, instrumentos ISA, malha PI, VFD e intertravamentos.
- P05 acrescenta layout industrial, máquinas trifásicas, quadros, tomadas,
  alimentadores, eletrocalhas e quadro de cargas industrial.
- P06 acrescenta gavetas de CCM, partida direta, reversão intertravada, VFD, STO e
  integração de bornes e cabos.
- P07 acrescenta arquitetura veicular HV/LV, BMS, pré-carga, HVIL, CAN e diagramas
  conceituais de controle V/f e FOC para motor de indução.
- P08 acrescenta módulos e strings fotovoltaicos, string box, DPS CC/CA, inversor
  conectado à rede, medição e equipotencialização residencial.
- P09 acrescenta fonte AC/DC isolada, regulação buck CC/CV, medição de bancada,
  painel frontal, ventilação e detalhes mecânicos de gabinete.
- P10 acrescenta transmissores de temperatura, pressão, vazão e nível, remotas de I/O,
  arquitetura Ethernet industrial, filosofia 4–20 mA, bornes e blindagem funcional.

## Resultado desta etapa

Os Projetos 01 a 10 estão concluídos, reproduzíveis e integrados ao manifesto e ao
validador comum do portfólio.
