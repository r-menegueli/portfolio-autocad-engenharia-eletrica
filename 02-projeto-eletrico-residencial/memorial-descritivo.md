# Memorial descritivo - Projeto 02

- Autor: Rogério Eduardo Moreira Menegueli
- Data: 2026-11-06
- Revisão: 02, compatível com P02 revisão gráfica 04

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## 1. Caracterização

A residência fictícia possui um pavimento, planta retangular de 10,00 m por 7,50 m e
área construída conceitual de 75,00 m². Os ambientes representados são sala/jantar,
quarto 1, quarto 2, cozinha, lavanderia, banheiro, circulação e closet privativo do
Quarto 1. A planta foi mobiliada de modo indicativo; vãos, acessos e móveis permanecem
premissas. A arquitetura foi criada para este portfólio e não reproduz imóvel, cliente
ou planta existente.

## 2. Alimentação e distribuição

Adotou-se, como dado acadêmico, fornecimento 127/220 V, 60 Hz, duas fases, neutro e PE,
derivado de rede trifásica em estrela. O quadro QD1 tem capacidade física conceitual de
24 módulos. A corrente nominal e a curva de QG1 permanecem pendentes; a antiga indicação
de 63 A foi retirada por falta de método de demanda por condutor. DPS1 e DR1 são
referências didáticas: ratings, tipo, arranjo e coordenação ainda precisam ser definidos.
Neutro e proteção permanecem separados a jusante da origem TN-S conceitual.

Oito circuitos finais separam iluminação, tomadas de uso geral e tomadas de uso
específico. C1 a C5 e C8 são monofásicos a 127 V; C6 e C7 são bipolares a 220 V.
Todos incluem condutor de proteção. Seções e disjuntores dos circuitos são premissas
conferidas por corrente de circuito e queda simplificada; método de instalação,
temperatura, agrupamento, capacidade de interrupção e curto-circuito ainda não foram
verificados.

## 3. Iluminação, tomadas e comandos

Foram previstos onze pontos de iluminação LED: seis em C1 (78 W, 84,7825 VA) e cinco
em C2 (68 W, 73,913 VA). A sala possui duas luminárias; a cozinha também possui duas;
os demais pontos atendem quartos, circulação, closet, banheiro, espelho e lavanderia.
O closet recebeu o ponto L09 e um comando junto ao acesso. Interruptores ficam próximos
aos acessos; a circulação recebe comando paralelo indicativo. A locação continua
esquemática e deve ser confirmada com o mobiliário e o uso reais.

As potências de TUG são atribuídas para fins acadêmicos: 100 VA por ponto em sala,
quartos e circulação; 600 VA nos três primeiros pontos de cozinha e 100 VA nos demais;
600 VA por ponto no banheiro e lavanderia. As TUEs fictícias são forno elétrico de
3 000 VA em C6, chuveiro de 5 500 VA em C7 e lavadora de 1 500 VA em C8.

## 4. Arquitetura e esquadrias

A revisão gráfica 03 corrige o acesso do Quarto 2 e do banheiro a partir da circulação,
e o acesso ao closet a partir do Quarto 1. A antiga porta indevida entre banheiro e
Quarto 2 foi removida; o antigo hall foi redefinido como closet. A planta identifica
oito portas e sete janelas e inclui sofá, mesa, camas, armários, bancada, aparelhos e
louças como referências de ocupação. As dimensões e posições estão registradas em
`esquadrias.csv` e seguem como `PREMISSA`; não comprovam acessibilidade, ventilação,
iluminação natural, afastamentos, áreas mínimas nem atendimento a código de obras.

## 5. Eletrodutos, condutores e identificação

As rotas são conceituais e partem de QD1 para caixas de passagem e pontos terminais.
Foram indicados eletrodutos de 20, 25 e 32 mm conforme concentração relativa dos
circuitos. O preenchimento, o raio de curvatura e a ocupação devem ser recalculados com
catálogo e trajeto real. Condutores são de cobre, isolação 450/750 V ou 0,6/1 kV conforme
aplicação, com identificação funcional e seções entre 1,5 e 16 mm².

## 6. Demanda por fase, proteção e aterramento

P02-10 separa os ramais de 127 V fase-neutro dos ramais de 220 V fase-fase. A soma de
magnitudes S/V por condutor resulta em cotas superiores de 65,288 A na fase A e 67,565 A
na fase B, sem diversidade. Esses valores não são correntes fasoriais nem demanda; a
simultaneidade, os fatores de potência e o método de cálculo precisam ser definidos.
QG1, DR1 e o alimentador permanecem sem ratings/seção selecionados. O antigo QG1 de
63 A e alimentador de 16 mm² foram retirados como escolhas justificadas.

DPS1 e DR1 aparecem no diagrama e no arranjo de QD1 como referências didáticas. O DR
global foi adotado por simplicidade gráfica; In, tipo, distribuição dos circuitos,
continuidade de serviço e coordenação precisam de estudo específico.

O aterramento apresenta eletrodo vertical de 2,40 m apenas como detalhe indicativo,
caixa de inspeção, condutor de aterramento de cobre de 16 mm² e barramento principal de
equipotencialização. Nenhum valor de resistência de aterramento é prometido: solo,
geometria, corrosão, conexões, continuidade e medições precisam ser determinados no
local. O banheiro mostra ligação equipotencial do PE às massas acessíveis e ao chuveiro.

## 7. Limitações e responsabilidade

Não foram realizados levantamento arquitetônico, consulta à concessionária, cálculo de
demanda por condutor, estudo de curto-circuito, seletividade, coordenação de DPS, cálculo
térmico completo, ensaio de aterramento ou inspeção física. Os símbolos seguem uma linguagem coerente inspirada em
referências eletrotécnicas, porém não se afirma reprodução integral de biblioteca
normativa licenciada. Antes de qualquer uso real, todas as premissas devem ser substituídas
por dados de campo e revisadas por profissional legalmente habilitado.
