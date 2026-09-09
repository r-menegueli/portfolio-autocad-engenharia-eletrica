# Estratégias de controle do motor de indução

## V/f - controle escalar

O controle V/f estabelece uma frequência elétrica e uma magnitude de tensão de
referência. A razão V/f é mantida aproximadamente constante até a frequência-base para
preservar o fluxo; uma compensação de baixa velocidade pode ser proposta para a queda
resistiva. A frequência integrada fornece o ângulo para a modulação do inversor.

Vantagens didáticas: estrutura simples, poucos parâmetros e boa visualização da relação
entre tensão, frequência e velocidade síncrona. Limitações: fluxo e torque permanecem
acoplados, a resposta transitória é menor e o controle em baixa velocidade depende
fortemente das quedas e do escorregamento. O esquema deste projeto não calcula ganhos
nem demonstra desempenho.

## FOC - controle orientado pelo campo

O FOC é uma forma de controle vetorial. Ele transforma as correntes trifásicas pelas
transformações de Clarke e Park para um referencial d-q alinhado ao fluxo do
rotor. A componente `id` é associada à magnetização e `iq` à produção de torque; malhas
PI geram referências de tensão, que retornam ao sistema trifásico e à modulação SVPWM.
Para um motor de indução são necessários parâmetros coerentes da máquina e uma
estimativa de fluxo/escorregamento, com sensor de posição/velocidade ou observador.

Vantagens potenciais: desacoplamento de fluxo e torque, resposta dinâmica superior e
controle preciso em ampla faixa. Limitações: maior custo computacional, sensibilidade a
parâmetros e sensores, necessidade de sintonia e validação do estimador.

## Comparação para o EV-07

| Aspecto | V/f | FOC |
| --- | --- | --- |
| Natureza | escalar | vetorial |
| Entradas mínimas no esquema | frequência e magnitude | correntes, tensão CC, velocidade/posição ou observador |
| Controle de fluxo e torque | acoplado | desacoplado no referencial d-q |
| Complexidade | menor | maior |
| Baixa velocidade | desempenho limitado sem compensações | potencialmente melhor, dependente de sensores/modelo |
| Uso nesta entrega | referência didática simples | proposta didática para estudo ligado ao TCC |

## Limite de interpretação

As duas estratégias são apresentadas como arquiteturas de sinal. Não há código de
controle, parâmetros identificados, simulação fechada, curvas de torque, eficiência,
THD, tempo de resposta nem resultados experimentais atribuídos ao TCC.
