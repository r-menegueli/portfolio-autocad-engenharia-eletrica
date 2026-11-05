# Projeto 07 - Arquitetura elétrica acadêmica de veículo elétrico

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 08

Formato: A3 paisagem, unidades geométricas em milímetros, revisão gráfica 01 (2026-11-05)

Estado: concluído e validado em 2026-09-09

Este projeto apresenta a arquitetura elétrica conceitual do EV-07, um veículo elétrico
didático com bateria de tração, inversor e motor de indução. O escopo relaciona a
arquitetura física às estratégias de controle V/f e FOC estudadas no TCC do autor, sem
declarar, reproduzir ou inventar qualquer resultado experimental do trabalho acadêmico.

## Escopo

- bateria de tração, BMS, fusíveis, contatores, pré-carga e PDU de alta tensão;
- inversor trifásico e motor de indução;
- conversor CC-CC, bateria auxiliar de 12 V e distribuição de baixa tensão;
- VCU, sensores, comunicação CAN, HVIL e monitoramento de isolação;
- permissivos, desligamento de emergência e estados seguros conceituais;
- diagramas comparativos das cadeias de controle V/f e FOC.

Não estão incluídos carregador embarcado, conector de recarga, homologação veicular,
software executável de controle, projeto mecânico, ensaios, análise térmica, EMC,
ASIL, HARA, FMEDA ou dimensionamento executivo.

## Pranchas

1. [Arquitetura geral](fonte/01_arquitetura_geral.dxf)
2. [Circuito de alta tensão](fonte/02_circuito_alta_tensao.dxf)
3. [Circuito de baixa tensão](fonte/03_circuito_baixa_tensao.dxf)
4. [Pré-carga e contatores](fonte/04_pre_carga_contatores.dxf)
5. [Inversor e motor](fonte/05_inversor_motor.dxf)
6. [Sensores e controle](fonte/06_sensores_controle.dxf)
7. [Rede de comunicação](fonte/07_rede_comunicacao.dxf)
8. [Layout dos componentes](fonte/08_layout_componentes.dxf)

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Separação epistemológica

| Classe | Conteúdo usado neste projeto |
| --- | --- |
| Fato técnico | funções gerais de BMS, pré-carga, inversor, motor de indução, CAN e estratégias de controle, apoiadas nas referências declaradas |
| Premissa acadêmica | 400 V nominais, faixa 320-450 V, 60 kW, 60 kWh, 2.200 µF, 100 Ω, 12 V e comprimentos de cabos |
| Proposta conceitual | tags, topologia EV-07, limiares, mensagens CAN, estados e disposição física |
| Resultado experimental | nenhum; este projeto não contém medições, curvas de bancada, eficiência medida ou validação do TCC |

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Estratégias V/f e FOC](estrategias-controle.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Referências técnicas](referencias-normativas.md)
- [Parâmetros conceituais](parametros.csv)
- [Lista de sinais](lista-sinais.csv)
- [Matriz CAN](rede-can.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de materiais](lista-materiais.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-arquitetura.json)
- [Validação estrita](validacao.json)

## Verificação da revisão 00

- oito fontes DXF AC1027 abertas e auditadas individualmente pelo Autodesk
  AcCoreConsole 2027, sem erro;
- 4.224 verificações específicas aprovadas, incluindo combinações de permissivos,
  pré-carga, habilitação de torque, tags, cálculos e coerência entre tabelas;
- validação estrita integrada aprovada em 272.953 verificações, sem erros nem avisos;
- 24 derivados examinados: oito PNGs de produção, oito PDFs reabertos e
  rasterizados pelo Poppler e oito SVGs abertos no Google Chrome;
- nova geração com hashes idênticos em 32/32 artefatos, sendo oito DXFs e 24
  derivados;
- nove testes automatizados aprovados.

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 07-arquitetura-veiculo-eletrico\fonte\gerar_projeto_07.py --root .
.venv\Scripts\python.exe 07-arquitetura-veiculo-eletrico\fonte\validar_projeto_07.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 07-arquitetura-veiculo-eletrico\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
