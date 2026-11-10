# Inventário de arquivos

Inventário consolidado em 2026-11-05 para o portfólio de Rogério Eduardo Moreira
Menegueli. A contagem considera os arquivos incluídos nesta revisão e exclui
`.git/`, `.venv/`, `node_modules/`, caches e saídas temporárias em `work/`.

## Resumo do repositório

| Tipo | Quantidade | Função |
| --- | ---: | --- |
| DXF | 100 | 98 pranchas de projeto, template e carimbo |
| PDF | 99 | 98 pranchas de projeto e template A3 |
| SVG | 100 | 98 pranchas de projeto, template e carimbo |
| PNG | 99 | 98 pranchas de projeto e template A3 |
| CSV | 70 | entradas, cálculos, cabos, bornes, materiais, proteção, verificação, causa–efeito, rastreabilidade por ambiente e dados para coordenação |
| XLSX | 2 | workbooks técnicos dos Projetos 04 e 05 |
| Markdown | 95 | READMEs, memoriais, critérios, memórias e relatórios |
| JSON | 22 | validações e manifesto |
| Python | 37 | geração, renderização, revisão, validadores e testes |
| PowerShell / SCR | 2 | automação e auditoria pelo AutoCAD |
| Outros arquivos de configuração/licença | 6 | Git, Python, licença e configuração |
| **Total** | **632** | arquivos incluídos nesta revisão, sem caches nem saídas temporárias |

Nenhum arquivo DWG integra o repositório.

## Inventário por projeto

| Projeto | Pranchas | Arquivos | Markdown | CSV | Linhas de dados CSV | JSON | XLSX |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P01 | 8 | 44 | 6 | 4 | 58 | 1 | 0 |
| P02 | 9 | 50 | 6 | 4 | 63 | 2 | 0 |
| P03 | 10 | 57 | 7 | 6 | 145 | 2 | 0 |
| P04 | 7 | 47 | 8 | 6 | 79 | 2 | 1 |
| P05 | 9 | 54 | 6 | 6 | 96 | 2 | 1 |
| P06 | 8 | 49 | 7 | 6 | 94 | 2 | 0 |
| P07 | 9 | 54 | 8 | 6 | 98 | 2 | 0 |
| P08 | 7 | 45 | 6 | 7 | 115 | 2 | 0 |
| P09 | 9 | 55 | 6 | 9 | 210 | 2 | 0 |
| P10 | 7 | 50 | 7 | 10 | 90 | 2 | 0 |
| P11 | 7 | 41 | 6 | 3 | 62 | 1 | 0 |
| P12 | 8 | 45 | 6 | 3 | 48 | 1 | 0 |
| **Total** | **98** | **591** | **83** | **70** | **1.158** | **21** | **2** |

Cada uma das 98 pranchas de projeto forma um conjunto de quatro arquivos homônimos: um DXF em
`fonte/` e PDF, SVG e PNG em `exports/`. A auditoria consolidada confirmou os 98
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

O inventário detalhado por arquivo pode ser regenerado localmente com:

```powershell
.\.venv\Scripts\python.exe .\scripts\revisar_portfolio.py --root .
```

A saída inclui projeto, prancha, identificador, tipo, caminho, tamanho e dimensões das tabelas CSV. Ela é derivada e permanece fora do controle de versão.
