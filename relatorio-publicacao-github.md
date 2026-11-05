# Relatório de GitHub e revisão — 2026-11-05

## Estado da publicação

Os cinco branches desta revisão foram enviados aos repositórios existentes e estão
abertos como pull requests em rascunho. Os branches `main` permanecem sem alterações;
nenhum PR foi mesclado.

| Repositório | Commit | PR de revisão |
| --- | --- | --- |
| [Perfil](https://github.com/r-menegueli/r-menegueli) | `ed62f17` | [#1 — Clarify engineering portfolio claims](https://github.com/r-menegueli/r-menegueli/pull/1) |
| [Portfólio AutoCAD](https://github.com/r-menegueli/portfolio-autocad-engenharia-eletrica) | `83acb57` | [#1 — Refresh CAD portfolio drawings and technical audit](https://github.com/r-menegueli/portfolio-autocad-engenharia-eletrica/pull/1) |
| [Automação PLC/SCADA](https://github.com/r-menegueli/automacao-clp-scada-iec61131) | `40e336d` | [#1 — Align QTA logic and document PLCopen draft](https://github.com/r-menegueli/automacao-clp-scada-iec61131/pull/1) |
| [PCB/KiCad](https://github.com/r-menegueli/hardware-pcb-kicad-industrial) | `fd09bf1` | [#1 — Mark PCB repository as a conceptual scaffold](https://github.com/r-menegueli/hardware-pcb-kicad-industrial/pull/1) |
| [BIM/MEP](https://github.com/r-menegueli/modelagem-bim-3d-eletrica-mep) | `db078cd` | [#1 — Clarify BIM model as volumetric placeholders](https://github.com/r-menegueli/modelagem-bim-3d-eletrica-mep/pull/1) |

Branch comum: `codex/professional-portfolio-2026-11`. Cada PR foi anexado à tarefa
para acompanhamento. Os cinco estão abertos e marcados como draft.

## Auditoria CAD repetida antes desta revisão

- 548 arquivos incluídos na árvore do portfólio e 361 links locais examinados.
- Sem achados de CPF, telefone, endereço, credenciais ou caminhos locais nos arquivos
  atuais; nenhum arquivo excede 50 MiB.
- Resultado: `WARN`, com uma observação no endereço de e-mail registrado num commit
  preexistente do `main`. Não reescrevi o histórico compartilhado.
- Um primeiro resultado `FAIL` foi uma colisão de dígitos dentro de um SHA-256 do
  manifesto. O detector foi ajustado para ignorar hashes hexadecimais de 64 caracteres;
  a repetição eliminou esse falso positivo e manteve apenas o aviso histórico acima.

## Evidência de revisão CAD

- `scripts/construir.py --root . --strict`: reconstrução aprovada.
- `scripts/validar_portfolio.py --root . --strict`: 423.829 verificações, 0 erros,
  0 avisos.
- `scripts/revisar_portfolio.py --root .`: 12 projetos, 81 pranchas, 324 arquivos
  gráficos e 54 CSVs; similaridade mínima PDF/PNG de 0,9842.
- DXFs e exportações foram inspecionados por geração e estrutura. AutoCAD/AcCoreConsole
  não foi reaberto nesta revisão.

## Limites conhecidos

P11 continua um estudo conceitual: aterramento, toque/passo, GPR, SPDA e seleção de
DPS não estão validados. P09 ainda precisa de uma topologia elétrica definida antes
de receber circuito detalhado. KiCad, FreeCAD e IDE de CLP não foram abertos nesta
revisão; os respectivos PRs descrevem os artefatos como scaffold, placeholders ou
rascunhos quando aplicável. Os rascunhos permitem revisar os diffs sem publicar essas
mudanças nos branches padrão.

> Para integrar as mudanças, revise os cinco PRs e faça o merge no GitHub depois da
> revisão técnica desejada.
