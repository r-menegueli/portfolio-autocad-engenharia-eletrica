# Memorial descritivo

## 1. Identificação

Projeto acadêmico 01: painel de acionamento de motor de indução trifásico com inversor
de frequência. Autor: Rogério Eduardo Moreira Menegueli. Data-base: 2026-09-05.
Revisão: 02 (gráfica; 2026-11-05).

## 2. Finalidade e limites

O projeto apresenta uma arquitetura didática completa para alimentar, comandar,
proteger e monitorar um motor de indução trifásico M1 por meio do inversor VFD1. As
grandezas e componentes foram definidos como premissas rastreáveis, não como resultado
de levantamento ou dimensionamento executivo.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## 3. Arquitetura elétrica

A alimentação assumida é 380 V, trifásica, 60 Hz, em esquema TN-S. O cabo W01 chega à
régua X1 e segue pela seccionadora Q0, pelo disjuntor Q1 e pelo inversor VFD1. O DPS1 é
ligado a jusante de Q0 e ao barramento PE. A saída PWM U/V/W de VFD1 chega ao motor M1
por W02, cabo próprio para inversor, blindado e com condutor de proteção.

Não há contator de manobra entre VFD1 e M1. A interrupção não programada da saída do
inversor durante a operação pode produzir sobretensões ou falhas; qualquer dispositivo
de isolamento no lado do motor deve ter intertravamento e procedimento específico.

O ajuste de proteção térmica eletrônica do inversor adota 15,5 A, valor nominal
assumido para M1. Q1 protege o alimentador e o equipamento contra curto-circuito dentro
das premissas declaradas; não substitui a proteção de sobrecarga parametrizada no VFD.

## 4. Alimentação de comando

Q2 protege a fonte PS1, de entrada compatível com 380-480 Vca e saída 24 Vcc/2,5 A.
O comando em tensão extra baixa reduz a exposição nos dispositivos de porta e de campo.
Os circuitos digitais e analógicos são segregados fisicamente dos cabos de potência.

## 5. Comando e modos de operação

S3 seleciona LOCAL, posição central 0 ou REMOTO. Em LOCAL, S1 e S2 enviam comandos RUN e
STOP separados, e P1 fornece a referência de velocidade de 0-10 V. Em REMOTO, contatos
do PLC em X3:7 e X3:8 enviam RUN e STOP separados; X3:9 solicita reset de falha do VFD,
enquanto W06 fornece a referência de 4-20 mA. Os contatos e a parametrização do VFD
precisam ser compatibilizados com o modelo selecionado; o desenho não fixa terminais.

S4 (LOCAL) e X3:9 (REMOTO) solicitam somente o reset de falha de VFD1. S5 é o botão
dedicado de rearme manual monitorado do KSR1 e não comanda o VFD. O rearme de segurança,
a troca de modo e o retorno de energia exigem novo comando de partida. Os sinalizadores
H1 a H4 indicam painel energizado, VFD pronto, motor em marcha e falha.

## 6. Emergência e STO

S0 possui dois contatos normalmente fechados monitorados por KSR1. S5 solicita o rearme
manual monitorado depois da liberação de S0; esta função é separada do reset de falha do
VFD, feito por S4 ou X3:9. As duas saídas de KSR1 alimentam STO-A e STO-B de VFD1. A
atuação remove a capacidade de produzir torque, mas não garante parada instantânea: o
conjunto pode parar por inércia. O rearme de S5 não comanda nova partida.

Esta representação não declara categoria, PL ou SIL. A arquitetura real depende de
análise de risco, tempo de parada, diagnóstico, dados certificados do inversor e relé,
distâncias de segurança e validação documentada.

## 7. Aterramento e compatibilidade eletromagnética

O barramento PE recebe o condutor de proteção de W01, carcaça do painel, VFD1, motor M1,
PS1, DPS1 e abraçadeiras de blindagem. W02 usa terminação de blindagem em 360 graus nas
duas extremidades. W03 e W06 têm blindagem aterrada conforme o estudo de EMC da
instalação; o desenho adota terminação no painel e exige confirmação para evitar laços.

## 8. Construção e arranjo

O invólucro de referência mede 800 x 600 x 300 mm, grau IP54, com placa de montagem,
trilhos DIN, canaletas, ventilação filtrada e folga vertical mínima conceitual de 100 mm
ao redor do VFD. Potência e controle ocupam regiões segregadas. X1/X2 ficam separados
de X3; a barra PE e as terminações de blindagem ficam próximas às entradas de cabos.

As dimensões finais dependem das perdas reais, temperatura ambiente, altitude, método
de instalação, raios de curvatura, bornes selecionados e recomendações do fabricante.

## 9. Interfaces documentais

As referências Q0, Q1, Q2, DPS1, PS1, VFD1, KSR1, S0-S5, P1, H1-H4, X1-X3, M1 e
W01-W06 são mantidas nas oito pranchas, nas listas de materiais e de cabos e nas matrizes
de coordenação. Os DXFs são as fontes principais; PDF, SVG e PNG servem à revisão visual.

## 10. Proteção e dados para coordenação

A prancha 07 rastreia sete grupos de premissas: corrente de curto-circuito presumida,
seccionamento Q0, disjuntor Q1, proteção do VFD e do motor, circuito auxiliar Q2/PS1,
DPS1 e cabos W01/W02. O CSV vinculado lista, para cada grupo, o dado que deve substituir
a hipótese atual e a verificação ainda aberta.

A divisão de 10 kA de Icu pela hipótese de 5 kA de Icc resulta em 2:1 apenas como
operação aritmética. Sem o valor real de curto-circuito no ponto, tensão e ratings
específicos do dispositivo, curvas e tabelas de coordenação do fabricante, essa razão
não demonstra capacidade de interrupção, seletividade, retaguarda ou energia passante.
Q0 é representado como seccionador; a sobrecarga do motor depende do ajuste do VFD e
da placa real. Nenhum desses itens foi dimensionado para execução.

## 11. Plano de verificação e evidências

A prancha 08 organiza os documentos, dados de campo/OEM, cálculos, verificações
funcionais e registros necessários para encerrar cada etapa. A matriz vinculada
`plano-verificacao.csv` mantém todos os treze pontos no estado `NÃO EXECUTADO`; isso
significa que este estudo não contém ensaios nem aceite de uma instalação real.

Os critérios de aceitação, tolerâncias e instrumentos devem ser definidos a partir dos
equipamentos e requisitos efetivamente selecionados. O plano não é procedimento de
trabalho energizado, não autoriza comissionamento e não declara desempenho funcional,
coordenação, categoria de segurança, PL ou SIL.
