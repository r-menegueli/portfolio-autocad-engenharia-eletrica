# Relatório de GitHub e revisão — 2026-11-05

## Estado da publicação

Os cinco branches desta revisão foram enviados aos repositórios existentes e estão
abertos como pull requests em rascunho. Os branches `main` permanecem sem alterações;
nenhum PR foi mesclado.

| Repositório | Commit | PR de revisão |
| --- | --- | --- |
| [Perfil](https://github.com/r-menegueli/r-menegueli) | `ed62f17` | [#1 — Clarify engineering portfolio claims](https://github.com/r-menegueli/r-menegueli/pull/1) |
| [Portfólio AutoCAD](https://github.com/r-menegueli/portfolio-autocad-engenharia-eletrica) | `695972d` | [#1 — Refresh CAD portfolio drawings and technical audit](https://github.com/r-menegueli/portfolio-autocad-engenharia-eletrica/pull/1) |
| [Automação PLC/SCADA](https://github.com/r-menegueli/automacao-clp-scada-iec61131) | `40e336d` | [#1 — Align QTA logic and document PLCopen draft](https://github.com/r-menegueli/automacao-clp-scada-iec61131/pull/1) |
| [PCB/KiCad](https://github.com/r-menegueli/hardware-pcb-kicad-industrial) | `fd09bf1` | [#1 — Mark PCB repository as a conceptual scaffold](https://github.com/r-menegueli/hardware-pcb-kicad-industrial/pull/1) |
| [BIM/MEP](https://github.com/r-menegueli/modelagem-bim-3d-eletrica-mep) | `db078cd` | [#1 — Clarify BIM model as volumetric placeholders](https://github.com/r-menegueli/modelagem-bim-3d-eletrica-mep/pull/1) |

Branch comum: `codex/professional-portfolio-2026-11`. Cada PR foi anexado à tarefa
para acompanhamento. Os cinco estão abertos e marcados como draft.

## Auditoria CAD repetida antes desta revisão

- 557 arquivos incluídos na árvore do portfólio e 366 links locais examinados.
- Sem achados de CPF, telefone, endereço, credenciais ou caminhos locais nos arquivos
  atuais; nenhum arquivo excede 50 MiB.
- Resultado: `WARN`, com uma observação no endereço de e-mail registrado num commit
  preexistente do `main`. Não reescrevi o histórico compartilhado.
- Um primeiro resultado `FAIL` foi uma colisão de dígitos dentro de um SHA-256 do
  manifesto. O detector foi ajustado para ignorar hashes hexadecimais de 64 caracteres;
  a repetição eliminou esse falso positivo e manteve apenas o aviso histórico acima.

## Evidência de revisão CAD

- `09-fonte-bancada/fonte/gerar_projeto_09.py` e `scripts/renderizar.py`: oito
  pranchas P09 regeneradas em DXF, PDF, SVG e PNG.
- `09-fonte-bancada/fonte/validar_projeto_09.py`: 18.616 verificações, 0 erros.
- `scripts/validar_portfolio.py --root . --strict`: 434.039 verificações, 0 erros,
  0 avisos.
- `scripts/revisar_portfolio.py --root .`: 12 projetos, 83 pranchas, 332 arquivos
  gráficos e 55 CSVs; similaridade mínima PDF/PNG de 0,9842.
- P09-07/08 foram inspecionadas em PNG integral e PDF rasterizado; P09-02/03/06/07
  também foram conferidas nos PNGs após as correções de rótulos e legibilidade.
- AutoCAD/AcCoreConsole não foi reaberto; os SVGs P09-07/08 aguardam a inspeção
  visual no navegador, conforme pedido do usuário.

## Limites conhecidos

P11 continua um estudo conceitual: aterramento, toque/passo, GPR, SPDA e seleção de
DPS não estão validados. P09 agora tem topologia e pré-dimensionamento, mas K1 apenas
desabilita a alimentação: sem descarga dedicada, 0 V residual nos bornes não é
garantido. Malhas, compensação, seleção térmica, proteções e layout EMI seguem
pendentes. KiCad, FreeCAD
e IDE de CLP não foram abertos nesta revisão; os respectivos PRs descrevem os artefatos
como scaffold, placeholders ou rascunhos quando aplicável. Os rascunhos permitem
revisar os diffs sem publicar essas mudanças nos branches padrão.

> Para integrar as mudanças, revise os cinco PRs e faça o merge no GitHub depois da
> revisão técnica desejada.
