# Memorial descritivo - Projeto 05

## 1. Identificação e finalidade

Autor: Rogério Eduardo Moreira Menegueli

Revisão: 02, emitida em 2026-11-05

O conjunto documenta, para fins acadêmicos, uma instalação elétrica de baixa tensão de
uma oficina metalmecânica fictícia. Ele demonstra a passagem do levantamento de
cargas para a implantação, a distribuição de força e iluminação, as rotas, o diagrama
unifilar, o quadro de cargas e detalhes típicos.

## 2. Edificação fictícia

O galpão mede `30,00 m x 18,00 m`, totalizando `540,00 m²`. A faixa principal de
produção ocupa `24,00 m x 18,00 m` (`432,00 m²`). A faixa de apoio ocupa
`6,00 m x 18,00 m` (`108,00 m²`) e foi dividida conceitualmente em escritório,
manutenção e serviços. O pé-direito de `6,00 m` é apenas uma premissa para estudo.

Não há levantamento cadastral, arquitetônico, estrutural, de incêndio, ergonomia,
classificação de áreas, agressividade ambiental ou acesso real.

## 3. Sistema elétrico adotado

A origem fictícia fornece `380/220 V`, `60 Hz`, `3F+N+PE`. Adota-se TN-S a jusante
do ponto de entrega, com neutro e condutor de proteção separados. O alimentador geral
AL-QGBT chega ao QGBT-05. O quadro distribui energia para:

- QDF-05: motores, tomada de solda e tomadas industriais, circuitos C01 a C08;
- QDL-05: iluminação interna e externa, circuitos C09 a C13;
- QADM-05: tomadas de escritório, manutenção e serviços, circuitos C14 a C16.

O QGBT-05 inclui, de forma conceitual, proteção geral 4P de 100 A, DPS tipo 2 e barras
separadas de N e PE. A corrente de curto-circuito foi presumida em 6 kA apenas para
estabelecer a condição a verificar; o Icu mínimo de 10 kA atribuído ao DJ-G também é
uma premissa, sem cálculo de curto-circuito ou confirmação da concessionária. A folha
08 e a matriz de seis pares registram as comparações que continuam pendentes; não
demonstram capacidade de interrupção, retaguarda ou seletividade.

## 4. Cargas de força

As cargas trifásicas fictícias são M-501 (compressor de 11 kW), M-502 (torno de
7,5 kW), M-503 (fresadora de 5,5 kW), M-504 (exaustor de 3 kW), M-505 (esmeril de
2,2 kW), TUE-501 (solda de 12 kVA) e dois grupos de três tomadas industriais IEC 60309
de 16 A. Rendimentos, fatores de potência e demanda estão individualizados em
[quadro-cargas.csv](quadro-cargas.csv).

O projeto representa apenas a distribuição. Métodos de partida, proteção térmica,
proteção contra falta de fase, comando e segurança de cada máquina devem ser definidos
com os dados dos fabricantes e com análise de risco.

## 5. Iluminação e tomadas auxiliares

O galpão possui 24 luminárias LED fictícias de 100 W, divididas igualmente entre C09,
C10 e C11 e distribuídas nas fases A, B e C. O apoio possui 12 luminárias de 40 W em
C12 e a área externa, seis projetores de 50 W em C13. Fotometria, iluminância,
uniformidade, ofuscamento, iluminação de emergência e acionamentos automáticos não
foram calculados.

QADM-05 alimenta três circuitos monofásicos de 1,5 kVA, um por fase. A proteção
diferencial residual de 30 mA para tomadas é premissa conservadora sujeita à seleção
final conforme uso, esquema de aterramento e compatibilidade das cargas.

## 6. Encaminhamento

E-501 é a rota principal de força, nominalmente 300 x 100 mm. E-502 atende iluminação
e E-503 atende a faixa de apoio, ambas nominalmente 100 x 50 mm. As rotas e descidas
são identificadas em [lista-cabos.csv](lista-cabos.csv). A ocupação máxima inicial de
40%, os suportes a cada 2 m e a segregação são critérios de estudo, não detalhes de
montagem.

Devem ser confirmados: ocupação real, agrupamento, ventilação, esforços, raio de
curvatura, compatibilidade eletromagnética, selagem, transições, proteção mecânica,
resistência à corrosão e continuidade elétrica.

## 7. Proteção, aterramento e inspeção

Todas as massas e eletrocalhas devem ser ligadas ao PE e ao BEP-05. O projeto executivo
deve verificar seção e continuidade do PE, equipotencialização, impedância do laço,
tempos de seccionamento, resistência de aterramento, coordenação de DPS e ensaios.

O acesso aos quadros, graus IP, identificação, bloqueio e desenergização devem ser
compatíveis com o ambiente e com a NR-10 vigente na data do trabalho. Em setembro de
2026, a revisão publicada em 2026 ainda possui vigência futura em 2027; uma aplicação
real deve confirmar o texto efetivamente vigente.

## 8. Rastreabilidade

As tags C01-C16, QGBT-05, QDF-05, QDL-05, QADM-05, M-501-M-505, TUE-501,
TI-501-TI-506 e AL-QGBT/AL-QDF/AL-QDL/AL-QADM são comuns aos desenhos, CSVs,
memória de cálculo e workbook. O validador específico recalcula as grandezas e rejeita
divergências entre essas fontes. A matriz P05-08 rastreia os seis pares de proteção
montante-jusante. A prancha P05-09 e `dados-estudo-coordenacao.csv` organizam os dados
e evidências necessários ao futuro cálculo; nenhum dado de concessionária ou curva de
dispositivo foi recebido e os doze grupos continuam `PENDENTE`.

## 9. Limitação de responsabilidade

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
