# Usina de cogeração a biomassa, 25 MW

Estudo **acadêmico e conceitual** para portfólio. Abrange gerador síncrono de 13,8 kV, conexão via transformador 40 MVA a 138 kV, AVR, governador, sincronismo, proteção, auxiliares, balanço de vapor e energia e aterramento.

## Conteúdo

- 10 pranchas A3 em `fonte/` (DXF editável) e `exports/` (PDF, SVG e PNG).
- Memorial, critérios, memória de cálculo, referências e inspeção visual.
- Parâmetros centrais exportados de `portfolio.toml` para `dados/parametros.csv`.
- Análises MATLAB em `matlab/calculos/run_analysis.m`; resultados CSV e gráficos em `resultados/`.
- Modelo dinâmico Simulink: `modelo_cogeracao_dinamico.slx`.

## Reprodução

Execute `matlab/calculos/run_analysis.m` no MATLAB R2026a (ou versão compatível). Para reconstruir o modelo Simulink, execute `matlab/calculos/build_model.m`. A rotina de verificação local é `fonte/validar_projeto_25.py`. Gere novamente DXFs/derivados com `python fonte/gerar_projeto_25.py` a partir da raiz do repositório.

## Limites

Estudo conceitual de cogeração com balanços elétrico, térmico e de combustível, verificação preliminar de correntes e equivalente dinâmico de máquina síncrona ligado a barramento infinito. A simulação usa blocos Simulink padrão e equações médias em pu; não usa blocos elétricos de máquina nem valida estabilidade transitória, controles do fabricante ou requisitos de conexão.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
