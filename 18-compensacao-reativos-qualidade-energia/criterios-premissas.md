# Critérios e premissas — P18

## Hipóteses explícitas

| Parâmetro | Valor de estudo | Observação |
| --- | ---: | --- |
| Tensão secundária | 400 V | Nominal ilustrativa |
| Transformador TR-01 | 1,0 MVA; 13,8/0,4 kV | Não dimensionado por estudo de carga |
| Carga linear | 400 kW | Hipótese |
| Carga com VFD | 200 kW | Hipótese; espectro não fornecido |
| Potência ativa total | 600 kW | Soma nominal ilustrativa |
| FP inicial | 0,80 indutivo | Caso-base aritmético |
| FP-alvo | 0,95 | Alvo de comparação, não requisito regulatório |
| Banco BC-01 | 300 kvar; 12 × 25 kvar | Arranjo didático, sem seleção de equipamento |

## Critérios de cálculo

O fator de potência é tratado como deslocamento fundamental no cálculo do caso-base. Calcula-se `Q = P × tan(arccos(FP))`; a potência reativa de correção é a diferença entre o Q inicial e o Q correspondente ao alvo. A potência aparente é `S = √(P² + Q²)` e a corrente estimada é `I = S/(√3 × V)` em sistema trifásico equilibrado.

As correntes não incluem correntes harmônicas, desequilíbrio, perdas, queda de tensão, variação de tensão, tolerância de capacitores, temperatura, regime de sobrecarga ou correntes transitórias de energização.

## Sensibilidade e degraus

Com 600 kW, FP 0,80, Q inicial de 450 kvar e alvo 0,95, o Qc contínuo calculado é 252,8 kvar. Um banco hipotético de degraus de 25 kvar permite representar 250 kvar (10 estágios) e 275 kvar (11 estágios). Os resultados aproximados são FP 0,949 e 0,960, respectivamente. A curva CSV demonstra também cenários de 50% de potência e FP diferente para ilustrar a necessidade de controle variável.

## Qualidade de energia

Nenhum conteúdo harmônico foi inventado como medição. Os VFDs motivam o levantamento, mas não provam distorção excessiva. A decisão por filtro passivo, filtro ativo ou dessintonia exige medições repetíveis, impedância de fonte, estrutura espectral, cargas simultâneas, limites aplicáveis e verificação de ressonância.

## Itens em aberto

1. Perfil horário de P, Q, FP, tensão e corrente no PCC.
2. Espectro harmônico/inter-harmônico e classe/método do analisador.
3. Dados de curto-circuito e impedância do sistema no PCC.
4. Tolerância dos capacitores, tensão eficaz, corrente RMS, vida, ventilação e ambiente.
5. Tipo de comutação, restrições de manobra, corrente de inrush, proteção e descarga.
6. Avaliação de ressonância e eventual dimensionamento de reatores ou filtros.
7. Metas de desempenho definidas pelo proprietário e requisitos do agente de rede.
