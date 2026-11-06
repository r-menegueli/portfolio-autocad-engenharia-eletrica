# Critérios técnicos e premissas

## 1. Natureza dos valores

Todos os valores abaixo são premissas acadêmicas explícitas. Não representam medição,
catálogo escolhido, cálculo executivo ou condição garantida de uma instalação real.

## 2. Dados de projeto adotados

| Grandeza | Premissa | Consequência documental |
|---|---:|---|
| Rede | 380 V, 3 fases, 60 Hz, TN-S | equipamentos e isolação compatíveis com 380-480 Vca |
| Curto-circuito presumido no painel | 5 kA eficazes | Q1 adotado com capacidade de interrupção de 10 kA |
| Motor M1 | 7,5 kW, 4 polos, 380 V, 15,5 A | corrente de placa usada na proteção térmica do VFD |
| Rendimento assumido | 0,89 | usado somente na verificação de ordem de grandeza |
| Fator de potência assumido | 0,82 | usado somente na verificação de ordem de grandeza |
| Carga mecânica | bomba centrífuga de torque variável | perfil V/f quadrático como ponto de partida |
| Temperatura ambiente | 30 °C | sem fator de correção térmica nesta etapa |
| Altitude | até 1.000 m | sem desclassificação por altitude nesta etapa |
| Distância painel-motor | 20 m | cabo W02 sem filtro de saída nesta premissa |
| Tensão de comando | 24 Vcc | PS1 de 2,5 A, com reserva a confirmar |
| Invólucro | IP54, 800 x 600 x 300 mm | layout e ventilação ainda conceituais |

## 3. Verificação da corrente do motor

Para conferência de ordem de grandeza, sem substituir os dados de placa:

`I = P / (raiz(3) x V x rendimento x fator de potência)`

Com as premissas: `I = 7.500 / (1,732 x 380 x 0,89 x 0,82) = 15,63 A`.

Adota-se 15,5 A como corrente nominal de placa para parametrização inicial. A pequena
diferença confirma a coerência da hipótese, mas o valor real deve vir da placa do motor.

## 4. Seleção conceitual dos componentes

- **Q0:** seccionadora tripolar, 32 A, categoria AC-23A, bloqueável em desligado.
- **Q1:** disjuntor tripolar, 25 A, capacidade de interrupção mínima 10 kA em 380 V.
- **DPS1:** DPS tipo 2, tripolar, tensão contínua compatível com rede de 380 V e TN-S.
- **VFD1:** classe 380-480 V, potência nominal 11 kW e corrente de saída mínima 17 A.
  A margem não autoriza uso sem conferir regime, sobrecarga, temperatura e fabricante.
- **Q2:** disjuntor bipolar de comando, 2 A, adequado à corrente de magnetização de PS1.
- **PS1:** entrada compatível com 380-480 Vca e saída 24 Vcc/2,5 A.
- **KSR1:** relé de segurança de dois canais, rearme manual monitorado por botão S5
  dedicado e saídas adequadas às entradas STO específicas de VFD1. S5 não é o reset de
  falha do inversor; não se declara categoria, PL ou SIL.
- **S3:** seletor conceitual de três posições LOCAL-0-REMOTO. Os blocos de contato e a
  comutação entre comandos/referências ainda dependem da arquitetura e dos componentes
  selecionados; posições LOCAL e REMOTO devem ser mutuamente exclusivas.
- **Painel:** aço pintado, IP54, 800 x 600 x 300 mm, com placa, ventilação e barra PE.

## 5. Cabos e segregação

W01 é assumido como 4G4 mm² cobre, isolação 0,6/1 kV. W02 é cabo simétrico blindado
para inversor, com três condutores de 4 mm² e três condutores PE de 2,5 mm². As seções
foram adotadas para o exercício; capacidade de corrente, queda de tensão, curto-circuito,
agrupamento e coordenação devem ser recalculados com o método real de instalação.

W03, W05 e W06 são blindados. Sinais analógicos e PTC seguem em canaleta distinta de
potência, com cruzamentos a 90 graus quando inevitáveis. A terminação de blindagem e o
conceito de equipotencialização devem seguir a documentação dos equipamentos reais.

## 6. Parâmetros iniciais conceituais de VFD1

