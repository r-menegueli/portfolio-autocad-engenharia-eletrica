# Inspeção visual e validação — P13

**Data:** 2026-11-06

**Formato:** A3 paisagem, 420 × 297 mm; exportações PNG com 4960 × 3507 px.

## Inspeção das pranchas

- **01 — Implantação:** seis posições e equipamentos estão identificados; circulação, áreas técnicas e premissas geométricas estão separadas. O texto “ROTA: A DEFINIR” deixa explícito que a rota física dos cabos depende de levantamento. Não há colisões relevantes, cortes ou conteúdo fora da moldura.
- **02 — Unifilar:** a sequência rede, medição, QGBT existente e QEV-01 está legível; os seis alimentadores e as interfaces do EMS estão distinguidos. As proteções aparecem como funções sem especificação. Não há colisões relevantes ou textos cortados.
- **03 — Gestão de potência:** entradas, estados, sequência, limites por ponto e cenários aritméticos ocupam áreas distintas. Os totais de 120, 142, 93 e 164 kW conferem com as hipóteses registradas. A prancha indica que essas somas não representam limite da rede. Não há colisões relevantes ou textos cortados.

Nas três folhas foram conferidos moldura, hierarquia, unidades, carimbo, revisão, número de prancha, legenda, notas e aviso obrigatório. Os textos pequenos permanecem adequados para leitura ampliada ou impressão em A3; a visão reduzida serve apenas para conferir composição.

## Consistência dos derivados

Cada PDF tem uma página A3 paisagem. PDFs foram rasterizados independentemente e comparados aos PNGs correspondentes, ambos normalizados a 4960 × 3507 px. O erro absoluto médio por canal RGB foi:

| Prancha | Diferença média PDF–PNG (escala 0–255) |
| :---: | ---: |
| 01 | 1,857 |
| 02 | 1,680 |
| 03 | 2,190 |

As diferenças pequenas são compatíveis com rasterização e antialiasing; a composição e o conteúdo coincidem.

## Auditorias e limites

- Validação específica: **PASS**, 29 verificações, sem erros.
- Validação integrada estrita: **PASS**, 688.933 verificações, zero erros e zero avisos.
- AutoCAD AcCoreConsole 2027: abertura e auditoria **PASS** nos três DXFs.

Esses resultados verificam estrutura, aritmética, compatibilidade de abertura e consistência dos arquivos. Não comprovam dimensionamento, atendimento normativo, aprovação de concessionária, acessibilidade do local nem aptidão para execução.
