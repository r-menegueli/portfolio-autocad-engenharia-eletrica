# Projeto 05 - Instalação elétrica industrial

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 07

Formato: A3 paisagem, unidades em milímetros, revisão 00

Estado: concluído e validado em 2026-09-09

Este projeto acadêmico apresenta a distribuição elétrica conceitual de uma oficina
metalmecânica fictícia de `30,00 x 18,00 m`, com área de `540,00 m²`. A alimentação
adotada é `380/220 V`, trifásica, `60 Hz`, com esquema TN-S conceitual a jusante do
ponto de entrega. QGBT-05 alimenta QDF-05, QDL-05 e QADM-05.

## Entregáveis

- `fonte/`: sete desenhos DXF R2013 e scripts reproduzíveis;
- `exports/`: versões PDF, SVG e PNG derivadas dos DXFs;
- `memorial-descritivo.md`: descrição do sistema e de suas interfaces;
- `criterios-premissas.md`: hipóteses, critérios de cálculo e limitações;
- `memoria-calculo.md`: potências, demandas, correntes e quedas de tensão;
- `referencias-normativas.md`: referências e condição de uso;
- `quadro-cargas.csv`: fonte tabular dos 16 circuitos;
- `alimentadores.csv`: consolidação dos quatro alimentadores;
- `lista-cabos.csv` e `lista-materiais.csv`: rastreabilidade de rotas e quantitativos;
- `tabelas-projeto-05.xlsx`: workbook técnico com fórmulas e auditoria;
- `fonte/gerar_tabelas_05.mjs`: fonte reproduzível do workbook;
- `validacao-calculos.json` e `validacao.json`: resultados das validações específica e global;
- `inspecao-visual.md`: registro da inspeção dos arquivos renderizados.

## Pranchas

1. [Layout industrial](fonte/01_layout_industrial.dxf): implantação, dimensões,
   máquinas, tomadas e quadros.
2. [Distribuição de força](fonte/02_distribuicao_forca.dxf): circuitos C01 a C08,
   cargas trifásicas e tomadas industriais.
3. [Distribuição de iluminação](fonte/03_distribuicao_iluminacao.dxf): luminárias,
   comandos e circuitos C09 a C13.
4. [Eletrocalhas e rotas](fonte/04_eletrocalhas_rotas.dxf): E-501, E-502, E-503,
   alimentadores e descidas.
5. [Diagrama unifilar](fonte/05_diagrama_unifilar.dxf): entrada, QGBT-05, quadros
   secundários, DPS, DR, N e PE.
6. [Quadro de cargas](fonte/06_quadro_cargas.dxf): 16 circuitos e resumo elétrico.
7. [Detalhes de instalação](fonte/07_detalhes_instalacao.dxf): eletrocalha, tomada,
   quadro, equipotencialização e identificação.

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Resultados principais

| Grandeza | Resultado |
| --- | ---: |
| Potência ativa instalada | 68,495 kW |
| Potência aparente instalada | 80,277 kVA |
| Potência ativa demandada | 48,069 kW |
| Potência aparente demandada | 56,289 kVA |
| Corrente equivalente de demanda | 85,523 A |
| Maior corrente de fase no alimentador geral | 86,550 A |
| Proteção geral preliminar | 4P, 100 A |
| Alimentador geral preliminar | 4 x 50 mm² + PE 25 mm² Cu |
| Maior queda combinada estimada | 3,808% |

## Documentação

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Quadro de cargas](quadro-cargas.csv)
- [Alimentadores](alimentadores.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de materiais](lista-materiais.csv)
- [Workbook técnico](tabelas-projeto-05.xlsx)
- [Validação específica](validacao-calculos.json)
- [Validação estrita](validacao.json)

## Como reproduzir

Na raiz do portfólio, execute:

```powershell
.venv\Scripts\python.exe scripts\construir.py --root . --strict
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 05-instalacao-eletrica-industrial\validacao.json
node 05-instalacao-eletrica-industrial\fonte\gerar_tabelas_05.mjs --root .
```

O comando Node pressupõe a dependência `@oai/artifact-tool` 2.8.59 instalada conforme
o `package.json`; ambientes com módulos compartilhados podem informá-los por
`--node-modules <diretório>`. O workbook confere as mesmas entradas usadas nos CSVs e
nas pranchas. Nenhum DWG é fornecido; os DXFs AC1027 são as fontes principais.

Resultado registrado: validação específica `PASS` com 294 verificações; validação
estrita do portfólio `PASS` com 200.489 verificações, zero erros e zero avisos.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
