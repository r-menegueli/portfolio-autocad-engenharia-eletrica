# P16 — Parque eólico: coleta elétrica e conexão à rede

Estudo conceitual da infraestrutura elétrica de um parque eólico terrestre hipotético com cinco aerogeradores, dois alimentadores coletores em 34,5 kV, subestação elevadora e ponto de conexão representado em 69 kV. O conjunto demonstra organização de unifilar, implantação esquemática, bases aritméticas e interfaces de controle e proteção.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Unifilar dos aerogeradores, alimentadores, barra coletora, transformador e POI | [DXF](fonte/01_unifilar_coleta_conexao.dxf) | [PDF](exports/01_unifilar_coleta_conexao.pdf) | [SVG](exports/01_unifilar_coleta_conexao.svg) | [PNG](exports/01_unifilar_coleta_conexao.png) |
| 02/03 | Implantação esquemática das cinco unidades e das rotas F01/F02 | [DXF](fonte/02_layout_parque_eolico.dxf) | [PDF](exports/02_layout_parque_eolico.pdf) | [SVG](exports/02_layout_parque_eolico.svg) | [PNG](exports/02_layout_parque_eolico.png) |
| 03/03 | Potências aparentes, correntes nominais estimadas e interfaces pendentes | [DXF](fonte/03_base_calculo_interfaces.dxf) | [PDF](exports/03_base_calculo_interfaces.pdf) | [SVG](exports/03_base_calculo_interfaces.svg) | [PNG](exports/03_base_calculo_interfaces.png) |

Documentos de apoio: [memorial descritivo](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências normativas](referencias-normativas.md), [lista de materiais](lista-materiais.csv), [lista de sinais](lista-sinais.csv), [gerador](fonte/gerar_projeto_16.py), [validador específico](fonte/validar_projeto_16.py), [resultado da validação](validacao-projeto-16.json) e [inspeção visual](inspecao-visual.md).

## Dados assumidos

- Cinco aerogeradores de 2,0 MW cada: 10 MW instalados.
- Transformador elevador unitário hipotético de 2,5 MVA por aerogerador, com tensão ilustrativa de 0,69/34,5 kV.
- Dois alimentadores radiais de coleta em 34,5 kV, com três unidades em F01 e duas em F02.
- Transformador principal hipotético de 12,5 MVA, relação 34,5/69 kV, e ponto de conexão representado em 69 kV.
- Fator de potência de 0,95 usado apenas para os cálculos aritméticos apresentados.

Os dados não são especificações comerciais nem resultado de estudos de acesso. Não há local, curvas OEM ou estudo de recurso eólico. A energia anual não foi estimada.

## Como reproduzir

Na raiz do repositório, com Python 3.11+ e as dependências listadas em `requirements.txt`:

```powershell
python .\16-parque-eolico-coleta-conexao\fonte\gerar_projeto_16.py --root .
python .\scripts\renderizar.py --root . --artifact p16-01-unifilar-coleta-conexao --artifact p16-02-layout-parque-eolico --artifact p16-03-base-calculo-interfaces
python .\16-parque-eolico-coleta-conexao\fonte\validar_projeto_16.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

O DXF AC1027 é a fonte CAD editável em milímetros. PDF, SVG e PNG são derivados; não há DWG neste projeto.

## Limites

O projeto não define fabricação, instalação, obra ou comissionamento. Estão pendentes, entre outros: modelo e curva de potência do aerogerador; tensão e capacidade de conversores; recurso eólico e energia anual; distâncias e rotas; bitolas e ampacidade dos cabos; perdas e queda de tensão; curto-circuito; aterramento e proteção contra descargas atmosféricas; proteção, seletividade e coordenação; harmônicos e estabilidade; controle de potência ativa e reativa; telecomunicações; requisitos de acesso, estudos da rede e aprovações aplicáveis.

As referências normativas orientam o estudo, mas não constituem declaração de conformidade. Requisitos e edições devem ser confirmados para o empreendimento real.
