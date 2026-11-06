# Inspeção visual — P17

Revisão das três folhas A3 em PNG e comparação independente dos PDFs por rasterização PDFium a 300 dpi.

| Prancha | Auditoria DXF/AutoCAD | PDF | PNG | Resultado visual |
| --- | --- | --- | --- | --- |
| 01 — Diagrama funcional SAS/IED | ezdxf e AutoCAD 2027: PASS | 1 página, 420 × 297 mm | 4960 × 3507 px; MAE PDF/PNG 1,777 | Fluxo elétrico, associação funcional dos IEDs, notas e carimbo sem cortes ou colisões relevantes. |
| 02 — Redes IEC 61850 | ezdxf e AutoCAD 2027: PASS | 1 página, 420 × 297 mm | 4960 × 3507 px; MAE PDF/PNG 1,978 | Separação entre rede de processo e de estação; MUs, switch, IEDs e serviços estão identificados e legíveis. |
| 03 — Matriz GOOSE e verificações | ezdxf e AutoCAD 2027: PASS | 1 página, 420 × 297 mm | 4960 × 3507 px; MAE PDF/PNG 2,057 | Publisher/subscriber, ações, sequência SCL, verificações e limites permanecem dentro dos quadros. |

As pranchas incluem moldura, carimbo, legenda, notas e o aviso acadêmico obrigatório. A diferença entre as dimensões raster do PDFium e do PNG foi alinhada por recorte de um pixel antes do cálculo do erro médio absoluto.

A inspeção confirma a apresentação e a consistência visual dos formatos; não demonstra interoperabilidade, conformidade IEC 61850, proteção funcional ou aptidão para operação real.
