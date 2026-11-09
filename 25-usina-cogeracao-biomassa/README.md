# Usina de cogeração a biomassa, 25 MW

Estudo **acadêmico e conceitual** para portfólio. Abrange gerador síncrono de 13,8 kV, conexão via transformador 40 MVA a 138 kV, AVR, governador, sincronismo, proteção, auxiliares, balanço de vapor e energia e aterramento.

![Prévia das dez pranchas do P25](pranchas-preview.png)

## Conteúdo

- 10 pranchas A3 em `fonte/` (DXF editável) e `exports/` (PDF, SVG e PNG).
- Memorial, critérios, memória de cálculo, referências e inspeção visual.
- Parâmetros centrais exportados de `portfolio.toml` para `dados/parametros.csv`.
- Análises MATLAB em `matlab/calculos/run_analysis.m`; resultados CSV e gráficos em `resultados/`.
- Recalculo independente dos balanços estáticos em `validacao/calculos_independentes_p25.py`, com testes em `validacao/test_calculos_independentes_p25.py`.
- Alternativa dinâmica Python de oito cenários, com sinais de tensão, frequência, potência e corrente, em `validacao/simulacao_dinamica_python_p25.py`; a variação de potência é uma referência mecânica do governador, não um degrau físico de carga nem execução do Simulink.
- Modelo dinâmico Simulink: `modelo_cogeracao_dinamico.slx`.

## Reprodução

Execute `python 25-usina-cogeracao-biomassa/validacao/calculos_independentes_p25.py` para regenerar os três balanços estáticos sem MATLAB; execute `python -m pytest -q 25-usina-cogeracao-biomassa/validacao/test_calculos_independentes_p25.py` para verificá-los. `matlab/calculos/run_analysis.m` recalcula os mesmos balanços e, por padrão, executa a série dinâmica existente no MATLAB R2026a (ou compatível). Para reconstruir o modelo Simulink, execute `matlab/calculos/build_model.m`. A rotina de verificação estrutural CAD é `fonte/validar_projeto_25.py`. Gere DXFs/derivados com `python scripts/engineering_studies.py --project p25` a partir da raiz.

Para reproduzir a alternativa dinâmica quando MATLAB não puder ser iniciado: `python 25-usina-cogeracao-biomassa/validacao/simulacao_dinamica_python_p25.py`. Os oito cenários Python geram 8.008 amostras e têm quatro testes. `resposta-cenarios-python.png` separa os degraus de referência mecânica; `resposta-afundamento-python.png` mostra os cenários de tensão reduzida. Nenhum dos dois é execução do Simulink.

## Limites

Estudo conceitual de cogeração com balanços elétrico, térmico e de combustível, correntes de operação/placa e curto trifásico equivalente de rede e gerador. O curto usa a reatância transitória informada e não substitui estudo segundo norma ou dados de máquina. A alternativa dinâmica Python é uma aproximação RK4 reduzida, sem rede detalhada, limitador de corrente ou proteção; o degrau de entrada é na referência mecânica, e ainda não há modelo de carga local/auxiliar nem resposta de frequência da rede. No ensaio externo sintético de 0,2 pu por 0,12 s, o cálculo chega a cerca de 5,54 kA e permanece oscilatório aos 5 s, terminando com potência ativa negativa. Esse resultado não demonstra a suportabilidade do gerador nem pode orientar curto, proteção ou seleção de equipamento. O arquivo Simulink usa blocos padrão e equações médias em pu, não blocos elétricos de máquina; sua execução atual não foi confirmada nesta revisão e ele não valida estabilidade, controles de fabricante ou requisitos de conexão.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
