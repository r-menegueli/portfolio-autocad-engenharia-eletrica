# Projeto 06 - Centro de Controle de Motores

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 09

Formato: A3 paisagem, unidades em milímetros, revisão gráfica 03 (2026-11-05)

Estado: revisão acadêmica 03; validação de fonte e derivados registrada abaixo.

O CCM-06 acadêmico integra três métodos de acionamento em uma instalação fictícia
380/220 V, 3F+N+PE, 60 Hz: partida direta da bomba M-601, reversão da esteira M-602 e
controle por inversor do ventilador M-603. O projeto demonstra interfaces comuns sem
repetir o painel individual do Projeto 01.

## Entregáveis

- `fonte/`: nove desenhos DXF AC1027 e scripts reproduzíveis;
- `exports/`: derivados PDF, SVG e PNG;
- `lista-cargas.csv`: três cargas e respectivos critérios elétricos;
- `alimentador.csv`: alimentador geral W600;
- `lista-cabos.csv`, `lista-bornes.csv` e `lista-materiais.csv`: rastreabilidade;
- `causa-efeito.csv`: nove eventos de falha, ação e limites conhecidos;
- `memorial-descritivo.md`, `criterios-premissas.md` e `memoria-calculo.md`;
- `sequencia-funcionamento.md` e `referencias-normativas.md`;
- `validacao-integracao.json` e `validacao.json`;
- `inspecao-visual.md`.

## Pranchas

1. [Diagrama unifilar do CCM](fonte/01_diagrama_unifilar_ccm.dxf)
2. [Partida direta da bomba](fonte/02_partida_direta.dxf)
3. [Partida reversora da esteira](fonte/03_partida_reversora.dxf)
4. [Acionamento por inversor](fonte/04_acionamento_inversor.dxf)
5. [Layout do CCM](fonte/05_layout_ccm.dxf)
6. [Diagrama de bornes](fonte/06_diagrama_bornes.dxf)
7. [Lista de cabos](fonte/07_lista_cabos.dxf)
8. [Matriz causa–efeito do CCM-06](fonte/08_matriz_causa_efeito_ccm.dxf)
9. [Balanço de demanda do CCM-06](fonte/09_balanco_demanda_ccm.dxf)

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Resultados principais

| Grandeza | Resultado |
| --- | ---: |
| Potência ativa instalada | 18,185 kW |
| Potência aparente instalada | 20,893 kVA |
| Potência ativa demandada | 16,645 kW |
| Potência aparente demandada | 19,134 kVA |
| Corrente equivalente demandada | 29,071 A |
| Proteção geral preliminar | 4P, 50 A |
| Alimentador preliminar | 4 x 10 mm² + PE 10 mm² Cu |
| Maior queda combinada | 2,038% em M-601 |

## Validação da revisão 03

- Validador específico: `PASS`, 864 verificações e zero erros; nove folhas e nove eventos causa–efeito.
- Validador estrito do portfólio: `PASS`, 561.440 verificações, zero erros e zero avisos.
- Revisor consolidado: `PASS`, 12 projetos, 102 folhas, 408 arquivos gráficos e 71 CSVs;
  similaridade mínima PDF/PNG de 0,9841.
- P06-09 consolida a demanda aplicada a cada motor, os totais instalados/demandados e
  a relação aritmética declarada para W600. Os fatores, o disjuntor e Iz continuam
  premissas; isso não valida curto-circuito, seletividade nem instalação.
- P06-09 foi conferida no PNG de produção a 300 dpi e em PDF rasterizado a 150 dpi; a
  tabela, as barras comparativas, os limites do alimentador e o carimbo ficaram legíveis,
  sem cortes ou colisões visíveis. O contato atualizado das nove pranchas foi conferido.
- O AutoCAD AcCoreConsole 2027 abriu e auditou 9/9 DXFs. A inspeção visual de SVGs no
  navegador segue aguardando autorização do usuário.
- Respostas de falha e reset dependentes dos modelos KSR/VFD permanecem pendentes; P06-08 registra uma sequência conceitual.

## Documentação

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Lista de cargas](lista-cargas.csv)
- [Alimentador](alimentador.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de bornes](lista-bornes.csv)
- [Lista de materiais](lista-materiais.csv)
- [Matriz causa–efeito](causa-efeito.csv)
- [Validação específica](validacao-integracao.json)
- [Validação estrita](validacao.json)

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 06-centro-controle-motores\fonte\gerar_projeto_06.py --root .
.venv\Scripts\python.exe 06-centro-controle-motores\fonte\validar_projeto_06.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 06-centro-controle-motores\validacao.json
```

Nenhum DWG é fornecido; os DXFs AC1027 são as fontes principais.

## Histórico da revisão 00

- validador específico: `PASS`, 828 verificações e nenhum erro;
- validador estrito do portfólio: `PASS`, 238.890 verificações, nenhum erro e nenhum
  aviso;
- abertura e auditoria no Autodesk AcCoreConsole 2027: `PASS` nos sete DXFs;
- PDF: sete arquivos A3 paisagem, uma página, reabertos e rasterizados pelo Poppler;
- SVG e PNG: sete pares inspecionados visualmente, sem cortes ou texto ilegível;
- reprodutibilidade: os hashes dos sete DXFs e dos 21 derivados permaneceram idênticos
  após nova geração e renderização.
- testes automatizados do repositório: 9 aprovados.

Os resultados acima registram a revisão 00. A revisão 02 e seus limites constam em [inspecao-visual.md](inspecao-visual.md), `validacao-integracao.json` e `validacao.json`.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
