# Sequência de funcionamento

## Partida automática

1. PLC-101 verifica emergência liberada, KSR-101 pronto, VFD pronto, LSHH-101 inativo e LT-101 válido.
2. O operador seleciona AUTO e confirma a habilitação.
3. LIC-101 assume a saída rastreada, aplica limites e envia referência a VFD-101.
4. O VFD aciona M-101/P-101; a frequência varia para manter TK-101 em 60%.

## Operação esperada

Maior vazão de consumo reduz o nível; LIC-101 eleva gradualmente a frequência e a vazão de entrada. Menor consumo eleva o nível; LIC-101 reduz a frequência. A bomba para quando um intertravamento for acionado ou quando a lógica operacional aprovada assim exigir.

## Parada e falha

- STOP, emergência, LSHH-101, falha do VFD, sinal LT-101 inválido ou tempo máximo excedido retiram o comando de marcha.
- Alarmes ficam memorizados até remoção da causa e reconhecimento.
- Retorno de energia não provoca repartida automática.
- Operação manual mantém limites, alarmes e intertravamentos essenciais.

LA-L-101 em 15% e LA-H-101 em 85% são alarmes declarados na filosofia. A resposta de
processo para esses dois alarmes permanece pendente; esta documentação não lhes atribui
comando de partida ou parada automática. Consulte `matriz-causa-efeito.csv`.

## Testes funcionais mínimos

- Simulação de LT-101 em 4, 12 e 20 mA.
- Teste individual de LSL-101, LSH-101 e LSHH-101.
- Confirmação do sentido da ação da malha.
- Teste da referência e realimentação do VFD.
- Teste de emergência, perda de energia, falha do VFD e rearme.
- Registro de tendências de SP, PV, saída, frequência e alarmes.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
