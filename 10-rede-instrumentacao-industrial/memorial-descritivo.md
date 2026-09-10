# Memorial descritivo — P10

## Identificação

- Projeto: rede acadêmica de instrumentação industrial
- Autor: Rogério Eduardo Moreira Menegueli
- Data: 2026-09-10
- Revisão: 00
- Fonte gráfica: seis DXFs AC1027 em A3 paisagem e milímetros

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Finalidade e processo fictício

O conjunto documenta a aquisição de temperatura, pressão, vazão e nível de um skid
industrial fictício. TT-101, PT-102, FT-103 e LT-104 usam transmissores genéricos de
dois fios com saída 4–20 mA. LSH-105 e PSL-106 fornecem estados discretos 24 Vcc. O
objetivo é demonstrar a passagem rastreável do instrumento de campo ao I/O remoto, à
rede de controle e ao SCADA, sem afirmar desempenho experimental ou conformidade.

## Arquitetura funcional

O painel PI-101 recebe 230 Vca conceituais e PS1 fornece 24 Vcc/10 A. PLC-101 e o
switch SW-101 estão no painel. RIO-201 atende a área A e recebe TT-101, PT-102 e
LSH-105; RIO-202 atende a área B e recebe FT-103, LT-104 e PSL-106. SW-101 interliga
PLC-101, as duas remotas, SCADA-101 e uma estação temporária de engenharia em topologia
estrela. O protocolo e os produtos não são selecionados.

## Malhas e interligações

Cada malha analógica usa um par trançado blindado identificado. A blindagem termina
em BE-101 no painel e permanece isolada no campo, conforme premissa específica que
deve ser revista com as instruções do fabricante e o estudo de EMC. As entradas
digitais usam cabos próprios. Alimentação de remotas e comunicação usam rotas e
identificadores independentes. Bornes X2 distribuem 24 Vcc/0 V, X3 atende analógicos e
X4 atende digitais.

PE-101 é a barra de proteção e equipotencialização. BE-101 é a barra funcional de
blindagem, ligada ao PE em um ponto definido no conceito. O condutor PE não é retorno
operacional; 0 V não é sinônimo de PE; a blindagem não substitui condutor de proteção.

## Dados e coerência

As listas CSV são a referência tabular para tags, canais, cabos, bornes, endereços e
materiais. A relação de escala analógica é documentada na
[memória de cálculo](memoria-calculo.md). A distinção entre energia e informação está
detalhada na [filosofia de sinais](filosofia-sinais.md). Todas as pranchas apresentam
autor, data, revisão, número, unidades, legenda, notas e aviso.

## Exclusões e segurança

Não fazem parte: malha de controle fechada, funções instrumentadas de segurança,
classificação de áreas, especificação de barreiras, cibersegurança industrial,
disponibilidade, redundância, seleção de protocolo, cálculo de curto-circuito,
coordenação e seletividade, detalhamento de DPS, comissionamento, calibração e ensaios.
Alarmes do CLP/SCADA não são funções de segurança.
