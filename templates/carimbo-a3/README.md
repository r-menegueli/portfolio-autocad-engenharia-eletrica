# Carimbo A3 reutilizavel

O arquivo [`carimbo-a3.dxf`](carimbo-a3.dxf) contem o bloco `CARIMBO_A3`, com
dimensoes de 180 x 58 mm e atributos editaveis. A visualizacao vetorial esta em
[`carimbo-a3.svg`](carimbo-a3.svg).

## Atributos

| Tag | Conteudo |
|---|---|
| `TITULO` | titulo descritivo da prancha |
| `AUTOR` | nome do autor |
| `DATA` | data ISO 8601 |
| `REVISAO` | revisao de dois algarismos |
| `PRANCHA` | numero atual e total |
| `ARQUIVO` | nome do DXF-fonte |
| `UNIDADES` | unidade declarada |
| `ESCALA` | escala da folha |
| `FOLHA` | formato A3 |
| `STATUS` | estado documental |

O gerador oficial em [`../../scripts/gerar_template_a3.py`](../../scripts/gerar_template_a3.py)
recria este arquivo. Para uso em um projeto, inserir o bloco em `(230, 10)` na
folha A3 ou usar o template completo em [`../template-a3.dxf`](../template-a3.dxf).
