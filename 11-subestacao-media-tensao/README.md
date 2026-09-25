# Projeto 11 - Subestação de Média Tensão 13,8 kV com SPDA e Aterramento

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 06

Formato: A3 paisagem, unidades em milímetros, revisão 00

Estado: concluído e validado em 2026-09-25

Este projeto apresenta a infraestrutura elétrica conceitual de uma **Subestação Transformadora Abrigada de Média Tensão (13,8 kV / 380-220 V - 500 kVA)**, projetada segundo as prescrições das normas ABNT NBR 14039, NBR 5410, NBR 15751 e NBR 5419:2015. O projeto estabelece a interface primária entre a rede de distribuição da concessionária e a planta fabril, alimentando o Quadro Geral de Baixa Tensão (QGBT) que supre os alimentadores de força, iluminação e o Centro de Controle de Motores (CCM).

## Entregáveis

- `fonte/`: seis desenhos DXF R2013 e scripts reproduzíveis;
- `exports/`: versões PDF vetorial, SVG e PNG (300 dpi) derivadas dos DXFs;
- `memorial-descritivo.md`: descrição detalhada do sistema primário, secundário e segurança;
- `criterios-premissas.md`: premissas técnicas, distâncias de segurança e limites normativos;
- `memoria-calculo.md`: cálculos de correntes nominais, curto-circuito, ajustes de relé, malha de terra e SPDA;
- `referencias-normativas.md`: normas técnicas e notas regulatórias;
- `lista-cabos.csv` e `lista-materiais.csv`: relação completa de componentes, equipamentos e condutores;
- `fonte/gerar_projeto_11.py`: gerador determinístico das pranchas em DXF;
- `fonte/validar_projeto_11.py`: script de validação de consistência técnica;
- `inspecao-visual.md`: relatório de conformidade visual das pranchas renderizadas.

## Pranchas

1. [Diagrama unifilar geral](fonte/01_diagrama_unifilar_geral.dxf): ramal 13,8 kV, muflas, cubículo de medição, cubículo de proteção primária com disjuntor a vácuo 17,5 kV e relé 50/51/50N/51N, transformador a óleo 500 kVA e QGBT 800 A.
2. [Planta baixa da subestação](fonte/02_planta_baixa_subestacao.dxf): arranjo físico em alvenaria 6,00 x 4,00 m, portas corta-fogo P-90, canaletas de cabos, tapete isolante 20 kV, ventilação cruzada e bacia de contenção com brita nº 1 e dreno sifonado.
3. [Cortes e detalhes eletromecânicos](fonte/03_cortes_detalhes_eletromecanicos.dxf): elevações A-A e B-B, barramentos de MT em barra chata Cu 25x5 mm sobre isoladores epóxi 17,5 kV, bacia de contenção e barramento flexível BT.
4. [Diagrama funcional de proteção e comando](fonte/04_diagrama_funcional_protecao.dxf): esquema de medição AC (TCs de proteção), circuito auxiliar 125 Vcc com retificador/banco de baterias, lógica de trip na bobina de abertura (BA) com contato auxiliar 52a e intertravamentos de segurança (Buchholz 63 e termômetro 49).
5. [Malha de aterramento e equipotencialização](fonte/05_malha_aterramento.dxf): malha externa em anel e reticulado interno em cabo Cu nu 70 mm² a 0,60 m de profundidade, 8 hastes copperweld 5/8" x 2,40 m com solda exotérmica, Barramento de Equipotencialização Principal (BEP) e memória NBR 15751 ($R_{malha} \le 3,85\ \Omega$).
6. [Sistema de Proteção contra Descargas Atmosféricas (SPDA)](fonte/06_spda_geral.dxf): método das malhas (Gaiola de Faraday 10x10 m - Nível II) com captores terminais aéreos 35 cm, 4 condutores de descida em cabo Cu 35 mm² com tubos de proteção mecânica na base, caixas de medição e DPS Classe I+II.

## Resultados principais

| Grandeza | Valor adotado / calculado |
| --- | ---: |
| Potência nominal do transformador | 500 kVA |
| Tensão primária / secundária | 13,8 kV / 380-220 V |
| Corrente nominal primária ($I_{n1}$) | 20,92 A |
| Corrente nominal secundária ($I_{n2}$) | 759,67 A |
| Impedância percentual do transformador | 4,50% |
| Corrente de curto-circuito simétrica no secundário ($I_{cc2}$) | 16,88 kA |
| Disjuntor geral de baixa tensão | Caixa aberta 3P 800 A ($I_{cu} = 50\text{ kA}$) |
| Disjuntor de média tensão | Disjuntor a vácuo 17,5 kV / 630 A / 16 kA |
| Proteção secundária | Relé digital microprocessado ANSI 50/51/50N/51N |
| Volume da bacia de contenção de óleo | 1,20 m³ (óleo total trafo = 850 L) |
| Resistência calculada da malha de aterramento | $\le 3,85\ \Omega$ (critério $R \le 5,0\ \Omega$) |
| Nível de proteção do SPDA | Nível II (ABNT NBR 5419-3:2015) |

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
