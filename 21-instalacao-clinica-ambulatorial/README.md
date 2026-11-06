# P21 — Instalação elétrica de clínica ambulatorial

Estudo acadêmico de uma pequena clínica ambulatorial fictícia, com planta elétrica esquemática, fontes normal/gerador/UPS e matriz preliminar de continuidade. As três pranchas mostram interfaces e decisões pendentes; não definem solução executiva para estabelecimento de saúde.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Planta esquemática, iluminação, tomadas e rotas conceituais | [DXF](fonte/01_planta_eletrica_clinica.dxf) | [PDF](exports/01_planta_eletrica_clinica.pdf) | [SVG](exports/01_planta_eletrica_clinica.svg) | [PNG](exports/01_planta_eletrica_clinica.png) |
| 02/03 | Unifilar da rede normal, transferência, gerador e UPS | [DXF](fonte/02_unifilar_fontes_quadro_clinica.dxf) | [PDF](exports/02_unifilar_fontes_quadro_clinica.pdf) | [SVG](exports/02_unifilar_fontes_quadro_clinica.svg) | [PNG](exports/02_unifilar_fontes_quadro_clinica.png) |
| 03/03 | Matriz de continuidade, estados propostos e sequência de transferência | [DXF](fonte/03_matriz_continuidade_e_transferencia.dxf) | [PDF](exports/03_matriz_continuidade_e_transferencia.pdf) | [SVG](exports/03_matriz_continuidade_e_transferencia.svg) | [PNG](exports/03_matriz_continuidade_e_transferencia.png) |

Documentos e dados: [memorial descritivo](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências normativas](referencias-normativas.md), [lista de materiais](lista-materiais.csv), [lista de sinais](lista-sinais.csv), [matriz de cargas](matriz-cargas.csv), [plano de estudos](plano-estudos.csv), [gerador](fonte/gerar_projeto_21.py), [validador específico](fonte/validar_projeto_21.py), [resultado da validação](validacao-projeto-21.json) e [inspeção visual](inspecao-visual.md).

## Premissas do estudo

- Clínica ambulatorial fictícia com recepção, administração, consultórios, sala de procedimento e apoio; planta sem escala e sem dimensões construtivas.
- Tensão de alimentação ilustrativa: 380/220 V, 60 Hz. Confirmar padrão da concessionária e condições locais.
- Gerador, QTA e UPS aparecem como fontes candidatas; suas potências, autonomias, ventilação e requisitos de transferência não foram definidos.
- Nenhum ambiente foi enquadrado em grupo médico. A classificação depende dos procedimentos, equipamentos, avaliação clínica e norma aplicável.
- As designações “normal”, “reserva” e “UPS” na matriz são propostas de estudo, não declaração de serviço essencial nem de requisito normativo.

## Reprodução

Na raiz do repositório, usando o `.venv` e as dependências registradas:

```powershell
.\.venv\Scripts\python.exe .\21-instalacao-clinica-ambulatorial\fonte\gerar_projeto_21.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --artifact p21-01-planta-clinica --artifact p21-02-unifilar-fontes-clinica --artifact p21-03-matriz-continuidade-clinica
.\.venv\Scripts\python.exe .\21-instalacao-clinica-ambulatorial\fonte\validar_projeto_21.py --root .
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável em milímetros. PDF, SVG e PNG são derivados. Não há DWG neste projeto.

## Limites

Não foram feitos levantamento arquitetônico ou clínico, classificação dos locais, cálculo de demanda, curto-circuito, queda de tensão, dimensionamento de circuitos, seletividade, aterramento, iluminação de emergência, autonomia, ventilação do gerador/UPS, análise de risco, aprovação sanitária, ensaio ou verificação de campo. Consultar as edições vigentes das normas e as autoridades locais antes de qualquer especificação.
