# Estratégia PI inicial

O controlador LIC-101 utiliza inicialmente apenas as ações proporcional e integral. A derivativa permanece desabilitada por causa do ruído típico da medição de nível e porque a dinâmica do reservatório já é integradora.

| Parâmetro | Valor inicial | Observação |
|---|---:|---|
| SP | 60% | Ajustável dentro da faixa operacional aprovada |
| Kc | 0,8 % saída/% PV | Valor acadêmico para partida de comissionamento |
| Ti | 120 s | Refinar por teste controlado |
| Td | 0 s | Ação derivativa desabilitada |
| Saída mínima | 20 Hz | Aplicável com bomba habilitada |
| Saída máxima | 60 Hz | Limite conceitual do acionamento |
| Rampa | 1 Hz/s | Limitação proposta de variação |

O erro deve ser implementado de modo que nível abaixo do setpoint aumente a frequência. A convenção “direta/reversa” depende do fabricante; a verificação funcional deve confirmar o sentido antes da liberação. Anti-windup impede acumulação integral durante saturação ou bloqueio, e rastreamento da saída manual permite transferência sem salto.

## Procedimento de sintonia proposto

1. Confirmar escalas, sentido de ação e limites com a bomba desacoplada ou em condição segura.
2. Operar em manual e obter resposta a pequenos degraus dentro dos limites aprovados.
3. Estimar ganho e constante de tempo do processo.
4. Aplicar sintonia conservadora, validar sem ultrapassar LSH-101 e registrar tendências.
5. Testar perturbações de consumo, trocas de modo, saturação, falha do transmissor e bloqueio LSHH-101.

Os valores acima não são uma sintonia definitiva e não autorizam operação de uma instalação real.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
