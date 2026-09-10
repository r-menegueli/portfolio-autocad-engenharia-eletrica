# Memorial descritivo

## Finalidade

Documentar uma fonte de bancada ajustável de 0-30 Vcc e 0-5 A, com limite de 150 W,
como exercício de integração elétrica e mecânica. O conjunto é uma arquitetura
funcional acadêmica, não um produto desenvolvido, certificado ou liberado para
fabricação.

## Cadeia de energia

A entrada X1 recebe L, N e PE por conector IEC de painel. O PE segue diretamente ao
ponto de aterramento do chassi e às carcaças metálicas. A fase passa por F1; S1 abre L
e N. MOV1 e FL1 representam proteção contra surtos e filtragem conduzida, sujeitos a
coordenação e ensaios.

PS1 fornece isolamento funcional proposto e barramento de 36 Vcc. F2 protege
preliminarmente esse barramento. REG1 reduz a tensão e regula os modos CV e CC. K1
habilita ou remove a saída positiva; SH1 mede corrente no retorno. X2 oferece bornes
positivo e negativo flutuantes, e X3 oferece conexão separada ao chassi/PE.

## Controle e medição

RV1 ajusta tensão e RV2 ajusta o limite de corrente. S2 solicita habilitação de saída,
com LED branco para estado ligado. Os LEDs verde e âmbar indicam CV e CC. M1 apresenta
tensão e corrente a partir de linhas Kelvin e do shunt, mas classe de exatidão,
resolução, atualização e calibração permanecem pendentes.

TS1 integra a cadeia de habilitação e abre por sobretemperatura proposta de 75 °C.
TH1 aciona o ventilador a 40 °C. Nenhuma dessas funções foi analisada quanto a falha
única, histerese, contato soldado, cobertura térmica ou confiabilidade.

## Organização eletromecânica

O gabinete de referência mede 320 × 150 × 260 mm. A zona primária fica próxima à
entrada traseira e sob cobertura própria; o ponto PE fica adjacente à entrada. PS1 e
REG1 ocupam o fluxo principal de ar. Cabos de rede, potência CC, sinais Kelvin e
controle seguem rotas segregadas. Conectores frontais possuem alívio mecânico e
identificação persistente a especificar.

O painel frontal contém chave geral, display, ajustes de tensão e corrente, comando
de saída, indicação CV/CC e três bornes. A prancha mecânica fornece somente cotas de
interface; tolerâncias, acabamento e processo de fabricação não estão definidos.

## Proteções e riscos remanescentes

F1, S1, FL1, MOV1, F2, TS1 e a limitação eletrônica são propostas funcionais. A
capacidade de interrupção, seletividade, energia passante, descargas dos capacitores,
isolação, corrente de toque, continuidade do PE, acesso a partes vivas, temperatura e
propagação de chama exigem projeto detalhado e ensaios.

A saída nominal é inferior a 30 Vcc, mas isso não autoriza classificar o equipamento
como SELV, PELV, fonte limitada ou produto seguro sem a avaliação completa do estágio
isolado, do invólucro e das condições de falha.

## Responsabilidade

Nenhum tag corresponde a produto comercial escolhido. Dimensões, valores, símbolos e
cálculos servem ao portfólio acadêmico. Não há declaração de conformidade com IEC,
ABNT, Inmetro, NR-10 ou qualquer regime de certificação.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
