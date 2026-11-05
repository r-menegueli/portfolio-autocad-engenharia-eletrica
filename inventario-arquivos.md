# Inventário de arquivos

Inventário consolidado em 2026-11-05 para o portfólio de Rogério Eduardo Moreira
Menegueli. A contagem considera os arquivos incluídos nesta revisão e exclui
`.git/`, `.venv/`, `node_modules/`, caches e saídas temporárias em `work/`.

## Resumo do repositório

| Tipo | Quantidade | Função |
| --- | ---: | --- |
| DXF | 89 | 87 pranchas de projeto, template e carimbo |
| PDF | 88 | 87 pranchas de projeto e template A3 |
| SVG | 89 | 87 pranchas de projeto, template e carimbo |
| PNG | 88 | 87 pranchas de projeto e template A3 |
| CSV | 59 | entradas, cálculos, cabos, bornes, materiais e causa–efeito |
| XLSX | 2 | workbooks técnicos dos Projetos 04 e 05 |
| Markdown | 95 | READMEs, memoriais, critérios, memórias e relatórios |
| JSON | 22 | validações e manifesto |
| Python | 37 | geração, renderização, revisão, validadores e testes |
| PowerShell / SCR | 2 | automação e auditoria pelo AutoCAD |
| Outros arquivos de configuração/licença | 6 | Git, Python, licença e configuração |
| **Total** | **577** | 182.681.482 bytes |

Nenhum arquivo DWG integra o repositório.

## Inventário por projeto

| Projeto | Pranchas | Arquivos | Markdown | CSV | Linhas de dados CSV | JSON | XLSX |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P01 | 6 | 34 | 6 | 2 | 39 | 1 | 0 |
| P02 | 8 | 45 | 6 | 3 | 55 | 2 | 0 |
| P03 | 9 | 52 | 7 | 5 | 133 | 2 | 0 |
| P04 | 7 | 47 | 8 | 6 | 79 | 2 | 1 |
| P05 | 7 | 44 | 6 | 4 | 78 | 2 | 1 |
| P06 | 8 | 49 | 7 | 6 | 94 | 2 | 0 |
| P07 | 8 | 49 | 8 | 5 | 88 | 2 | 0 |
| P08 | 6 | 40 | 6 | 6 | 102 | 2 | 0 |
| P09 | 8 | 50 | 6 | 8 | 188 | 2 | 0 |
| P10 | 6 | 45 | 7 | 9 | 82 | 2 | 0 |
| P11 | 6 | 36 | 6 | 2 | 40 | 1 | 0 |
| P12 | 8 | 45 | 6 | 3 | 48 | 1 | 0 |
| **Total** | **87** | **536** | **83** | **59** | **1.026** | **21** | **2** |

Cada prancha de projeto forma um conjunto de quatro arquivos homônimos: um DXF em
`fonte/` e PDF, SVG e PNG em `exports/`. A auditoria consolidada confirmou os 87
conjuntos completos, sem nomes-base divergentes.

## Contrato documental

Todos os doze projetos contêm:

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
