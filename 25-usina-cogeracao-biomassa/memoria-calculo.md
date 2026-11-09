# Memória de cálculo — Usina de cogeração a biomassa, 25 MW

## Método

I=S/(√3V); Q=P·tan(arccos(fp)); exportação líquida P=Pg−Paux. Energia de combustível = fluxo mássico × PCI; vapor útil = eficiência da caldeira × entrada térmica; rendimento útil conjunto usa potência elétrica bruta mais vapor útil dividido pela entrada do combustível. Curto-circuito é calculado por equivalente em pu com a impedância presumida do transformador. Dinâmica usa equação de oscilação, governador de primeira ordem, AVR de primeira ordem e curva potência-ângulo simplificada durante degrau de referência e afundamento de tensão.

## Fonte de dados e rastreabilidade

`portfolio.toml` é a fonte única dos parâmetros ajustáveis. O gerador exporta as folhas achatadas para `dados/parametros.csv`, preservando nome, valor, unidade e referência de origem. `matlab/calculos/run_analysis.m` lê esse CSV e gera os resultados; os arquivos CSV em `resultados/tabelas/` são saídas regeneráveis, não dados medidos.

## Precisão e validade

A precisão numérica dos cálculos é limitada pelas simplificações indicadas acima. Hipóteses sintéticas não devem ser usadas para dimensionar, contratar, fabricar, instalar ou operar. Antes de uso real são necessários dados locais, análise multidisciplinar e revisão independente por profissional legalmente habilitado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
