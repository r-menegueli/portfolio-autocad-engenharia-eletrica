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
| Resistividade aparente do solo ($\rho$) | 250 $\Omega\cdot\text{m}$ | hipótese não medida; sem uso para aprovar malha |
| Resistividade da camada superficial ($\rho_s$) | não definida | não medida; não usar para validar segurança |
| Geometria/classificação do SPDA | retícula e captores esquemáticos | sem análise de risco ou verificação normativa |

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

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
