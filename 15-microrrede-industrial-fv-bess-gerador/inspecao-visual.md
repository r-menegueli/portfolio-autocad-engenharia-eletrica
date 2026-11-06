# Inspeção visual e validação — P15

**Data:** 2026-11-06

**Formato:** A3 paisagem, 420 × 297 mm; PNGs de 4960 × 3507 px.

## Inspeção das pranchas

- **01 — Unifilar:** a cadeia de rede, PCC, transformador e QGBT chega ao barramento comum; FV, BESS, GE e carga são separados. O banco de baterias está distinguido do conversor. As proteções e o paralelismo permanecem pendentes. Não encontrei colisões relevantes, cortes ou conteúdo fora da moldura.
- **02 — Layout:** o campo FV, BESS, GE, QGBT e grupos de carga estão separados. As potências hipotéticas são repetidas no cadastro lateral e o desenho se identifica como sem escala. Não encontrei colisões relevantes ou textos cortados.
- **03 — Operação e balanço:** cinco cenários mostram explicitamente as parcelas de FV, GE, BESS e rede. Os totais conferem com as premissas; a indisponibilidade do GE mantém 800 kW prioritários e corta 200 kW não prioritários. Modos e limitações de proteção estão em painéis próprios. Não encontrei colisões relevantes ou textos cortados.

Nas três pranchas conferi moldura, carimbo, revisão, número, unidades, legenda, notas e aviso obrigatório. As tabelas são legíveis com ampliação ou na impressão A3.

## Consistência dos derivados

Cada PDF tem uma página A3 paisagem. PDFs foram rasterizados independentemente e comparados aos PNGs equivalentes, normalizados a 4960 × 3507 px. Erro absoluto médio por canal RGB:

| Prancha | Diferença média PDF–PNG (escala 0–255) |
| :---: | ---: |
| 01 | 1,539 |
| 02 | 1,628 |
| 03 | 2,024 |

As diferenças pequenas são compatíveis com antialiasing; conteúdo e composição coincidem.

## Auditorias e limites

- Validação específica: **PASS**, 49 verificações, sem erros.
- AutoCAD AcCoreConsole 2027: abertura e auditoria **PASS** nos três DXFs.
- Os três DXFs foram regenerados; os hashes permaneceram idênticos.

As verificações não demonstram estabilidade da microrrede, dimensionamento, proteção, autonomia real, autorização de interconexão ou atendimento normativo.
