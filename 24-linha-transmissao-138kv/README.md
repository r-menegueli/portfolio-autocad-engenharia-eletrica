# Linha aérea de transmissão 138 kV, 30 km

Estudo **acadêmico e conceitual** para portfólio. Abrange traçado e perfil sintéticos, vão nominal 300 m, geometria conceitual de fases, flecha e tração, torres de suspensão/ancoragem, fundações, aterramento e bays terminais.

## Conteúdo

- 10 pranchas A3 em `fonte/` (DXF editável) e `exports/` (PDF, SVG e PNG).
- Memorial, critérios, memória de cálculo, referências e inspeção visual.
- Parâmetros centrais exportados de `portfolio.toml` para `dados/parametros.csv`.
- Análises MATLAB em `matlab/calculos/run_analysis.m`; resultados CSV e gráficos em `resultados/`.
- Modelo dinâmico Simulink: `não aplicável neste projeto`.

## Reprodução

Execute `matlab/calculos/run_analysis.m` no MATLAB R2026a (ou versão compatível). Para reconstruir o modelo Simulink, execute `matlab/calculos/build_model.m`. A rotina de verificação local é `fonte/validar_projeto_24.py`. Gere novamente DXFs/derivados com `python fonte/gerar_projeto_24.py` a partir da raiz do repositório.

## Limites

Estudo conceitual de uma LT aérea de 138 kV com corredor e cotas explicitamente sintéticos. Reúne fluxo de potência por modelo nominal π, estimativa mecânica compatível simplificada, envelopes de flecha e tabelas de arranjo. A verificação térmica confronta os cenários com as premissas e sinaliza margem negativa para revisão. Não representa levantamento topográfico, servidão, licenciamento, travessias, cálculo estrutural ou especificação comercial.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
