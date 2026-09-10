# Inventário de arquivos

Inventário consolidado em 2026-09-10 para o portfólio de Rogério Eduardo Moreira
Menegueli. A contagem considera os arquivos versionados após esta revisão e exclui
`.git/`, `.venv/`, `node_modules/`, caches e saídas temporárias em `work/`.

## Resumo do repositório

| Tipo | Quantidade | Função |
| --- | ---: | --- |
| DXF | 70 | 68 pranchas de projeto, template e carimbo |
| PDF | 69 | 68 pranchas de projeto e template A3 |
| SVG | 70 | 68 pranchas de projeto, template e carimbo |
| PNG | 69 | 68 pranchas de projeto e template A3 |
| CSV | 50 | entradas, cálculos, cabos, bornes e materiais |
| XLSX | 2 | workbooks técnicos dos Projetos 04 e 05 |
| Markdown | 81 | READMEs, memoriais, critérios, memórias e relatórios |
| JSON | 21 | validações, manifesto e metadados de dependência |
| Python | 28 | geração, renderização, revisão, validadores e testes |
| JavaScript MJS | 2 | geração/revisão de workbooks |
| PowerShell / SCR | 2 | automação e auditoria pelo AutoCAD |
| Outros arquivos de configuração/licença | 6 | Git, Python, Node, licença e configuração |
| **Total versionado** | **470** | inventário final desta revisão |

Nenhum arquivo DWG integra o repositório.

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
| **Total** | **68** | **431** | **67** | **50** | **884** | **19** | **2** |

Cada prancha de projeto forma um conjunto de quatro arquivos homônimos: um DXF em
`fonte/` e PDF, SVG e PNG em `exports/`. A auditoria consolidada confirmou os 68
conjuntos completos, sem nomes-base divergentes.

## Contrato documental

Todos os dez projetos contêm:

- README individual, memorial descritivo e critérios/premissas;
- `lista-materiais.csv` e demais listas específicas;
- script-fonte Python e fontes DXF;
- derivados PDF, SVG e PNG;
- registro de inspeção visual e relatório JSON de validação.

Memórias de cálculo e documentos funcionais adicionais aparecem quando aplicáveis. O
[manifesto de renders](renders/manifesto.json) é a relação processável dos artefatos
gráficos, e [portfolio.toml](portfolio.toml) é a fonte de verdade para projetos,
layers, geometria e caminhos.

## Rastreabilidade

O inventário detalhado por arquivo pode ser regenerado em
`work/revisao-portfolio/inventario.csv` com:

```powershell
.\.venv\Scripts\python.exe .\scripts\revisar_portfolio.py --root .
```

Essa saída local inclui projeto, prancha, identificador, tipo, caminho, tamanho e
dimensões das tabelas CSV. Ela é deliberadamente ignorada pelo Git para evitar
versionar dados diagnósticos derivados.
