# Memorial descritivo — Usina de cogeração a biomassa, 25 MW

## Objetivo e escopo

Estudo conceitual de cogeração com balanços elétrico, térmico e de combustível, verificação preliminar de correntes e equivalente de curto trifásico de rede e gerador. A potência aparente calculada do gerador em operação é 27,78 MVA, abaixo da placa assumida de 32 MVA; a corrente calculada em operação é 1.162 A, abaixo da corrente nominal de 1.339 A. O transformador exporta 23,86 MVA no cenário nominal, cerca de 59,7% da potência assumida de 40 MVA. A triagem de curto usa X'd e hipóteses explicitadas na memória, sem corrente subtransitória ou componente CC.

O modelo dinâmico existente usa blocos Simulink padrão e equações médias em pu; não usa blocos elétricos de máquina. A série atualmente armazenada cobre um afundamento de tensão e um degrau de potência mecânica, mas não todos os oito cenários solicitados. A versão atualizada do cálculo estático e a nova matriz dinâmica ainda precisam ser executadas no MATLAB para confirmar o modelo e regenerar as séries e gráficos.

## Arranjo representado

O conjunto inclui: gerador síncrono de 13,8 kV, conexão via transformador 40 MVA a 138 kV, AVR, governador, sincronismo, proteção, auxiliares, balanço de vapor e energia e aterramento. As pranchas são esquemáticas, sem compromisso de escala construtiva, seleção de fabricante, coordenadas de campo ou ajustes aprovados. A convenção gráfica, os layers e a folha A3 seguem o padrão do portfólio.

## Entregáveis e reprodução

A fonte vetorial DXF é mantida em `fonte/`; PDF/SVG/PNG são derivados em `exports/`. `dados/parametros.csv` registra valores centrais e `dados/origem-parametros.csv` documenta sua classe de evidência. `validacao/calculos_independentes_p25.py` produz os balanços estáticos em `resultados/tabelas/` e é conferido por testes Python. `matlab/calculos/run_analysis.m` espelha essas equações e executa a etapa dinâmica; `matlab/calculos/build_model.m` constrói o modelo Simulink.

## Responsabilidade

Dados faltantes, decisões de engenharia e estudos de campo estão enumerados nos critérios e na memória. Nenhum resultado representa aprovação de concessionária, operador, autoridade ou responsável técnico.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
