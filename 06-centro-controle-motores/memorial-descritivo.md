# Memorial descritivo - CCM-06

## Identificação

- Autor: Rogério Eduardo Moreira Menegueli
- Data: 2026-11-05
- Revisão: 03
- Unidades dos desenhos: milímetros
- Natureza: acadêmica e conceitual

## Solução adotada

O CCM-06 recebe o alimentador W600 do QGBT-05, em 380/220 V, 3F+N+PE, 60 Hz e
esquema TN-S conceitual. O disjuntor QG-06 alimenta barramento nominal de 80 A e três
ramais funcionalmente distintos:

- M-601, bomba de 5,5 kW, por partida direta com QF-601, KM-601 e FR-601;
- M-602, esteira de 3,0 kW, por reversão com QF-602, KM-602F, KM-602R, trava
  mecânica IM-602 e FR-602 comum;
- M-603, ventilador de 7,5 kW, por VFD-603 de 11 kW e QF-603.

## Integração e segurança funcional

KSR-601 recebe os dois canais do botão de emergência S0-601. Seus contatos de saída
retiram a habilitação das bobinas KM-601, KM-602F e KM-602R e comandam STO A/B do
VFD-603. Esta representação não declara categoria, PL ou SIL: arquitetura, diagnóstico,
tempo de parada e validação dependem de análise de risco da máquina real.

Na reversão, contatos auxiliares NF cruzados impedem o comando elétrico simultâneo dos
contatores e IM-602 impede fechamento mecânico simultâneo. FC-602F interrompe somente
o sentido frente e FC-602R somente o reverso. A troca de sentido exige parada.

O circuito da bomba usa selo de KM-601, mas o retorno da emergência ou da alimentação
não causa partida automática. O ventilador recebe comandos por entradas digitais e
referência 0-10 V; não há contator de manobra entre VFD-603 e M-603.

## Aterramento, EMC e segregação

PE-06 recebe o condutor de proteção do alimentador e atende invólucro, portas,
componentes e motores. N-06 permanece isolada de PE-06. O cabo W603B é blindado, com
terminação de 360 graus nas duas extremidades como premissa EMC. Potência, comando,
STO e sinais analógicos ocupam rotas e canaletas segregadas.

O balanço P06-09 relaciona, para cada carga, o fator de demanda declarado e as
potências ativa e aparente instaladas e demandadas. A corrente de cada ramal é exibida
com base na potência aparente instalada; para W600, a corrente equivalente usa a
potência aparente demandada total. Os fatores e os dados de proteção do alimentador
continuam premissas acadêmicas, sem verificação de simultaneidade ou dimensionamento
executivo.

## Limitações e responsabilidade

Correntes, seções, proteções, comprimentos e dimensões são premissas coerentes para o
exercício. Faltam levantamento real, dados de placa, estudo de curto-circuito,
seletividade, coordenação, partida, aquecimento, arco elétrico e análise de risco.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
