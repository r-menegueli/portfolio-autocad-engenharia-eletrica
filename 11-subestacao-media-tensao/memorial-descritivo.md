# Memorial descritivo - Projeto 11

## 1. Identificação e finalidade

Autor: Rogério Eduardo Moreira Menegueli

Revisão: 00, emitida em 2026-09-25

Este projeto documenta, para fins acadêmicos e de portfólio técnico, uma **Subestação Transformadora Abrigada de Média Tensão (13,8 kV / 380-220 V - 500 kVA)**, contemplando o diagrama unifilar geral, arranjo físico em alvenaria, cortes eletromecânicos, diagrama funcional de proteção secundária (ANSI 50/51/50N/51N), malha de aterramento subterrânea e Sistema de Proteção contra Descargas Atmosféricas (SPDA).

## 2. Entrada de energia e medição

O fornecimento ocorre em tensão primária de distribuição de `13,8 kV` (`60 Hz`), trifásico, derivado da rede aérea da concessionária através de ramal de entrada subterrâneo em cabos de cobre isolados em EPR `8,7/15 kV` de seção `3x(1x50 mm²)`, dotados de blindagem metálica aterrada em ambas as extremidades e muflas terminais termocontráteis.

No ponto de entrega situam-se os para-raios poliméricos de óxido de zinco (`12 kV / 10 kA`). O **Cubículo 01** abriga a chave seccionadora tripolar de manobra sob carga (`17,5 kV / 630 A`) com lâmina de aterramento rápido intertravada, além dos Transformadores de Corrente (`TC-MED`) e Transformadores de Potencial (`TP-MED`) exclusivos para medição de faturamento da concessionária.

## 3. Proteção primária e transformação

O **Cubículo 02** contém o disjuntor tripolar a vácuo (`17,5 kV / 630 A / 16 kA`), equipado com bobina de abertura (*shunt trip*) alimentada em `125 Vcc` por fonte retificadora e banco de baterias seladas VRLA. A detecção de faltas é realizada por três TCs de proteção classe `10B200` (`50-100/5 A`) conectados ao relé digital microprocessado com funções `50/51` (sobrecorrente instantânea e temporizada de fase) e `50N/51N` (sobrecorrente de neutro/terra).

O **Cubículo 03** aloja o transformador de força trifásico imerso em óleo mineral isolante, potência nominal de `500 kVA`, relação `13.800 / 380-220 V`, grupo de ligação `Dyn1` e impedância percentual $Z\% = 4,50\%$. O equipamento dispõe de supervisão intrínseca por relé detector de gás *Buchholz* (ANSI 63) e termômetro de óleo com dois estágios de contato (alarme em $85^\circ\text{C}$ e desligamento/trip em $100^\circ\text{C}$). Sob o transformador encontra-se a bacia de contenção com volume útil de $1,20\text{ m}^3$, grelha metálica revestida com camada de brita nº 1 abafa-chamas e dreno sifonado interligado à caixa separadora de água e óleo.

## 4. Quadro Geral de Baixa Tensão (QGBT)

A interligação entre os terminais secundários do transformador e o **QGBT** é efetuada por condutores de cobre flexível `3x[2x(1x240 mm²)] + N + PE` alojados em canaleta técnica. O QGBT possui disjuntor geral em caixa aberta de `800 A` ($I_{cu} = 50\text{ kA}$ em `380 V`), proteção contra surtos **DPS Classe I+II** (`12,5 kA` / `40 kA`) e barramento de cobre eletrolítico de `1000 A`, alimentando os quadros setoriais da indústria (integrando-se diretamente aos projetos P05 - Instalação Industrial e P06 - Centro de Controle de Motores).

## 5. Malha de aterramento e SPDA

A malha de aterramento da subestação é constituída por cabo de cobre nu recozido de `70 mm²` enterrado a `0,60 m` de profundidade em anel perimetral externo e reticulado interno sob o piso, interligado a `8 hastes` de aço cobreado (*copperweld*) de `5/8" x 2,40 m` por conexões de solda exotérmica. Todas as massas metálicas, telas de proteção, portas corta-fogo, blindagens de cabos de MT e o neutro do secundário do transformador são conectados ao **Barramento de Equipotencialização Principal (BEP)**.

O **SPDA** adota o Método das Malhas (Gaiola de Faraday) combinado com captores terminais aéreos de `35 cm` nos vértices da cobertura, dimensionado para **Nível de Proteção II** conforme a ABNT NBR 5419:2015, contando com 4 condutores de descida em cobre nu de `35 mm²`, caixas de inspeção suspensa e proteção mecânica no trecho inferior.

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
