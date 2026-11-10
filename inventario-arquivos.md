# Inventário de arquivos

Inventário atualizado em 2026-11-08 para o portfólio de Rogério Eduardo Moreira
Menegueli. A contagem considera os arquivos versionados (incluindo as mudanças desta
revisão) e exclui `.git/`, `.venv/`, caches e saídas temporárias em `work/`.

## Resumo do repositório

| Tipo | Quantidade | Função |
| --- | ---: | --- |
| DXF | 142 | 140 pranchas de projeto, template e carimbo |
| PDF | 141 | 140 pranchas de projeto e template A3 |
| SVG | 142 | 140 pranchas de projeto, template e carimbo |
| PNG | 147 | pranchas, prévias e template para inspeção visual |
| CSV | 106 | entradas, resultados, materiais e listas técnicas |
| XLSX | 2 | workbooks técnicos dos Projetos 04 e 05 |
| Markdown | 165 | READMEs, memoriais, critérios, memórias e relatórios |
| JSON | 35 | validações e manifesto |
| Python | 66 | geração, renderização, revisão, validadores e testes |
| MATLAB / Simulink | 13 | 11 scripts `.m` e 2 modelos `.slx` |
| PowerShell / SCR | 2 | automação e auditoria pelo AutoCAD |
| TOML | 2 | configuração do portfólio e parâmetros de renderização |
| Outros arquivos de configuração/licença | 4 | Git, dependências e licença |
| **Total versionado** | **967** | inventário após a preparação desta revisão |

Nenhum arquivo DWG integra o repositório. Dos 967 arquivos, 924 pertencem às pastas
dos projetos e 43 são documentação, configuração, templates ou ferramentas comuns.

## Inventário por projeto

| Projeto | Pranchas | Arquivos | Markdown | CSV | Linhas de dados CSV | JSON | XLSX |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P01 | 6 | 34 | 6 | 2 | 39 | 1 | 0 |
| P02 | 8 | 45 | 6 | 3 | 55 | 2 | 0 |
| P03 | 8 | 47 | 7 | 4 | 125 | 2 | 0 |
| P04 | 6 | 42 | 8 | 5 | 70 | 2 | 1 |
| P05 | 7 | 44 | 6 | 4 | 78 | 2 | 1 |
| P06 | 7 | 44 | 7 | 5 | 85 | 2 | 0 |
| P07 | 8 | 49 | 8 | 5 | 88 | 2 | 0 |
| P08 | 6 | 40 | 6 | 6 | 102 | 2 | 0 |
| P09 | 6 | 41 | 6 | 7 | 160 | 2 | 0 |
| P10 | 6 | 45 | 7 | 9 | 82 | 2 | 0 |
| P11 | 6 | 36 | 6 | 2 | 40 | 1 | 0 |
| P12 | 6 | 36 | 6 | 2 | 39 | 1 | 0 |
| P13 | 3 | 22 | 5 | 2 | 13 | 1 | 0 |
| P14 | 3 | 22 | 5 | 2 | 16 | 1 | 0 |
| P15 | 3 | 22 | 5 | 2 | 16 | 1 | 0 |
| P16 | 3 | 22 | 5 | 2 | 18 | 1 | 0 |
| P17 | 3 | 25 | 5 | 5 | 50 | 1 | 0 |
| P18 | 3 | 23 | 5 | 3 | 19 | 1 | 0 |
| P19 | 3 | 25 | 5 | 5 | 44 | 1 | 0 |
| P20 | 3 | 25 | 5 | 5 | 42 | 1 | 0 |
| P21 | 3 | 24 | 5 | 4 | 37 | 1 | 0 |
| P22 | 3 | 24 | 5 | 4 | 28 | 1 | 0 |
| P23 | 10 | 63 | 7 | 6 | 207 | 1 | 0 |
| P24 | 10 | 61 | 7 | 6 | 189 | 1 | 0 |
| P25 | 10 | 63 | 7 | 6 | 128 | 1 | 0 |
| **Total** | **140** | **924** | **150** | **106** | **1.770** | **34** | **2** |

Cada prancha de projeto forma um conjunto de quatro arquivos homônimos: um DXF em
`fonte/` e PDF, SVG e PNG em `exports/`. Os números acima contam também os arquivos
de documentação, scripts, dados e validação de cada pasta.

## Rastreabilidade

O inventário detalhado por arquivo pode ser regenerado localmente com:

```powershell
.\.venv\Scripts\python.exe .\scripts\revisar_portfolio.py --root .
```

A saída inclui projeto, prancha, identificador, tipo, caminho, tamanho e dimensões das tabelas CSV. Ela é derivada e permanece fora do controle de versão. O [manifesto de renders](renders/manifesto.json)
relaciona os artefatos gráficos, e [portfolio.toml](portfolio.toml) é a fonte de
verdade para projetos, layers, geometria e caminhos.
