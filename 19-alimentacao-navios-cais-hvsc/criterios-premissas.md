# Critérios e premissas — P19

## Fatos usados

- A IEC/IEEE 80005-1 descreve sistemas de conexão HVSC em terra e a bordo, com requisitos gerais para distribuição, interface, transformadores/conversores, controle, monitoramento e intertravamento.
- A IEC/IEEE 80005-2 trata de interfaces de dados e procedimentos de comunicação para monitoramento e controle não emergencial; não especifica as funções de emergência cobertas pela parte 1.
- A IEC 61936-1:2021 fornece requisitos gerais para instalações elétricas acima de 1 kV AC até 60 Hz; sua página de escopo exclui instalações a bordo de navios.
- A IEC 62271-200:2021, consolidada com AMD1:2024, cobre conjuntos de manobra e controle em invólucro metálico para AC acima de 1 kV até 52 kV e frequências até 60 Hz.

## Hipóteses do caso-base

- Entrada do porto: 13,8 kV, 60 Hz.
- Saída ilustrativa: 6,6 kV, 60 Hz.
- Potência nominal hipotética do transformador: 4 MVA.
- Demanda aparente hipotética no ponto HVSC: 3,2 MVA.
- O navio atende a essa tensão, frequência, conexão e requisitos de interface; isso é uma hipótese e precisa ser substituído por dados de embarcação compatível.
- A planta é sem escala, sem levantamento topográfico, perfil do cais, dimensões de navio ou comprimento real de cabo.

## Critério de cálculo

Para sistema trifásico equilibrado, a corrente aparente de linha é estimada por `I = S / (√3 × Vlinha)`. Com S = 3,2 MVA, obtêm-se aproximadamente 133,9 A a 13,8 kV e 279,9 A a 6,6 kV. As correntes nominais aritméticas de um transformador de 4 MVA são aproximadamente 167,3 A e 349,9 A, respectivamente. A razão 3,2/4,0 MVA é 80% e serve apenas para conferir a conta; não constitui reserva técnica ou critério de dimensionamento.

## Decisões não tomadas

- Perfil e potência simultânea do navio, regime e fator de potência.
- Compatibilidade de tensão, frequência, sequência de fases, aterramento e aterramento do neutro.
- Conector, quantidade de cabos, comprimento, suporte, tambor, tração, raio de curvatura, resistência ambiental e método de conexão.
- Conversão de frequência ou tensão, quando necessária para uma embarcação específica.
- Correntes de curto-circuito, coordenação, proteção, capacidade de interrupção, seletividade, transformador, compensação e qualidade de energia.
- Topologia, nível de corrente, alimentação, redundância, roteamento e tempo de atuação de qualquer circuito de segurança; consultar a edição consolidada e o anexo aplicável da IEC/IEEE 80005-1.
- Pontos e formato dos dados funcionais, requisitos de cibersegurança e integração com sistemas do terminal.
- Acessibilidade, segregação, barreiras, incêndio, áreas classificadas, proteção ambiental e procedimentos de operação.

Nenhuma hipótese, conta ou referência nesta pasta prova conformidade normativa, dimensionamento ou aptidão para execução.
