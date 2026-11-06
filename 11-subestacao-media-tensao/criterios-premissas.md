# Critérios e premissas - Projeto 11

## Dados declarados

| Item | Valor adotado | Natureza |
| --- | ---: | --- |
| Tensão primária (concessionária) | 13,8 kV (3F - 60 Hz) | premissa |
| Tensão secundária (baixa tensão) | 380 / 220 V (3F+N+PE) | premissa |
| Potência nominal do transformador | 500 kVA | premissa |
| Tipo construtivo do transformador | Imerso em óleo mineral | hipótese |
| Impedância percentual ($Z\%$) | 4,50% | hipótese; confirmar em placa/datasheet |
| Grupo de ligação | Dyn1 | premissa |
| Nível Básico de Impulso (NBI - classe 15 kV) | 95 kV | valor de estudo; confirmar coordenação de isolamento |
| Corrente nominal primária ($I_{n1}$) | 20,92 A | calculada |
| Corrente nominal secundária ($I_{n2}$) | 759,67 A | calculada |
| Corrente de curto-circuito no secundário ($I_{cc2}$) | 16,88 kA | calculada |
| Dimensões externas da alvenaria | 6,00 x 4,00 m (24,00 m²) | premissa sem validação arquitetônica/civil |
| Pé-direito interno útil | 3,50 m | premissa civil |
| Resistividade aparente do solo ($\rho$) | não definida | depende de levantamento e interpretação do local |
| Resistividade da camada superficial ($\rho_s$) | não definida | depende de material, espessura e evidência de campo |
| Geometria/classificação do SPDA | retícula e captores esquemáticos | sem análise de risco ou verificação normativa |

## Escala e geometria da P11-02

- As cotas externas de 6,00 x 4,00 m são premissas do estudo, sem levantamento arquitetônico ou civil.
- A geometria interna representada não corresponde proporcionalmente às cotas; por isso a prancha declara `S/ESC.` e as cotas escritas prevalecem.
- Localização de portas, cubículos, transformador, canaletas, tapete, ventilação e bacia permanece esquemática; dimensões dos equipamentos dependem dos desenhos do fabricante.
- O corredor frontal de 1,20 m e os demais valores são critérios de estudo. A planta não demonstra que os afastamentos, a ventilação, a retirada dos equipamentos ou a NBR 14039 estejam atendidos.
- Para substituir o esquema por implantação real são necessários levantamento, seleção OEM, rotas de entrada/retirada e revisão técnica do arranjo.

## Critérios eletromecânicos e de segurança

1. **Compartimentação e Acesso:**
   - Separação física entre os cubículos de medição, proteção primária, transformação e quadro geral de baixa tensão (QGBT).
   - Portas metálicas corta-fogo P-90 com abertura para o exterior e barra antipânico.
   - Intertravamento mecânico tipo chave *Kirk* entre a chave seccionadora e a tela de proteção do transformador.

2. **Bacia de Contenção de Óleo:**
   - Dimensionada para comportar mais de 100% do volume de óleo isolante do transformador (850 litros), com volume útil de $1,20\text{ m}^3$, grelha metálica com camada de brita nº 1 abafa-chamas e dreno sifonado para caixa separadora.

3. **Proteção Primária (ANSI 50/51 e 50N/51N):**
   - Disjuntor a vácuo 17,5 kV / 630 A / 16 kA comandado por relé digital microprocessado alimentado em 125 Vcc por fonte/bateria auxiliar.
   - Atuação instantânea e temporizada para faltas entre fases e fase-terra, além de trip direto por atuação do relé Buchholz (gás) e sobretemperatura do óleo ($100^\circ\text{C}$).

4. **Aterramento e SPDA:**
   - A prancha apresenta uma malha conceitual em cobre nu $70\text{ mm}^2$, a $0,60\text{ m}$, com 8 hastes de $5/8" \times 2,40\text{ m}$. Materiais e geometria ainda não foram dimensionados para um local real.
   - A topologia conceitual prevê um Barramento de Equipotencialização Principal (BEP); conexões e coordenação com o SPDA precisam de projeto e verificação.
   - A revisão 02 remove da prancha 05 a estimativa aritmética sem dados medidos. Resistividade por profundidade, contribuição e tempo de falta, geometria real, GPR, tensões de toque/passo e potenciais transferidos continuam pendentes e foram rastreados em `dados-estudo-aterramento.csv`.
   - A prancha 07 organiza evidências de entrada e entregáveis; nenhum valor é presumido e nenhum status de segurança/aprovação é atribuído.
   - A prancha 08 relaciona o modelo de solo, os cenários de falta e a geometria às verificações de condutor/conexões, resposta da malha, exposição e potenciais transferidos. Ela registra resultados requeridos e evidências, sem substituir método de cálculo, definir limites numéricos ou atribuir aprovação; os resultados permanecem pendentes.

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
