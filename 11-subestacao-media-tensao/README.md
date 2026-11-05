# Projeto 11 - Subestação de Média Tensão 13,8 kV com SPDA e Aterramento

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 06

Formato: A3 paisagem, unidades em milímetros, revisão gráfica 01 (2026-11-05)

Estado: revisão conceitual 01 em 2026-11-05; segurança e conformidade normativa não validadas

Este estudo acadêmico apresenta uma proposta conceitual de **Subestação Transformadora Abrigada de Média Tensão (13,8 kV / 380-220 V - 500 kVA)** e cita as ABNT NBR 14039, NBR 5410, NBR 15751 e NBR 5419 como referências de estudo. Não declara conformidade normativa, segurança de aterramento, aprovação de concessionária ou aptidão executiva. A malha de terra ainda não possui cálculo de tensões de toque/passo nem avaliação de elevação de potencial.

## Entregáveis

- `fonte/`: seis desenhos DXF R2013 e scripts reproduzíveis;
- `exports/`: versões PDF vetorial, SVG e PNG (300 dpi) derivadas dos DXFs;
- `memorial-descritivo.md`: memorial conceitual; premissas e componentes não selecionados precisam de validação;
- `criterios-premissas.md`: premissas técnicas, distâncias de segurança e limites normativos;
- `memoria-calculo.md`: cálculos de correntes nominais, curto-circuito, ajustes de relé, malha de terra e SPDA;
- `referencias-normativas.md`: normas técnicas e notas regulatórias;
- `lista-cabos.csv` e `lista-materiais.csv`: listas preliminares, sem especificação executiva ou seleção de fornecedores;
- `fonte/gerar_projeto_11.py`: gerador determinístico das pranchas em DXF;
- `fonte/validar_projeto_11.py`: script de validação de consistência técnica;
- `inspecao-visual.md`: relatório de conformidade visual das pranchas renderizadas.

## Pranchas

1. [Diagrama unifilar geral](fonte/01_diagrama_unifilar_geral.dxf): ramal 13,8 kV, muflas, cubículo de medição, cubículo de proteção primária com disjuntor a vácuo 17,5 kV e relé 50/51/50N/51N, transformador a óleo 500 kVA e QGBT 800 A.
2. [Planta baixa da subestação](fonte/02_planta_baixa_subestacao.dxf): arranjo físico em alvenaria 6,00 x 4,00 m, portas corta-fogo P-90, canaletas de cabos, tapete isolante 20 kV, ventilação cruzada e bacia de contenção com brita nº 1 e dreno sifonado.
3. [Cortes e detalhes eletromecânicos](fonte/03_cortes_detalhes_eletromecanicos.dxf): elevações A-A e B-B, barramentos de MT em barra chata Cu 25x5 mm sobre isoladores epóxi 17,5 kV, bacia de contenção e barramento flexível BT.
4. [Diagrama funcional de proteção e comando](fonte/04_diagrama_funcional_protecao.dxf): esquema de medição AC (TCs de proteção), circuito auxiliar 125 Vcc com retificador/banco de baterias, lógica de trip na bobina de abertura (BA) com contato auxiliar 52a e intertravamentos de segurança (Buchholz 63 e termômetro 49).
5. [Malha de aterramento e equipotencialização](fonte/05_malha_aterramento.dxf): malha conceitual em cabo Cu nu 70 mm² a 0,60 m, 8 hastes 5/8" x 2,40 m e BEP. A estimativa simplificada de 18,72 Ω não valida segurança nem atendimento normativo; tensões de toque/passo e potencial da malha não foram calculados.
6. [Arranjo conceitual de SPDA](fonte/06_spda_geral.dxf): retícula, captores e descidas esquemáticos; classe de proteção, geometria final e coordenação de DPS não foram verificados.

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
| Estimativa geométrica simplificada da malha | 18,72 Ω; preliminar, sem aprovação de segurança |
| Classe e dimensionamento do SPDA | Não verificados; valores do desenho são premissas conceituais |

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
