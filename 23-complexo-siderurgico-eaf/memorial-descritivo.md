# Memorial descritivo — Complexo siderúrgico com forno elétrico a arco (EAF)

## Objetivo e escopo

Estudo de alimentação de uma aciaria elétrica com análise preliminar de demanda, corrente de curto-circuito, compensação reativa e espectro harmônico sintético. O conteúdo delimita premissas e interfaces para evolução do projeto; não seleciona fabricante, ajuste de relé, filtro ou equipamento de proteção.

## Arranjo representado

O conjunto inclui: recepção em 138 kV, distribuição em 34,5 kV, forno 30 MVA com secundário conceitual de 1 kV, compensação dinâmica, filtros harmônicos, proteção, aterramento e intertravamentos. As pranchas são esquemáticas, sem compromisso de escala construtiva, seleção de fabricante, coordenadas de campo ou ajustes aprovados. A convenção gráfica, os layers e a folha A3 seguem o padrão do portfólio.

## Entregáveis e reprodução

A fonte vetorial DXF é mantida em `fonte/`; PDF/SVG/PNG são derivados em `exports/`. `dados/parametros.csv` registra valores e origem no manifesto central. Os scripts MATLAB produzem tabelas e gráficos em `resultados/`; a construção do modelo dinâmico é rastreável em `matlab/calculos/build_model.m` quando houver modelo Simulink.

## Responsabilidade

Dados faltantes, decisões de engenharia e estudos de campo estão enumerados nos critérios e na memória. Nenhum resultado representa aprovação de concessionária, operador, autoridade ou responsável técnico.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
