# Memória de cálculo — P24

## Modelo elétrico

Para feixe de dois subconductores por fase, a resistência CA por fase é `Rac,75/n`. A indutância positiva-sequência equivalente por quilômetro é `L' = 2×10⁻⁴ ln(GMD/GMRb)` H/km, com `GMRb = sqrt(GMRsub·dfeixe)`. A capacitância por metro usa `C' = 2π ε0 / ln(GMD/rc)`, com `rc = sqrt(rsub·dfeixe)`. Para as distâncias 7,5/7,5/15 m: GMD = 9,449 m, GMRb = 0,06759 m, X ≈ 0,37249 Ω/km e C' ≈ 11,50 pF/m.

O modelo nominal π de 30 km usa `A=D=1+YZ/2`, `B=Z(1+YZ/4)`, `C=Y(1+YZ/4)`. Cada caso mantém 138 kV linha-linha no terminal receptor e calcula `Ir = conj(S/(√3·Vll))`, `Vs = A·Vr+B·Ir`, `Is=C·Vr+D·Ir`, perdas `Penvio−Precebimento` e regulação relativa à tensão nominal. É uma análise fasorial equilibrada de regime permanente; não é estudo de fluxo de uma rede com barramentos múltiplos.

### Resultados elétricos da matriz

- 9 combinações: 50/100/140 MW com fp 0,90/0,95/1,00.
- Caso de maior corrente: 140 MW e fp 0,90 — 650,80 A; perdas 1,627 MW; tensão calculada no terminal de envio 145,092 kV (regulação de 5,139% em relação a 138 kV no terminal receptor).
- Caso de 140 MW e fp 1,00 — 585,72 A; perdas 1,327 MW; tensão calculada no terminal de envio 139,669 kV.

As tensões e perdas dependem da hipótese de fonte/carga; nenhum limite de tensão ou critério de conexão foi fornecido. O valor de envio não é uma recomendação de tap nem um limite operacional.

## Triagem térmica

O calor de convecção, radiação e insolação é representado por `qconv = π·d·h·(Tc−Ta)`, `qrad = π·d·ε·σ[(Tc+273,15)^4−(Ta+273,15)^4]`, `qsolar = α·S·d` e `I = sqrt[(qconv+qrad−qsolar)/Rac,75]`. O modelo cruza cada uma das 9 condições ambiente/vento com a maior corrente elétrica da matriz e soma dois subconductores ideais em paralelo.

- Pior cenário de triagem: 45 °C e 0 m/s — 446,02 A por subconductor, 892,04 A no feixe.
- Margem mínima em relação a 650,80 A: 27,04% sobre a capacidade calculada do feixe.
- Com 25 °C e 1 m/s, os coeficientes simplificados produzem aproximadamente 914,91 A por subconductor, perto do valor de catálogo de 910 A; diferença de 0,54%. Isso é apenas uma comparação pontual, não valida o método térmico.

A convecção usada é uma aproximação de triagem. A IEEE 738-2023 descreve um método numérico de corrente-temperatura, mas esta rotina não implementa integralmente o padrão nem seleciona clima de projeto. Portanto, a margem não é rating aprovado nem capacidade térmica contínua demonstrada.

## Compatibilidade mecânica de um vão

Peso próprio `wv = m·g` e vento transversal `ww = 0,5·ρ·Cd·d·v²` são combinados como `we = hypot(wv,ww)`. A flecha vertical é `fv = wv·L²/(8H)`; o deslocamento transversal idealizado é `fh = ww·L²/(8H)`; a flecha resultante no plano de cargas é `fr = we·L²/(8H)`. A tensão horizontal `H` é obtida por compatibilidade aproximada de comprimento elástico entre o estado de referência (25 kN, 20 °C) e o estado avaliado. A tração no apoio soma geometricamente a componente horizontal e metade da carga distribuída resultante no vão.

Foram calculadas 900 linhas (100 vãos × 3 temperaturas × 3 ventos mecânicos). No vão de 300 m:

- Flecha vertical máxima: 9,046 m a 75 °C e vento nulo.
- Deslocamento transversal máximo: 6,55 m no caso de 75 °C e 30 m/s.
- Tração no apoio máxima: 32,76 kN no caso de 20 °C e 30 m/s, equivalente a 23,45% da carga de ruptura bruta de catálogo.
- Menor clearance vertical calculado no perfil sintético: 12,679 m; esse valor não inclui a translação lateral do condutor sobre uma topografia em coordenadas 2D, balanço de cadeia, movimento de isolador, vento não uniforme, tolerâncias ou combinações normativas.

O cálculo parabólico de um vão isolado não substitui catenária, estados inicial/final, creep, vãos reguladores, tensão de montagem, cargas combinadas normativas, fadiga, vibração, galope, blowout/clearance lateral, estrutura da torre ou fundação. O critério comparativo de 8 m é ilustrativo e não é atribuído a norma.

## Rastreabilidade e execução

`portfolio.toml` é a fonte dos valores ajustáveis; `dados/parametros.csv` é a extração numérica e `dados/origem-parametros.csv` separa dados de catálogo, hipóteses e limitações. `matlab/calculos/run_analysis.m` contém a formulação principal e exporta as tabelas; `matlab/testes/test_project_24.m` testa as saídas MATLAB. Nesta revisão, o MATLAB R2026a gravou as tabelas antes de falhar ao montar uma barra de cores por falta de memória. A matriz mecânica atualizada e os seis gráficos foram regenerados pelo fallback Python `validacao/plotar_resultados_p24.py` e conferidos por quatro testes automatizados em `validacao/test_resultados_p24.py`. O relatório registra essa diferença de ferramentas; os testes Python não são apresentados como teste MATLAB.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação, energização ou operação sem projeto executivo, verificações específicas e responsabilidade profissional habilitada.
