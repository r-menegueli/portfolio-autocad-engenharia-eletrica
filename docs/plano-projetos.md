# Plano dos dez projetos acadêmicos

> Este plano histórico cobre os projetos P01–P10. A coleção atual abrange P01–P25; consulte o [README](../README.md) e o manifesto `portfolio.toml` para o índice vigente.

Autor: Rogério Eduardo Moreira Menegueli
Estado: P01 a P10 concluídos

## Propósito

Este documento organiza a evolução do portfólio em dez projetos acadêmicos de
Engenharia Elétrica, do desenho de baixa tensão à integração de sistemas
industriais. A ordem foi escolhida para reaproveitar componentes já validados e
introduzir complexidade gradualmente.

Os critérios comuns estão descritos no [padrão gráfico](./padrao-grafico.md) e nos
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

**Marco de aceitação.** Concluído na revisão 00. Seis DXFs AC1027 auditados no AutoCAD
2027, derivados PDF/SVG/PNG inspecionados e validação estrita aprovada.

## P02 — Projeto elétrico residencial

**Objetivo.** Documentar uma residência térrea original e fictícia, com arquitetura,
iluminação, tomadas, eletrodutos, proteção, distribuição e aterramento conceitual.

**Escopo.** Alimentação 127/220 V, QD1, oito circuitos, TUG, TUE, DR, DPS,
disjuntores, condutores, queda de tensão simplificada, rotas de eletrodutos,
barramentos N/PE e detalhes de equipotencialização e eletrodo.

**Pranchas e dados específicos.** Planta arquitetônica, iluminação, tomadas,
eletrodutos, diagrama unifilar, quadro de distribuição, quadro de cargas e detalhes
de aterramento; listas CSV de pontos, cargas e materiais.

**Marco de aceitação.** Concluído na revisão 00. Oito DXFs AC1027, derivados
PDF/SVG/PNG, validação matemática e inspeção visual devem permanecer coerentes.

## P03 — Painel de automação com CLP para duas bombas

**Objetivo.** Documentar um painel acadêmico para enchimento de reservatório com duas
bombas, CLP genérico, alternância automática e operação manual protegida.

**Escopo.** Alimentação 220 V trifásica, fonte 24 Vcc, 16 DI, 16 DO, contatores,
sobrecargas, relés de interface, níveis baixo-baixo/baixo/alto/alto-alto, emergência em
dois canais, bloqueio físico por funcionamento a seco, sinalização e alarme remoto.

**Pranchas e dados específicos.** Arquitetura de automação; alimentação 24 Vcc;
entradas; saídas; comando; layout do painel; bornes; interligações de campo; listas CSV
de I/O, bornes, cabos e materiais; sequência, estados e pseudocódigo.

**Marco de aceitação.** Concluído na revisão 00. Oito DXFs AC1027 auditados no AutoCAD
2027, derivados PDF/SVG/PNG inspecionados, invariantes lógicos e validação estrita
aprovados.

## P04 — Controle de nível de reservatório

**Objetivo.** Documentar uma malha acadêmica de nível com bomba, instrumentação,
CLP e inversor de frequência, deixando explícitas a dinâmica e as limitações.

**Escopo.** Reservatório TK-101, bomba P-101/M-101, LT-101, chaves LSL/LSH/LSHH,
controlador LIC-101 no PLC-101, VFD-101, alarmes, permissivos, I/O, cabos e bornes.
A variável controlada é o nível; a variável manipulada é a frequência do inversor;
a vazão de consumo é a perturbação principal.

**Pranchas e dados específicos.** Fluxograma do processo; P&ID; malha de controle;
diagrama elétrico; interligações dos instrumentos; layout do sistema; listas de
instrumentos, I/O, cabos, bornes e materiais.

**Marco de aceitação.** Concluído na revisão 00. Seis DXFs AC1027, derivados
PDF/SVG/PNG, validação funcional da malha, auditoria CAD e inspeção visual devem
estar aprovados e registrados.

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
workbook técnico.

**Marco de aceitação.** Concluído na revisão 00. Sete DXFs AC1027, derivados
PDF/SVG/PNG, validação dos cálculos, auditoria CAD e inspeção visual devem permanecer
coerentes.

## P06 — Centro de Controle de Motores

**Objetivo.** Integrar em um CCM acadêmico três cargas industriais com métodos de
acionamento distintos e uma arquitetura comum de proteção, comando e segurança.

