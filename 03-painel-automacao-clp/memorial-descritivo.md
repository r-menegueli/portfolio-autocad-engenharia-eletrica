# Memorial descritivo

## 1. Identificação

Projeto 03 - Painel de automação com CLP para duas bombas de reservatório.

Autor: Rogério Eduardo Moreira Menegueli. Data-base: 2026-09-06. Revisão: 00.

## 2. Finalidade e solução conceitual

O painel P03 recebe alimentação trifásica de 220 V e distribui potência para duas
bombas centrífugas M1 e M2, cada uma com seccionamento/proteção, contator e relé de
sobrecarga. A automação é alimentada por PSU1, fonte de 24 Vcc / 10 A, e executada por
CLP1 genérico com 16 entradas e 16 saídas digitais PNP.

Quatro contatos discretos representam o nível do reservatório: LSL-LL (baixo-baixo),
LSL (baixo), LSH (alto) e LSHH (alto-alto). O arranjo foi concebido para enchimento do
reservatório: a demanda inicia em LSH, encerra em LSL e é bloqueada em LSL-LL para
evitar funcionamento a seco da fonte de captação. A interpretação física final dos
sensores depende do processo real e deve ser confirmada em campo.

## 3. Potência e proteção

Q0 secciona o painel. QF1/KM1/RT1 alimentam M1 e QF2/KM2/RT2 alimentam M2. QF3 protege
o circuito de entrada da fonte. QF4 a QF7 subdividem o 24 Vcc entre CLP, sensores,
relés/contatores e sinalização. Os valores registrados são preliminares e exigem
verificação de corrente de partida, capacidade de interrupção, curto-circuito,
seletividade, queda de tensão, temperatura, método de instalação e dados de placa.

## 4. Automação e segurança

CLP1 determina alternância, demanda, temporizações, supervisão e alarmes. K1 e K2 são
relés de interface entre as saídas transistorizadas e as bobinas KM1/KM2. Diodos de
supressão devem ser instalados nas bobinas CC compatíveis.

S0 atua em dois canais sobre KSR1. Os contatos seguros de KSR1 retiram a energia das
cadeias de KM1 e KM2 sem depender do programa. O CLP apenas monitora o estado de KSR1.
O relé KDRY, associado a LSL-LL, também mantém contatos em série com ambas as bobinas;
assim, o bloqueio por nível crítico possui camada física complementar à lógica. Não se
declara categoria, PL ou SIL: isso depende de análise de risco e validação específicas.

## 5. Operação

Em automático, LSH cria a demanda e a bomba escalada como titular parte se todos os
permissivos estiverem verdadeiros. Ao atingir LSL, a demanda termina e a preferência
é transferida à outra bomba para o próximo ciclo. LSHH, falha de partida ou sobrecarga
da titular solicitam a bomba disponível de reserva. Em manual, S2/S3 comandam M1 e
S4/S5 comandam M2, mas emergência, sobrecarga e proteção contra funcionamento a seco
continuam ativos.

## 6. Interfaces e manutenção

X1 recebe alimentação, X2 atende motores, X3 concentra sensores/comandos e X4 atende
sinalização remota. Os cabos W01 a W12 mantêm identificação nas duas extremidades.
Potência, comando e instrumentação devem percorrer canaletas/rotas segregadas; PE deve
ser contínuo e ligado à placa, porta, invólucro e carcaças das bombas.

## 7. Limitações e responsabilidade

O material demonstra organização documental e lógica funcional. Não contém programa
executável de CLP, análise de risco, validação de segurança, cálculo hidráulico nem
seleção comercial definitiva.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
