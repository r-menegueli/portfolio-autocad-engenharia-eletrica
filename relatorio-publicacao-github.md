# Relatório de publicação no GitHub

**Data da preparação:** 2026-11-08  
**Repositório:** `r-menegueli/portfolio-autocad-engenharia-eletrica`  
**Branch de trabalho:** `codex/p23-p25-studies`  
**Destino:** `main`  
**Estado:** preparado; publicação direta autorizada e pendente de execução.

O trabalho acrescenta os projetos P23–P25 à coleção e preserva o histórico anterior.
O push só ocorrerá após conferir que `origin/main` continua ancestral desta branch;
sem avanço rápido, não será forçada a atualização.

## Conteúdo preparado

- **25 projetos** e **140 pranchas A3** em DXF, PDF, SVG e PNG.
- **967 arquivos** na árvore, total de 280.331.377 bytes antes da compressão Git.
- Formatos principais: 142 DXFs, 141 PDFs, 142 SVGs, 147 PNGs, 106 CSVs,
  35 JSONs, 165 arquivos Markdown, 66 arquivos Python, 11 scripts MATLAB, 2 modelos
  Simulink e 2 workbooks XLSX.
- Código gerador e validador dos novos estudos, cálculos MATLAB, documentação,
  resultados e modelos Simulink P23/P25.
- DXF AC1027 em milímetros; arquivos DWG não fazem parte da entrega.

Não serão incluídos `.venv/`, caches MATLAB (`slprj/` e `*.slxc`), logs, saídas de
`work/`, temporários nem credenciais. As regras relevantes estão no `.gitignore`.

## Auditoria e validação

O auditor [`auditar_publicacao.py`](scripts/auditar_publicacao.py) examinou 967
arquivos, 883 blobs históricos e 612 links relativos: **zero erros e um aviso**.
O aviso é um e-mail pessoal em um commit antigo do histórico (identificador
`14c30d95098d`); o auditor oculta o valor. Esse commit antecede esta entrega e o
histórico não foi reescrito.

| Verificação | Escopo | Resultado |
| --- | ---: | :---: |
| Validador estrito do portfólio | P01–P25; 649.131 verificações | PASS, zero erros e avisos |
| Validador focado | 30 pranchas P23–P25 | PASS |
| AutoCAD Core Console 2027 | 30 DXFs P23–P25 | 30/30 PASS; P24 repetido após ajuste |
| MATLAB | cálculos P23, P24 e P25 | 3/3 PASS |
| Simulink | modelos dinâmicos P23 e P25 | PASS |
| Pytest | suíte Python atual | 11/11 PASS |
| `git diff --check` | alterações preparadas | PASS |

P24 contém uma pendência técnica explícita: no cenário de 140 MW, a corrente
calculada de 585,72 A ultrapassa a estimativa térmica de 571,04 A. O condutor e as
condições térmicas precisam de revisão antes de qualquer evolução do estudo. Os
modelos Simulink usam blocos padrão e equivalentes agregados em pu; Simscape Electrical
não estava licenciado neste ambiente.

O maior arquivo atual tem 1.576.950 bytes; não há arquivos próximos aos limites de
50 MiB ou 100 MiB do GitHub. Os derivados vetoriais e raster fazem parte deliberada da
entrega visual.

## Licenças e referências

A licença dual se aplica aos 25 projetos: MIT para código e configurações executáveis;
CC BY-NC 4.0 para desenhos, documentos, imagens, tabelas e artefatos acadêmicos. Os
novos estudos mantêm uma lista de referências técnicas por projeto. Suas premissas e
limitações estão nos respectivos READMEs e memoriais.

## Comandos reproduzíveis

```powershell
python .\scripts\validar_portfolio.py --root . --strict
python .\scripts\validar_estudos_p23_p25.py --project all
python .\scripts\auditar_publicacao.py --root .
python -m pytest -q
```

Os relatórios individuais de engenharia e validação ficam nas pastas P23–P25. Este
documento será atualizado com o resultado do push e o identificador final publicado.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
