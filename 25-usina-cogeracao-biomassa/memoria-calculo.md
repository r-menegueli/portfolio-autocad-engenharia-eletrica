# Memória de cálculo — Usina de cogeração a biomassa, 25 MW

## Método

`I=S/(√3·V)` e `Q=P·tan(arccos(fp))`. A exportação líquida é `Pgerador−Paux`. A energia do combustível é `vazão mássica × PCI / 3,6`; o vapor disponível é a eficiência da caldeira vezes a entrada térmica; o rendimento útil agregado é `(geração elétrica bruta + vapor útil) / entrada do combustível`. Esse rendimento de cogeração não é o rendimento do gerador elétrico.

O curto trifásico é uma triagem fasorial por equivalentes de Thévenin. O equivalente de rede e o transformador são combinados primeiro na base de 40 MVA; o resultado é convertido para a base de 32 MVA do gerador. No barramento de 13,8 kV são somadas as contribuições da rede e da máquina usando `X'd = 0,25 pu`; no lado de 138 kV são referidas pela base do transformador. Não foram fornecidos `X''d`, resistência da rede, motores, tensão pré-falta ou componente CC. Assim, essa estimativa não é corrente inicial segundo IEC 60909 nem base para seleção de disjuntores.

A alternativa dinâmica Python executada usa equação de oscilação, governador e AVR de primeira ordem e curva potência-ângulo agregada. A série exporta oito cenários (8.008 amostras), incluindo afundamento de tensão sintético, referência mecânica e desabilitação de controles; não representa degrau físico de carga nem curto EMT. Os eventos de entrada são integrados como descontinuidades, sem ocultar a sensibilidade restante ao passo. Não há modelo elétrico detalhado de máquina/transformador, carga explícita, rede por frequência, proteção ou limitador de corrente. Frequência e corrente são grandezas derivadas desse modelo conceitual.

## Fonte de dados e rastreabilidade

`portfolio.toml` é a fonte única dos parâmetros ajustáveis. O gerador exporta as folhas achatadas para `dados/parametros.csv`. `validacao/calculos_independentes_p25.py` recalcula e grava os balanços elétricos, o curto equivalente e a energia com a biblioteca padrão do Python; `matlab/calculos/run_analysis.m` espelha essas equações antes da etapa Simulink. Os resultados CSV são regeneráveis, não dados medidos. O curto também é conferido por testes independentes em `validacao/test_calculos_independentes_p25.py`.

## Precisão e validade

A precisão numérica é limitada pelas simplificações indicadas acima. A impedância de 12% do transformador, `X'd`, a rede de 5.000 MVA e os parâmetros dinâmicos são hipóteses, não dados de placa. A série Python foi regenerada e o cálculo estático MATLAB R2026a foi executado; a dinâmica MATLAB/Simulink continua sem execução validada. A resposta Python de 5 s muda materialmente com o passo e chega a potências ativa e correntes acima das bases nominais. Hipóteses sintéticas não devem ser usadas para dimensionar, contratar, fabricar, instalar ou operar. Antes de uso real são necessários dados locais, análise multidisciplinar e revisão independente por profissional legalmente habilitado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
