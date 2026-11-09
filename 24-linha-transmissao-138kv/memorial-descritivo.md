# Memorial descritivo — Linha aérea de transmissão 138 kV, 30 km

## Objetivo e escopo

Estudo conceitual de uma LT aérea de 138 kV com corredor e cotas explicitamente sintéticos. Reúne fluxo de potência por modelo nominal π, estimativa mecânica compatível simplificada, envelopes de flecha e tabelas de arranjo. A verificação térmica confronta os cenários com as premissas e sinaliza margem negativa para revisão. Não representa levantamento topográfico, servidão, licenciamento, travessias, cálculo estrutural ou especificação comercial.

## Arranjo representado

O conjunto inclui: traçado e perfil sintéticos, vão nominal 300 m, geometria conceitual de fases, flecha e tração, torres de suspensão/ancoragem, fundações, aterramento e bays terminais. As pranchas são esquemáticas, sem compromisso de escala construtiva, seleção de fabricante, coordenadas de campo ou ajustes aprovados. A convenção gráfica, os layers e a folha A3 seguem o padrão do portfólio.

## Entregáveis e reprodução

A fonte vetorial DXF é mantida em `fonte/`; PDF/SVG/PNG são derivados em `exports/`. `dados/parametros.csv` registra valores e origem no manifesto central. Os scripts MATLAB produzem tabelas e gráficos em `resultados/`; a construção do modelo dinâmico é rastreável em `matlab/calculos/build_model.m` quando houver modelo Simulink.

## Responsabilidade

Dados faltantes, decisões de engenharia e estudos de campo estão enumerados nos critérios e na memória. Nenhum resultado representa aprovação de concessionária, operador, autoridade ou responsável técnico.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
