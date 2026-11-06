# Memorial descritivo — P18

## Objetivo

Apresentar uma arquitetura conceitual para medição de qualidade de energia e compensação automática de potência reativa em uma instalação industrial hipotética. O material combina um diagrama unifilar, o cálculo de um caso-base, a discretização de degraus e um plano para levantar os dados harmônicos antes de decidir sobre filtragem.

## Instalação de referência

A planta de estudo considera alimentação em 13,8 kV, transformação para 400 V por um transformador hipotético de 1 MVA, cargas lineares de 400 kW e cargas com inversores de 200 kW. O total ativo assumido é 600 kW. O medidor PM-01 lê as grandezas no PCC/QGBT; o regulador RC-01 comanda o banco BC-01 conforme FP ou kvar medidos.

O banco desenhado tem capacidade nominal conceitual de 300 kvar, em 12 estágios de 25 kvar. Sua ligação é apresentada como conceito; a configuração real de proteção, descarga, comutação e elementos de controle não foi especificada. O estudo não seleciona filtros passivos, filtros ativos ou reatores de dessintonia.

## Cálculo do caso-base

Para carga de 600 kW, FP inicial 0,80 indutivo e alvo 0,95, `Qinicial = P × tan(arccos(FP inicial)) = 450 kvar`. A potência reativa correspondente ao alvo é cerca de 197,2 kvar. Portanto, a compensação ideal contínua calculada é `Qc ≈ 252,8 kvar`.

Com estágios de 25 kvar, 250 kvar deixam cerca de 200 kvar residuais e FP aproximado de 0,949. Com 275 kvar, o FP aproximado sobe a 0,960. Esta diferença ilustra que a discretização do banco não atinge necessariamente o ponto contínuo calculado. O regulador, a faixa-alvo e a quantidade de estágios dependeriam do perfil horário e dos equipamentos escolhidos.

## Medição e análise de harmônicos

PM-01 representa um analisador conectado no PCC por TCs e TPs. A avaliação futura deve registrar tensão, corrente, espectro, THD, simultaneidade de carga e degraus acionados durante períodos representativos. A impedância da fonte e os cenários de curto-circuito são necessários para avaliar ressonância e efeitos de banco capacitivo.

## Responsabilidade e limitações

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

O projeto não demonstra conformidade com limites harmônicos, não representa medição de campo e não dimensiona capacitores, reatores, filtros, proteção, cabos ou transformador. A operação real exige projeto, especificações de fabricante, estudos, validação e profissional legalmente habilitado.
