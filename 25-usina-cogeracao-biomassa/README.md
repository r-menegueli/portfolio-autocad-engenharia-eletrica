# Usina de cogeração a biomassa, 25 MW

Estudo **acadêmico e conceitual** para portfólio. Abrange gerador síncrono de 13,8 kV, conexão via transformador 40 MVA a 138 kV, AVR, governador, sincronismo, proteção, auxiliares, balanço de vapor e energia e aterramento.

## Conteúdo

- 10 pranchas A3 em `fonte/` (DXF editável) e `exports/` (PDF, SVG e PNG).
- Memorial, critérios, memória de cálculo, referências e inspeção visual.
- Parâmetros centrais exportados de `portfolio.toml` para `dados/parametros.csv`.
- Análises MATLAB em `matlab/calculos/run_analysis.m`; resultados CSV e gráficos em `resultados/`.
- Recalculo independente dos balanços estáticos em `validacao/calculos_independentes_p25.py`, com testes em `validacao/test_calculos_independentes_p25.py`.
- Modelo dinâmico Simulink: `modelo_cogeracao_dinamico.slx`.

## Reprodução

Execute `python 25-usina-cogeracao-biomassa/validacao/calculos_independentes_p25.py` para regenerar os três balanços estáticos sem MATLAB; execute `python -m pytest -q 25-usina-cogeracao-biomassa/validacao/test_calculos_independentes_p25.py` para verificá-los. `matlab/calculos/run_analysis.m` recalcula os mesmos balanços e, por padrão, executa a série dinâmica existente no MATLAB R2026a (ou compatível). Para reconstruir o modelo Simulink, execute `matlab/calculos/build_model.m`. A rotina de verificação estrutural CAD é `fonte/validar_projeto_25.py`. Gere DXFs/derivados com `python scripts/engineering_studies.py --project p25` a partir da raiz.

## Limites

Estudo conceitual de cogeração com balanços elétrico, térmico e de combustível, correntes de operação/placa e curto trifásico equivalente de rede e gerador. O curto usa a reatância transitória informada e não substitui estudo segundo norma ou dados de máquina. O modelo dinâmico utiliza blocos Simulink padrão e equações médias em pu; não usa blocos elétricos de máquina nem valida estabilidade transitória, controles do fabricante ou requisitos de conexão. A matriz de cenários dinâmicos solicitada ainda está incompleta e a simulação atual não foi reexecutada nesta revisão.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
