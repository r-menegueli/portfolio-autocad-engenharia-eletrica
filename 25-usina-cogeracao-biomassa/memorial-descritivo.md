# Memorial descritivo — Usina de cogeração a biomassa, 25 MW

## Objetivo e escopo

Estudo conceitual de cogeração com balanços elétrico, térmico e de combustível, verificação preliminar de correntes e equivalente dinâmico de máquina síncrona ligado a barramento infinito. A simulação usa blocos Simulink padrão e equações médias em pu; não usa blocos elétricos de máquina nem valida estabilidade transitória, controles do fabricante ou requisitos de conexão.

## Arranjo representado

O conjunto inclui: gerador síncrono de 13,8 kV, conexão via transformador 40 MVA a 138 kV, AVR, governador, sincronismo, proteção, auxiliares, balanço de vapor e energia e aterramento. As pranchas são esquemáticas, sem compromisso de escala construtiva, seleção de fabricante, coordenadas de campo ou ajustes aprovados. A convenção gráfica, os layers e a folha A3 seguem o padrão do portfólio.

## Entregáveis e reprodução

A fonte vetorial DXF é mantida em `fonte/`; PDF/SVG/PNG são derivados em `exports/`. `dados/parametros.csv` registra valores e origem no manifesto central. Os scripts MATLAB produzem tabelas e gráficos em `resultados/`; a construção do modelo dinâmico é rastreável em `matlab/calculos/build_model.m` quando houver modelo Simulink.

## Responsabilidade

Dados faltantes, decisões de engenharia e estudos de campo estão enumerados nos critérios e na memória. Nenhum resultado representa aprovação de concessionária, operador, autoridade ou responsável técnico.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
