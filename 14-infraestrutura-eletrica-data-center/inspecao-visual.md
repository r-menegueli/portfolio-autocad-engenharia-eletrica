# Inspeção visual e validação — P14

**Data:** 2026-11-06

**Formato:** A3 paisagem, 420 × 297 mm; PNGs de 4960 × 3507 px.

## Inspeção das pranchas

- **01 — Arquitetura:** os caminhos A/B são rastreáveis desde a alimentação MT até as entradas duplas dos racks. GE, QGBT/ATS, UPS e PDU estão identificados. As fontes e a separação física permanecem explicitamente não comprovadas. Não encontrei colisões relevantes, cortes ou conteúdo fora da moldura.
- **02 — Layout:** seis racks aparecem com entradas e rotas A/B distintas; as zonas QMT, TR, QGBT, UPS e pátio dos geradores estão separadas. O desenho declara que a planta é esquemática e sem escala. Não encontrei colisões relevantes ou textos cortados.
- **03 — Balanço e contingências:** tabelas de carga, capacidade e sequência ocupam painéis distintos. As contas de PUE, kVA, TR, GE e UPS conferem com as premissas documentadas. O caso de perda de um caminho deixa explícita a margem nula da UPS restante no limite assumido. Não encontrei colisões relevantes ou textos cortados.

Nas três pranchas foram conferidos moldura, unidade, carimbo, revisão, numeração, legenda, notas e aviso obrigatório. A leitura de detalhes pequenos depende de aproximação ou impressão em A3, como previsto no padrão do repositório.

## Consistência dos derivados

Cada PDF contém uma página A3 paisagem. PDFs foram rasterizados independentemente e comparados aos PNGs correspondentes, normalizados a 4960 × 3507 px. O erro absoluto médio por canal RGB foi:

| Prancha | Diferença média PDF–PNG (escala 0–255) |
| :---: | ---: |
| 01 | 1,566 |
| 02 | 1,618 |
| 03 | 2,028 |

As diferenças pequenas são compatíveis com antialiasing e rasterização; conteúdo e composição coincidem.

## Auditorias e limites

- Validação específica: **PASS**, 54 verificações, sem erros.
- Validação integrada estrita: **PASS**, 701.686 verificações, zero erros e zero avisos.
- AutoCAD AcCoreConsole 2027: abertura e auditoria **PASS** nos três DXFs.

Os resultados verificam estrutura, aritmética, abertura CAD e consistência dos derivados. Não comprovam dimensionamento, desempenho dinâmico, classificação de disponibilidade, atendimento normativo ou aptidão para execução.
