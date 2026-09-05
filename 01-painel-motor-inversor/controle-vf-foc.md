# Relação conceitual com controle V/f e FOC

## Visão geral

O painel elétrico permanece essencialmente o mesmo quando VFD1 opera em controle
escalar V/f ou em controle vetorial orientado a campo (FOC). Q0, Q1, DPS1, STO, bornes,
aterramento e cabos não mudam apenas por causa do algoritmo. O que muda é a forma como
o inversor estima ou mede o estado do motor e calcula as tensões de saída.

## Controle V/f

No controle V/f, o inversor mantém uma relação aproximadamente proporcional entre a
tensão fundamental e a frequência para conservar o fluxo magnético do motor. É uma
estratégia simples, robusta e suficiente para muitas cargas de velocidade variável.

Este projeto adota V/f quadrático como premissa inicial porque a carga acadêmica foi
definida como bomba centrífuga. Nessa família de carga, o torque resistente tende a
crescer com o quadrado da velocidade e a potência com o cubo, o que permite reduzir
consumo em baixa rotação. A parametrização real ainda depende da curva da bomba, faixa
de operação, ressonâncias, ventilação do motor e pressão mínima do processo.

Limitações típicas do V/f incluem menor precisão de velocidade em baixa frequência,
resposta de torque mais lenta e sensibilidade à queda de tensão no estator. O reforço
de torque em baixa velocidade não deve ser aplicado sem medição de corrente e temperatura.

## Controle FOC

O FOC transforma as correntes trifásicas em componentes equivalentes associadas ao
fluxo e ao torque. O regulador controla essas componentes separadamente, aproximando o
comportamento de um motor de corrente contínua. Pode operar sem sensor, a partir de um
modelo do motor, ou com encoder para maior precisão e torque em baixa velocidade.

FOC é conceitualmente preferível quando a aplicação exige resposta dinâmica, controle
de torque, pequena variação de velocidade sob carga ou operação prolongada em baixa
rotação. Exige identificação correta do motor, autoajuste compatível, parâmetros de
placa confiáveis e, em alguns casos, cabo adicional para encoder e alimentação do sensor.

## Impacto nas seis pranchas

| Prancha | V/f | FOC |
|---|---|---|
| Unifilar | sem mudança de topologia | sem mudança, salvo sensor dedicado |
| Potência | VFD1 e W02 iguais | VFD1 deve suportar modo vetorial e corrente requerida |
| Comando | referência e comandos digitais | pode incluir seleção de torque e realimentação |
| Layout | folgas conforme VFD escolhido | pode exigir módulo de encoder e mais bornes |
| Bornes | X2 recebe motor e PTC | encoder exigiria nova régua segregada |
| Campo | W03 atende PTC | cabo de encoder seria adicional e blindado |

## Decisão registrada

A entrega representa o hardware comum e parametriza V/f quadrático como ponto de
partida acadêmico. FOC não foi habilitado silenciosamente nem apresentado como requisito.
Se o levantamento futuro revelar transportador, içamento, extrusora, controle de torque
ou baixa velocidade contínua, a decisão deve ser reaberta e as seis pranchas atualizadas.

Em qualquer modo, a frequência de saída não elimina a necessidade de conferir rotação,
refrigeração, isolamento do motor, tensão de pico no cabo, corrente e limites mecânicos.
