# P19 — Alimentação elétrica de navios no cais (HVSC)

Estudo conceitual de uma interface de alimentação elétrica de alta tensão entre o cais e um navio compatível com HVSC. O pacote reúne diagrama unifilar, implantação esquemática, sequência de alto nível, premissas, cálculos aritméticos e listas rastreáveis de materiais, sinais e interfaces.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Unifilar do fornecimento do porto, transformação e ponto HVSC | [DXF](fonte/01_unifilar_hvsc_cais.dxf) | [PDF](exports/01_unifilar_hvsc_cais.pdf) | [SVG](exports/01_unifilar_hvsc_cais.svg) | [PNG](exports/01_unifilar_hvsc_cais.png) |
| 02/03 | Implantação esquemática da sala elétrica, cais, cabo e navio | [DXF](fonte/02_implantacao_eletrica_cais.dxf) | [PDF](exports/02_implantacao_eletrica_cais.pdf) | [SVG](exports/02_implantacao_eletrica_cais.svg) | [PNG](exports/02_implantacao_eletrica_cais.png) |
| 03/03 | Estados, permissivos, comunicação de dados e evento de abertura | [DXF](fonte/03_sequencia_intertravamentos_hvsc.dxf) | [PDF](exports/03_sequencia_intertravamentos_hvsc.pdf) | [SVG](exports/03_sequencia_intertravamentos_hvsc.svg) | [PNG](exports/03_sequencia_intertravamentos_hvsc.png) |

Documentos e dados: [memorial](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências](referencias-normativas.md), [cálculo de correntes](calculo-correntes.csv), [materiais](lista-materiais.csv), [sinais](lista-sinais.csv), [interfaces do navio](matriz-interfaces.csv), [sequência conceitual](sequencia-conexao.csv), [gerador](fonte/gerar_projeto_19.py), [validador](fonte/validar_projeto_19.py), [validação](validacao-projeto-19.json) e [inspeção visual](inspecao-visual.md).

## Caso-base ilustrativo

- Entrada do terminal: 13,8 kV, 60 Hz.
- Saída HVSC representada: 6,6 kV, 60 Hz.
- Transformador ilustrativo: 4 MVA, 13,8/6,6 kV.
- Demanda aparente didática no ponto de conexão: 3,2 MVA (80% da potência nominal assumida para o transformador).
- Corrente de linha calculada pela relação trifásica `I = S / (√3 × V)`: 133,9 A em 13,8 kV e 279,9 A em 6,6 kV, para a demanda assumida.

Esses valores não definem capacidade disponível do porto, compatibilidade com qualquer navio, carregamento contínuo, curto-circuito, proteção ou cabo. O transformador e as tensões são premissas didáticas; o perfil da embarcação, frequência, ligação, aterramento, conectores e sequência de transferência precisam ser confirmados em documentos oficiais do navio e do operador.

## Como reproduzir

Na raiz do repositório, com o ambiente `.venv` e as dependências de `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe .\19-alimentacao-navios-cais-hvsc\fonte\gerar_projeto_19.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --artifact p19-01-unifilar-hvsc-cais --artifact p19-02-implantacao-eletrica-cais --artifact p19-03-sequencia-intertravamentos-hvsc
.\.venv\Scripts\python.exe .\19-alimentacao-navios-cais-hvsc\fonte\validar_projeto_19.py --root .
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável em milímetros. PDF, SVG e PNG são derivados. Não há DWG neste projeto.

## Limites

O pacote não apresenta projeto executivo nem assegura conformidade com uma instalação portuária. Não foram feitos levantamento do cais, estudo de demanda, curto-circuito, coordenação, seletividade, aterramento, harmônicos, conversão de frequência, análise de risco, classificação de áreas, estudo mecânico de cabos, estudo ambiental ou verificação de compatibilidade com navio específico. A sequência é didática; não é instrução de manobra. A interface de comunicação funcional não substitui o circuito de segurança dedicado. Nenhum FAT, SAT, ensaio de proteção, teste de intertravamento ou teste operacional foi executado.
