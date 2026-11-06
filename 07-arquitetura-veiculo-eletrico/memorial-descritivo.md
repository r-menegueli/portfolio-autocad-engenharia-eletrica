# Memorial descritivo - Projeto 07

## Finalidade

O EV-07 é uma arquitetura elétrica acadêmica criada para organizar, em onze pranchas,
o fluxo de energia, a alimentação de controle, os permissivos de alta tensão, a rede de
comunicação e duas estratégias conceituais de acionamento de um motor de indução.

## Fluxo de energia

A energia parte da BAT-HV-701, passa pelo desconector manual MSD-701, fusível F701 e
contatores KMN-701/KMP-701. A PDU-HV-701 distribui o barramento ao INV-701 e ao
DCDC-701. O inversor sintetiza tensões trifásicas U/V/W para o IM-701; em operação
regenerativa conceitual, o fluxo pode inverter-se, condicionado pelos limites do
inversor, BMS e bateria. O conversor CC-CC alimenta o barramento de 14 V e mantém a
bateria auxiliar, que energiza VCU, BMS, sensores, comunicação e bobinas.

## Pré-carga e contatores

Após chave ligada e permissivos válidos, fecha-se primeiro KMN-701. KPR-701 insere
RPR-701 no caminho positivo e carrega o capacitor equivalente CCDC-701. Quando a razão
VDC/VBAT atinge o limiar proposto dentro do timeout, KMP-701 fecha e KPR-701 abre. A
perda de HVIL, isolação, BMS, sinal de colisão ou emergência comanda a abertura dos
contatores e bloqueia `READY`. Um circuito real requer detecção de contato soldado,
drivers adequados, descarga do barramento e análise de falhas independentes.

A prancha 11 representa a sequência temporal proposta: confirmar permissivos, iniciar
KMN/KPR, aguardar a razão VDC/VBAT, solicitar KMP, confirmar seu retorno auxiliar e
abrir KPR antes de `READY`. O cruzamento ideal de 90% ocorre em 0,506569 s para os
valores acadêmicos R=100 ohm e C=2.200 uF, dentro do timeout proposto de 1,5 s.
Tempos mecânicos, lógica de realimentação e resposta ao timeout permanecem dependentes
de hardware e análise de segurança; o desenho não demonstra essa sequência em veículo.

## Proteções

F701 limita a energia de falhas de alta corrente segundo coordenação ainda não
executada. Fusíveis derivados protegem inversor e CC-CC. BMS supervisiona células,
temperaturas e corrente; IMD-701 supervisiona resistência de isolamento; HVIL-701
detecta abertura de conectores; SDE-701 solicita desconexão de emergência. As carcaças
são equipotencializadas ao chassi, mantendo os polos HV isolados dele.

## Acionamento do motor

O INV-701 recebe referência de torque ou velocidade da VCU-701, aplica limites do BMS
e executa uma estratégia de controle. Em V/f, magnitude de tensão e frequência seguem
uma lei escalar. Em FOC, correntes são transformadas para eixos d-q; malhas de corrente
controlam separadamente as componentes associadas a fluxo e torque. Ambas as cadeias
são diagramas didáticos, não software validado.

## Controle, sensores e comunicação

APPS e BPS usam dois canais para plausibilidade. Correntes de fase, tensão do elo CC,
corrente da bateria, posição/velocidade e temperaturas alimentam BMS, VCU e inversor.
A CAN-PT troca estados e limites entre BMS, VCU, inversor e CC-CC; a CAN-DIAG conecta
diagnóstico por gateway. IDs, taxas e tempos são premissas propostas.

## Interfaces e falhas

A prancha 09 e `matriz-interfaces-falhas.csv` relacionam sinais já listados, mensagens
CAN, estados propostos e reações conceituais para dez eventos. A matriz destaca lacunas
como detecção de contato soldado, temporização, dados obsoletos e rearme. Essas linhas
organizam requisitos para estudo futuro; não definem função de segurança, falha segura,
diagnóstico implementado ou desempenho de hardware.

## Relação com o TCC

O projeto oferece uma base gráfica para discutir controle V/f e FOC de motor de
indução no contexto veicular. Não afirma que a topologia, os parâmetros, os limiares,
as curvas ou os desempenhos aqui mostrados foram construídos, medidos ou validados no
TCC de Rogério Eduardo Moreira Menegueli.

## Responsabilidade e limitações

O EV-07 não é um veículo homologado nem um projeto executivo. Não há HARA, ASIL,
FMEDA, validação de software, ensaio de isolação, análise térmica, coordenação de
proteções, EMC, crashworthiness ou comprovação regulatória.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
