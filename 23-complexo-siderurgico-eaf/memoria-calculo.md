# Memória de cálculo — Complexo siderúrgico com forno elétrico a arco (EAF)

## Método

P=S·fp; Q=S·sen(arccos(fp)); Q alvo=P·tan(arccos(fp alvo)); Q dinâmica requerida=max(0,Q bruto−Q filtros−Q alvo). Corrente trifásica I=S/(√3·V). Curto-circuito no barramento 34,5 kV é estimado pelo equivalente em pu na base de 45 MVA. THDi ilustrativo = √Σ(Ih/I1)². A dinâmica do STATCOM e da tensão é simulada em equivalentes pu agregados por estados contínuos; não é modelo eletromagnético do conversor nem do arco.

## Fonte de dados e rastreabilidade

`portfolio.toml` é a fonte única dos parâmetros ajustáveis. O gerador exporta as folhas achatadas para `dados/parametros.csv`, preservando nome, valor, unidade e referência de origem. `matlab/calculos/run_analysis.m` lê esse CSV e gera os resultados; os arquivos CSV em `resultados/tabelas/` são saídas regeneráveis, não dados medidos.

## Precisão e validade

A precisão numérica dos cálculos é limitada pelas simplificações indicadas acima. Hipóteses sintéticas não devem ser usadas para dimensionar, contratar, fabricar, instalar ou operar. Antes de uso real são necessários dados locais, análise multidisciplinar e revisão independente por profissional legalmente habilitado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