| Parâmetro | Valor adotado | Observação |
|---|---:|---|
| Tensão nominal do motor | 380 V | substituir pelo dado de placa |
| Corrente nominal do motor | 15,5 A | base da proteção térmica eletrônica |
| Frequência nominal | 60 Hz | substituir pelo dado de placa |
| Velocidade nominal | 1.760 rpm | hipótese para motor de 4 polos |
| Frequência mínima | 5 Hz | confirmar refrigeração e faixa da carga |
| Frequência máxima | 60 Hz | sem operação acima da frequência-base |
| Rampa de aceleração | 5 s | confirmar torque e processo |
| Rampa de desaceleração | 8 s | evita sobretensão; confirmar inércia |
| Limite de corrente | 18 A | hipótese inferior à capacidade do VFD e superior a In |
| Método de controle inicial | V/f quadrático | adequado à carga centrífuga assumida |
| Rearme após falta de energia | desabilitado | evita partida não comandada |
| Fonte de comando | local/0/remoto por S3 | sem transferência automática em marcha; contatos e lógica pendentes |

## 7. Referências técnicas de orientação

- ABNT NBR 5410: instalações elétricas de baixa tensão;
- ABNT NBR IEC 61439-1 e 61439-2: conjuntos de manobra e controle de baixa tensão;
- IEC 60204-1: equipamento elétrico de máquinas;
- IEC 61800-5-1: requisitos de segurança elétrica de acionamentos;
- IEC 61800-5-2: segurança funcional e função STO;
- IEC 60617 e IEC 61082-1: símbolos e preparação de documentos eletrotécnicos;
- NR-10: segurança em instalações e serviços em eletricidade.

A edição vigente, aplicabilidade e requisitos locais devem ser confirmados por
profissional habilitado antes de qualquer uso fora do contexto acadêmico.

## 8. Pendências para um projeto executivo

Levantamento da rede, corrente de curto-circuito, coordenação e seletividade; dados de
placa e curva da carga; método de instalação dos cabos; harmônicas e EMC; filtro de
entrada ou saída; resistor de frenagem; ventilação e balanço térmico; análise de risco;
PL/SIL e tempo de parada; arquitetura do PLC; ensaios, inspeções e comissionamento.

### 8.1 Proteção e coordenação

O valor de 5 kA é uma hipótese de curto-circuito, e 10 kA é a capacidade de interrupção
indicada para Q1 sem modelo ou curva selecionados. A comparação numérica entre esses
valores não comprova adequação. Para avançar, obter a corrente de curto-circuito máxima
e mínima no painel, selecionar os modelos e consultar Icu/Ics na tensão aplicável,
curvas/ajustes, energia passante e tabelas do fabricante para seletividade e retaguarda.
Confirmar também a suportabilidade do conjunto e a corrente condicional de Q0, a
proteção de entrada recomendada para o VFD, o ajuste térmico pelos dados de placa do
motor, a curva de Q2 conforme a partida da fonte, e os parâmetros Uc/Up/TOV e proteção
de retaguarda do DPS. Cabos e barramentos exigem método de instalação, fatores de
correção, queda de tensão e verificação térmica de curto-circuito.

A relação linha a linha está em [protecao-coordenacao.csv](protecao-coordenacao.csv)
e na prancha 07. Todos os itens dessa matriz permanecem pendentes.

### 8.2 Plano de verificação e evidências

A prancha 08 e [plano-verificacao.csv](plano-verificacao.csv) são um plano de
fechamento documental e funcional, não um registro de testes aprovados. Os treze itens
permanecem como `NÃO EXECUTADO`, pois não foram apresentados dados de campo nem
resultados de ensaio. O status não deve ser convertido em aprovado por inferência.

Antes de encerrar qualquer linha, devem existir os dados e as evidências indicados,
critérios e tolerâncias aplicáveis, identificação do modelo e revisão do fabricante,
instrumentos adequados e responsável habilitado. Ensaios de STO e funções de segurança
dependem de requisitos derivados da análise de risco e de validação documentada; esta
matriz não prescreve como executá-los nem estabelece PL/SIL. A linha V13 exige verificar
separadamente o rearme S5/KSR1, o reset S4/X3:9 do VFD e a ausência de partida após
rearme, troca de modo ou retorno de energia. O desenho também não autoriza energização
ou comissionamento.

### 8.3 Sequência operacional

A prancha 09 resume habilitação, comando local/remoto e respostas a emergência,
falha do VFD, falta de energia e troca de modo. O arquivo
[sequencia-estados.csv](sequencia-estados.csv) fornece os estados e textos mostrados.
Essa representação acompanha a sequência descrita neste memorial, mas não prova que
a lógica foi implementada ou ensaiada. Perda de 4–20 mA com parada controlada e alarme
continua hipótese a confirmar no modelo selecionado; tempos de parada, categoria,
PL/SIL e respostas reais dependem de requisitos, equipamentos e validação próprios.