**Escopo.** Bomba com partida direta, esteira com reversão eletricamente e
mecanicamente intertravada e ventilador com inversor de frequência e STO. Inclui
alimentador, proteções, aterramento, layout, bornes, cabos e sequência funcional.

**Pranchas e dados específicos.** Unifilar do CCM; partida direta; partida reversora;
acionamento por inversor; layout do CCM; diagrama de bornes; lista de cabos; listas
estruturadas de cargas, alimentador, bornes, cabos e materiais.

**Marco de aceitação.** Sete DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar as
listas estruturadas, comprovar a exclusão mútua dos contatores reversores, a parada
comum e a ausência de rearme automático.

**Situação.** Concluído na revisão 00 em 2026-09-09, com validação específica,
auditoria dos sete DXFs no AutoCAD e inspeção visual dos 21 derivados aprovadas.

## P07 — Arquitetura elétrica acadêmica de veículo elétrico

**Objetivo.** Representar a arquitetura de um veículo elétrico conceitual com bateria
de tração, barramento de alta tensão, inversor e motor de indução, relacionando o
projeto ao estudo acadêmico de controle escalar V/f e controle vetorial FOC.

**Escopo.** BMS, fusíveis, contatores positivo e negativo, pré-carga, inversor,
motor de indução, conversor CC-CC, bateria auxiliar, VCU, sensores, CAN, HVIL,
monitoramento de isolação, intertravamentos e desconexão de emergência.

**Pranchas e dados específicos.** Arquitetura geral; circuitos de alta e baixa tensão;
pré-carga e contatores; inversor e motor; sensores e controle; rede de comunicação;
layout conceitual dos componentes; parâmetros, sinais, mensagens, cabos e materiais.

**Marco de aceitação.** Oito DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar as
tabelas estruturadas, demonstrar uma sequência de pré-carga segura por construção,
separar fatos de premissas e propostas e explicar V/f e FOC sem atribuir resultados
experimentais ao TCC do autor.

**Situação.** Concluído na revisão 00 em 2026-09-09, com validação específica,
auditoria dos oito DXFs no AutoCAD e inspeção visual dos 24 derivados aprovadas.

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
regulador buck CC/CV, saída flutuante de 0-30 Vcc e 0-5 A limitada a 150 W, medição,
comandos, ventilação, painel frontal, gabinete, organização interna e PE de chassi.

**Pranchas e dados específicos.** Diagrama de blocos; diagrama elétrico; painel
frontal; layout interno; detalhes mecânicos; interligações; parâmetros, cálculos,
equipamentos, proteções, recortes, condutores e materiais em CSV.

**Marco de aceitação.** Seis DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar
tensões, correntes, potência, perdas, ventilação, tags, recortes e interligações,
sem apresentar o equipamento como certificado ou pronto para fabricação.

**Situação.** Concluído na revisão 00 em 2026-09-09, com validação específica,
auditoria dos seis DXFs no AutoCAD e inspeção visual dos 18 derivados aprovadas.

## P10 — Rede acadêmica de instrumentação industrial

**Objetivo.** Documentar de ponta a ponta uma arquitetura fictícia de instrumentação,
distinguindo energia, medição analógica, estados digitais e comunicação industrial.

**Escopo.** TT-101, PT-102, FT-103 e LT-104 em 4–20 mA; LSH-105 e PSL-106 como
entradas digitais 24 Vcc; PLC-101; remotas RIO-201 e RIO-202; switch SW-101;
SCADA-101; fonte PS1; bornes, cabos, shield, PE e endereçamento documental.

**Pranchas e dados específicos.** Arquitetura da rede; diagrama de instrumentação;
diagrama de interligação; topologia de comunicação; painel de instrumentação; lista
de instrumentos; tabelas de I/O, cabos, bornes, rede, alimentação e materiais.

**Marco de aceitação.** Seis DXFs AC1027 e derivados PDF/SVG/PNG devem reconciliar
tags, canais, cabos, bornes, faixas e endereços; quatro escalas lineares devem ser
verificadas; alimentação, analógico, digital e comunicação devem permanecer claros.

**Situação.** Concluído na revisão 00 em 2026-09-10, com validação específica,
auditoria dos seis DXFs no AutoCAD e inspeção visual dos 18 derivados aprovadas.

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
