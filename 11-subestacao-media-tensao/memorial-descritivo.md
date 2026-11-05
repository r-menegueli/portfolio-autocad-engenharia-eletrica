# Memorial descritivo - Projeto 11

## 1. Identificação e finalidade

Autor: Rogério Eduardo Moreira Menegueli

Revisão do conteúdo: conceitual; conferir todas as premissas antes de qualquer uso técnico.

Este projeto documenta, para fins acadêmicos e de portfólio técnico, uma **Subestação Transformadora Abrigada de Média Tensão (13,8 kV / 380-220 V - 500 kVA)**, contemplando o diagrama unifilar geral, arranjo físico em alvenaria, cortes eletromecânicos, diagrama funcional de proteção secundária (ANSI 50/51/50N/51N), malha de aterramento subterrânea e Sistema de Proteção contra Descargas Atmosféricas (SPDA).

## 2. Entrada de energia e medição

O fornecimento ocorre em tensão primária de distribuição de `13,8 kV` (`60 Hz`), trifásico, derivado da rede aérea da concessionária através de ramal de entrada subterrâneo em cabos de cobre isolados em EPR `8,7/15 kV` de seção `3x(1x50 mm²)`, dotados de blindagem metálica aterrada em ambas as extremidades e muflas terminais termocontráteis.

O desenho reserva a função de para-raios poliméricos de óxido de zinco no ponto de entrega; tensão nominal, MCOV, corrente, nível de proteção e coordenação de isolamento precisam ser definidos a partir dos dados da rede e dos equipamentos. O **Cubículo 01** ilustra uma chave seccionadora de `17,5 kV / 630 A` e os TCs/TPs de medição como premissas, ainda sem aprovação da concessionária ou seleção por fabricante.

## 3. Proteção primária e transformação

O **Cubículo 02** contém o disjuntor tripolar a vácuo (`17,5 kV / 630 A / 16 kA`), equipado com bobina de abertura (*shunt trip*) alimentada em `125 Vcc` por fonte retificadora e banco de baterias seladas VRLA. A detecção de faltas é realizada por três TCs de proteção classe `10B200` (`50-100/5 A`) conectados ao relé digital microprocessado com funções `50/51` (sobrecorrente instantânea e temporizada de fase) e `50N/51N` (sobrecorrente de neutro/terra).

O **Cubículo 03** aloja o transformador de força trifásico imerso em óleo mineral isolante, potência nominal de `500 kVA`, relação `13.800 / 380-220 V`, grupo de ligação `Dyn1` e impedância percentual $Z\% = 4,50\%$. O equipamento dispõe de supervisão intrínseca por relé detector de gás *Buchholz* (ANSI 63) e termômetro de óleo com dois estágios de contato (alarme em $85^\circ\text{C}$ e desligamento/trip em $100^\circ\text{C}$). Sob o transformador encontra-se a bacia de contenção com volume útil de $1,20\text{ m}^3$, grelha metálica revestida com camada de brita nº 1 abafa-chamas e dreno sifonado interligado à caixa separadora de água e óleo.

## 4. Quadro Geral de Baixa Tensão (QGBT)

A interligação entre os terminais secundários do transformador e o **QGBT** é representada por condutores de cobre flexível `3x[2x(1x240 mm²)] + N + PE` em canaleta técnica. As seções e o arranjo são premissas conceituais, sem verificação de ampacidade, queda de tensão, agrupamento, curto-circuito ou instalação real. O desenho propõe um disjuntor geral de `800 A`, capacidade nominal declarada de `50 kA` em `380 V`, e barramento de `1000 A`; os equipamentos não foram selecionados por fabricante nem validados. O DPS consta apenas como função a especificar: classe, tensão máxima contínua, nível de proteção, correntes nominais e coordenação permanecem em aberto. Os alimentadores para P05 e P06 são referências conceituais, sem coordenação confirmada.

## 5. Malha de aterramento e SPDA

A prancha mostra, como arranjo conceitual ainda não dimensionado, cabo de cobre nu de `70 mm²` a `0,60 m` de profundidade e `8 hastes` de `5/8" x 2,40 m`. Materiais, seção, espaçamento, conexões e equipotencialização não foram verificados para o local. Não há levantamento de resistividade, dados reais de falta, tempos de eliminação, cálculo de elevação de potencial nem verificação de tensões de toque e passo; a estimativa aritmética de `18,72 Ω` não valida segurança. A topologia mostra a intenção de interligar massas, blindagens e neutro ao **Barramento de Equipotencialização Principal (BEP)**, sem projeto de aterramento final.

O **SPDA** ilustra uma disposição conceitual com anel de cobertura, captores terminais e quatro descidas. O nível de proteção, o método, as distâncias, a equipotencialização e a necessidade de proteção não foram determinados por análise de risco nem validados para uma edificação real.

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
