# Memorial descritivo - Projeto 08

## Finalidade

O FV-08 é um estudo acadêmico de microgeração fotovoltaica residencial conectada à
rede. Ele organiza as interfaces elétricas do telhado ao ponto de conexão interno, sem
constituir projeto executivo, orçamento, solicitação de acesso ou documento de obra.

## Arranjo fotovoltaico

Doze módulos MOD-FV-801 de 550 Wp formam 6,60 kWp. Os módulos M01 a M06 compõem a
string S1 e alimentam o MPPT 1; M07 a M12 compõem S2 e alimentam o MPPT 2. Não há
paralelismo entre strings. Em STC, cada string apresenta 250,8 V em máxima potência,
299,4 V em circuito aberto, 13,16 A de operação e 13,92 A de curto-circuito.

A disposição gráfica considera duas fileiras orientadas ao norte e inclinadas em 20°.
A geometria é esquemática: não substitui levantamento métrico, estrutural, de
sombreamento, acesso de manutenção ou combate a incêndio.

## Circuito em corrente contínua

Cada string percorre cabo fotovoltaico identificado até SB-FV-801. A string box reúne
proteção gPV em ambos os polos, DPS tipo 2 para aplicação FV, seccionamento sob carga e
barramento PE. As saídas permanecem separadas até os dois MPPT do inversor. Os polos
positivo e negativo não são intencionalmente aterrados neste conceito.

Os fusíveis, DPS, seccionadores, conectores, cabos e invólucro são classes funcionais.
Tensão, corrente, coordenação, polaridade, compatibilidade de conectores, grau IP,
temperatura e capacidade de interrupção exigem seleção e verificação reais.

## Inversor e circuito em corrente alternada

INV-FV-801 é uma especificação acadêmica genérica: 6 kWca, 220 V entre fases, dois
MPPT, faixa de 90 a 550 Vcc, máximo de 600 Vcc, 16 A de operação e 20 A de
curto-circuito por MPPT. Um produto comercial somente poderá ser adotado após conferir
registro Inmetro, documentação técnica, compatibilidade com a rede e aceitação da
distribuidora.

Na saída CA são representados seccionamento bipolar, DPS tipo 2, disjuntor bipolar,
quadro dedicado, medição bidirecional e ponto de conexão com a instalação. Ajustes de
anti-ilhamento e qualidade da energia são funções do equipamento e da conexão
regulamentada; o estudo não inventa limiares ou tempos de atuação.

## Identificação de cabos e rotas conceituais

A prancha 06 relaciona `FV-S1 / R-CC-801` e `FV-S2 / R-CC-802` à string box, mostrando
cada saída até seu MPPT correspondente. O trecho CA inversor–quadro usa a referência
`CA-INV / R-CA-801`; quadro–ponto de conexão usa `CA-PCC / R-CA-802`. Também constam
`PE-MOD / R-PE-801` e `PE-EQP / R-PE-802`, associados conceitualmente ao BEP-801. Os
comprimentos indicados reproduzem as hipóteses de `lista-cabos.csv`: 20 m por string CC,
15 m para CA-INV, 5 m para CA-PCC, 25 m para PE-MOD e 8 m para PE-EQP.

`COM-INV / R-COM-801`, com 10 m assumidos, é opcional e aparece apenas como referência;
seu ponto remoto e trajeto não foram definidos. Nenhuma dessas distâncias veio de
levantamento do imóvel. As linhas servem para rastrear os circuitos no estudo e não
representam posições, comprimentos ou caminhos de instalação reais.

## Aterramento e proteção contra surtos

Molduras, estrutura de suporte, invólucros metálicos, string box, inversor e quadro são
interligados ao barramento equipotencial principal conceitual. Os DPS CC e CA têm
caminhos curtos ao PE. A integração com eletrodo e SPDA existentes depende de inspeção,
análise de risco, separação, coordenação e das edições vigentes das normas aplicáveis.

## Funcionamento esperado

Com irradiância e tensões dentro dos limites, o inversor acompanha os pontos de máxima
potência das duas entradas e injeta energia na instalação conectada à rede. Cargas
locais consomem parte da geração e o excedente pode circular pelo medidor conforme as
regras aplicáveis. Abertura de seccionadores, atuação de proteção, perda de rede ou
autodiagnóstico deve impedir a injeção conforme o equipamento homologado.

## Estudo de energia

A prancha 07 demonstra como a estimativa didática anual muda quando se variam HSP e PR,
mantendo a potência CC em 6,60 kWp. O caso-base preserva 5,2 h/dia e PR 0,78. As demais
combinações são cenários matemáticos escolhidos para estudo, sem vínculo com localidade,
clima observado ou probabilidade de ocorrência. A tabela e os resultados reproduzíveis
estão em [sensibilidade-energia.csv](sensibilidade-energia.csv). Uma previsão local
depende de dados meteorológicos e de implantação ainda não fornecidos.

## Limites

Não há simulação eletromagnética, medição solar, curva diária, ensaio, produção real,
modelo de rede, seletividade, estudo de SPDA, cálculo estrutural, autorização de acesso,
ART, memorial de aprovação ou comissionamento. A energia anual calculada é apenas uma
estimativa paramétrica e não uma promessa de desempenho.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
