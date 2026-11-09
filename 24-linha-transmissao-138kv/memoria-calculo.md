# Memória de cálculo — Linha aérea de transmissão 138 kV, 30 km

## Método

GMD=(Dab·Dbc·Dca)^(1/3); L'=2×10⁻⁷ ln(GMD/GMR) H/m; C'=2πɛ0/ln(GMD/r) F/m. Fluxo em π nominal: A=D=1+YZ/2, B=Z(1+YZ/4), C=Y(1+YZ/4). Flecha usa aproximação parabólica e compatibilidade de comprimento/elasticidade/temperatura em vão isolado, com vento em carga resultante. Ampacidade é checada por equilíbrio térmico estacionário com h e absorptividade assumidos. Não são modelos de transitórios, estabilidade de fundação, catenária exata, clearance codificado ou coordenação de isolamento.

## Fonte de dados e rastreabilidade

`portfolio.toml` é a fonte única dos parâmetros ajustáveis. O gerador exporta as folhas achatadas para `dados/parametros.csv`, preservando nome, valor, unidade e referência de origem. `matlab/calculos/run_analysis.m` lê esse CSV e gera os resultados; os arquivos CSV em `resultados/tabelas/` são saídas regeneráveis, não dados medidos.

## Precisão e validade

A precisão numérica dos cálculos é limitada pelas simplificações indicadas acima. Hipóteses sintéticas não devem ser usadas para dimensionar, contratar, fabricar, instalar ou operar. Antes de uso real são necessários dados locais, análise multidisciplinar e revisão independente por profissional legalmente habilitado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
