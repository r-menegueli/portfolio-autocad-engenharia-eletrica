# Memorial Descritivo: Sistema de Grupo Moto-Gerador e QTA (250 kVA)

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

---

## 1. Objetivo

Este memorial descritivo estabelece as premissas funcionais, características elétricas, eletromecânicas e de controle para o sistema de emergência composto por um **Grupo Moto-Gerador (GMG) Diesel de 250 kVA / 200 kW**, operando em **380/220 V**, e seu respectivo **Quadro de Transferência Automática (QTA)** com comutação em transição aberta e comando microprocessado por **Unidade de Supervisão de Corrente Alternada (USCA)**.

---

## 2. Descrição Geral do Sistema

### 2.1 Grupo Moto-Gerador (GMG)
* **Motor Diesel:** 6 cilindros em linha, 4 tempos, injeção direta eletrônica, turboalimentado e pós-arrefecido (*aftercooler*), com regulador eletrônico de rotação classe G2/G3 (NBR ISO 8528-5). Velocidade síncrona de 1800 rpm.
* **Alternador:** Trifásico, síncrono, sem escovas (*brushless*), 4 polos, isolamento classe H com elevação de temperatura classe F, enrolamento de passo 2/3 para atenuação de 3ª harmônica e múltiplos. Equipado com excitatriz auxiliar PMG (*Permanent Magnet Generator*) e regulador automático de tensão (AVR) com regulação estática $\le \pm 0,5\%$.
* **Base e Cabine:** Base metálica em perfil U laminado com amortecedores elastoméricos integrados. Cabine insonorizada em chapa de aço galvanizado com pintura eletrostática a pó, atenuadores acústicos do tipo células paralelas em lã de rocha e atenuação para $75\text{ dB(A)}$ a 1,5 metro de distância.
* **Sistema de Combustível:** Tanque de consumo diário em polietileno/metálico de 250 litros, instalado na base do grupo, provido de bacia de contenção para 110% do volume, visor mecânico de nível, transmissor eletrônico de nível e boia de corte por nível baixo.

### 2.2 Quadro de Transferência Automática (QTA)
* **Invólucro:** Painel autoportante em chapa de aço carbono 14 MSG (espessura 1,9 mm), grau de proteção IP54 para montagem abrigada, dimensões de $1800 \times 800 \times 400\text{ mm}$ (A x L x P).
* **Elementos de Potência:** Dois contatores tetrapolares de potência eletromecânicos (K1 para Rede e K2 para Gerador), comutando 3 fases e neutro, categoria de emprego AC-1/AC-3, corrente nominal proposta de 400 A, dotados de **intertravamento físico e lógico conceituais**:
  1. **Intertravamento Mecânico:** Tirante/barra rígida montada entre os chassis de K1 e K2 que impede fisicamente a manobra simultânea dos dois mecanismos.
  2. **Intertravamento Elétrico:** Contatos auxiliares normalmente fechados (NF) cruzados nas bobinas de comando de K1 e K2, além do gerenciamento lógico independente executado pelo software da USCA.
* **Barramentos:** Em cobre eletrolítico eletroestanhado $40 \times 5\text{ mm}$ com capacidade para $500\text{ A}$ contínuos, fixados sobre isoladores de epóxi tipo castanha 1 kV.

### 2.3 Unidade de Supervisão de Corrente Alternada (USCA)
* **Controlador Microprocessado:** Módulo digital para grupos geradores com IHM gráfica LCD monocromática, monitoramento contínuo das grandezas elétricas da rede (tensão trifásica, frequência) e do gerador (tensão, corrente trifásica, potência ativa, reativa, fator de potência, rotação, horímetro).
* **Parâmetros de Detecção e Lógica de Operação:**
  * **Subtensão de Rede:** Atuação se $V < 0,85 \times V_n$ (ajustável).
  * **Sobretensão de Rede:** Atuação se $V > 1,10 \times V_n$.
  * **Assimetria de Fase e Falha de Sequência:** Detecção imediata de falta de fase.
  * **Temporizador de Confirmação de Falha:** 3 segundos.
  * **Pulso de Partida:** Até 3 tentativas de arranque de 5 s, com repouso de 5 s entre tentativas.
  * **Estabilização de Tensão e Frequência do GMG:** Verificação em 5 segundos antes da transferência.
  * **Tempo Morto de Transição (*Dead Time*):** 1,5 segundo entre a abertura de K1 e o fechamento de K2 para extinção de arco elétrico e desaceleração de cargas motrizes.
  * **Retorno da Rede:** Temporizador de estabilização de rede proposto em 120 s.
  * **Arrefecimento do Motor (*Cool-down*):** 180 segundos operando em vazio antes da parada total.

Os tempos são setpoints conceituais para demonstrar a sequência, sujeitos às recomendações do fabricante do motor e da USCA. Eles não estabelecem um tempo total garantido para assumir a carga.

### 2.4 Cadastro de cargas essenciais

A revisão 03 organiza em cadastro-cargas-qce.csv e na prancha 09 os quatro
alimentadores de cargas essenciais identificados na lista de cabos: iluminação e
rotas de fuga, bomba de incêndio, UPS da sala de servidores e utilidades. Potências,
correntes, partidas, simultaneidade e prioridade de entrada ainda não foram
informadas. A lista atual não comprova que todos os ramais do QCE foram identificados
e não permite verificar a capacidade do GMG para a demanda real.

---

## 3. Dispositivos de Proteção

1. **Disjuntor Geral da Rede (DJ-REDE):** Caixa moldada 400 A, disparador termomagnético ajustável, capacidade de interrupção $I_{cu} = 25\text{ kA}$ em 380 V.
2. **Disjuntor Geral do Gerador (DJ-GER):** Caixa moldada 400 A com disparador eletrônico LSI, capacidade de interrupção $I_{cu} = 16\text{ kA}$ em 380 V.
3. **Dispositivo de Proteção contra Surtos (DPS):** Classe II, $I_n = 20\text{ kA}$, $I_{max} = 45\text{ kA}$, $U_c = 275\text{ V}$, monopolares instalados entre fases-terra e neutro-terra na saída para o quadro de cargas essenciais.
4. **Proteções do Motor Diesel:**
   - Parada por baixa pressão de óleo lubrificante ($< 1,2\text{ bar}$).
   - Parada por alta temperatura de arrefecimento ($> 103^\circ\text{C}$).
   - Parada por sobrevelocidade ($> 115\%\text{ rpm}$).
   - Alarme de nível baixo de diesel no reservatório.
   - Parada de emergência imediata via botão com trava tipo cogumelo.
