# Memória de cálculo — Complexo siderúrgico com forno elétrico a arco (EAF)

## Método

P=S·fp; Q=S·sen(arccos(fp)); Q alvo=P·tan(arccos(fp alvo)); Q dinâmica requerida=max(0,Q bruto−Q filtros−Q alvo). Corrente trifásica I=S/(√3·V). Curto-circuito no barramento 34,5 kV é estimado na base de 45 MVA: Xfonte=Sbase/Scc da fonte, Zeq=√(Rtransformador²+(Xtransformador+Xfonte)²), Sccbarra=Sbase/|Zeq| e Icc=Sccbarra/(√3·Vbarra). A resistência da fonte foi assumida nula por falta de dado R/X; a resistência do transformador é incluída. THDi ilustrativo = √Σ(Ih/I1)² e usa correntes harmônicas sintéticas cadastradas, sem impedância de rede por frequência nem efeito dos filtros.

## Fonte de dados e rastreabilidade

`portfolio.toml` é a fonte única dos parâmetros ajustáveis. O gerador exporta as folhas achatadas para `dados/parametros.csv`, preservando nome, valor, unidade e referência de origem. `matlab/calculos/run_analysis.m` lê esse CSV e gera os resultados; os arquivos CSV em `resultados/tabelas/` são saídas regeneráveis, não dados medidos.

`validacao/calculos_independentes_p23.py` recalcula balanço, corrente, curto-circuito e THDi sintético a partir do CSV e regenera as tabelas. `dados/origem-parametros.csv` registra a classe, justificativa e limitação de cada entrada. O MATLAB conserva a mesma expressão de impedância; `hypot(R,X)` e `sqrt(R^2+X^2)` são equivalentes e não alteraram o resultado histórico de 5,26298 kA. Corrente harmônica e respostas dinâmicas continuam estimativas conceituais.

## Precisão e validade

A precisão numérica dos cálculos é limitada pelas simplificações indicadas acima. Hipóteses sintéticas não devem ser usadas para dimensionar, contratar, fabricar, instalar ou operar. Antes de uso real são necessários dados locais, análise multidisciplinar e revisão independente por profissional legalmente habilitado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
