# Critérios e premissas — P24

## Escopo

Estudo acadêmico e conceitual de linha aérea trifásica de 138 kV, 60 Hz e 30 km. O corredor, as coordenadas locais, as cotas de terreno, os azimutes, os ventos, os pontos de ancoragem e a geometria das estruturas são sintéticos. A origem cartesiana local fica na SE A; X aponta para leste e Y para norte. Nada representa levantamento, faixa de servidão, licença ambiental ou cadastro real.

## Condutor e feixe

O condutor de referência é CAA 795 kcmil 26/7 Drake Class A, Nexans ref. 64719. O catálogo do fabricante informa seção nominal de 468 mm², 402,56 mm² de alumínio, diâmetro 28,11 mm, GMR 11,42 mm, massa aproximada 1,629 kg/m, resistência CC máxima de 0,072 Ω/km a 20 °C, resistência CA máxima de 0,086 Ω/km a 75 °C, ampacidade de catálogo de 910 A e carga de ruptura Classe A de 14.245 kgf. O catálogo dá 910 A sob 75 °C no condutor, 25 °C de ambiente, 1 m/s de vento e sol; isso é referência de produto, não a ampacidade final da linha.

Adota-se feixe duplo com 0,40 m entre subconductores por fase. A escolha é uma hipótese de estudo para manter a corrente do caso de 140 MW/fp 0,90 abaixo da triagem térmica simplificada em ambiente de 45 °C e vento nulo. O feixe, espaçador, ferragens, corona, perdas, vibração e distribuição de corrente não foram validados por fabricante.

O módulo axial equivalente de 34,85 MN e o coeficiente térmico de 18,9×10⁻⁶/K não são dados de placa confirmados para o produto Drake desta página. Foram adotados como aproximação a partir de uma tabela Nexans de tensão/deformação para cabo T-ACSR 26/7; a classe construtiva não é comprovadamente a mesma. Esses dois valores são premissas provisórias e limitam a confiança da flecha/tração. Exigir tabela mecânica específica do CAA selecionado e dados de encordoamento, creep e montagem antes de qualquer uso de engenharia executiva.

## Casos elétricos e térmicos

As nove combinações elétricas cruzam P = 50, 100 e 140 MW com fp = 0,90, 0,95 e 1,00, mantendo 138 kV no terminal receptor. O fluxo de potência usa o modelo nominal π positivo-sequência, resistência CA a 75 °C e parâmetros geométricos do feixe. Não foram modelados desequilíbrio, sequência zero, curto-circuito, estabilidade, transitórios, corona ou critérios de conexão.

A triagem térmica cruza três temperaturas ambiente (20, 40 e 45 °C) com três velocidades de vento (0, 0,61 e 1 m/s). A temperatura limite é 75 °C. São hipóteses do modelo: irradiância 800 W/m², absorptividade 0,5, emissividade 0,5, convecção natural mínima 6,5 W/(m²·K) e coeficiente de referência 15 W/(m²·K) a 1 m/s, com dependência em raiz quadrada da velocidade. A corrente do feixe é calculada como duas vezes a corrente por subconductor.

Essa expressão é um balanço estacionário simplificado para triagem; não é uma implementação validada da IEEE 738-2023. A margem calculada cruza conservadoramente a maior corrente dos nove casos elétricos com cada condição ambiental, independentemente do fator de simultaneidade. Não se declara capacidade térmica contínua, sazonal ou dinâmica.

## Casos mecânicos e corredor

O modelo mecânico cruza três temperaturas de condutor (20, 45 e 75 °C) com ventos transversais uniformes hipotéticos de 0, 15 e 30 m/s. Os ventos mecânicos são cenários ilustrativos; não são rajadas de projeto nem estão associados a período de retorno. Cada combinação é aplicada aos 100 vãos uniformes de 300 m.

A flecha usa aproximação parabólica e compatibilidade de comprimento/elasticidade para um vão isolado, com peso próprio e força transversal de vento. A altura de fixação média de 22 m, tração horizontal de referência de 25 kN a 20 °C e tensão de ruptura do catálogo entram no cálculo. O clearance é amostrado ao longo do perfil sintético, incluindo nós de terreno; o critério de 8 m é apenas ilustrativo. Não se modelam catenária exata, creep, balanço de cadeias, blowout lateral, vibração, galope, desnível de apoios, vãos reguladores, desequilíbrio de tensões ou hipóteses normativas de vento/gelo.

As ancoragens foram colocadas em 0, 9,9, 20,1 e 30 km para coincidir com estações da malha de 300 m. A última estrutura tem vão até a próxima igual a zero; não existe vão excedente após 30 km.

## Critérios de uso

- Tratar todos os resultados como triagem reproduzível, não como aprovação de linha, atendimento normativo ou liberação de travessias.
- Substituir o perfil, clima, parâmetros mecânicos, dados de cabo, carregamentos, geometria, critérios de clearance e ancoragens por dados do local e do proprietário.
- Verificar sequências positiva/negativa/zero, curtos, aterramento, proteção, coordenação de isolamento, estrutura, fundação, esforços de montagem e requisitos de acesso antes do projeto executivo.
- As fontes e premissas por grupo de dados estão em `dados/origem-parametros.csv`; a fonte numérica ajustável é `portfolio.toml` e sua extração é `dados/parametros.csv`.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação, energização ou operação sem projeto executivo, verificações específicas e responsabilidade profissional habilitada.
