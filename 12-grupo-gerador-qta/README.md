# Projeto 12: Grupo Moto-Gerador Diesel (250 kVA) com QTA e USCA

Documentação técnica e projeto executivo em AutoCAD de um **Sistema de Grupo Moto-Gerador (GMG) Diesel de Emergência de 250 kVA / 380–220 V** com **Quadro de Transferência Automática (QTA)** em transição aberta e **Unidade de Supervisão de Corrente Alternada (USCA)** microprocessada.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

---

## 1. Dados Nominais da Instalação

| Parâmetro | Valor Nominal | Observação |
| :--- | :--- | :--- |
| **Potência Standby do GMG** | 250 kVA / 200 kW | Regime de emergência (falha da rede da concessionária) |
| **Potência Prime do GMG** | 225 kVA / 180 kW | Regime de operação contínua variável |
| **Tensão e Frequência** | 380/220 V - 60 Hz | Trifásico a 4 fios (3F + N + PE) |
| **Velocidade Nominal** | 1800 rpm | Motor diesel 6 cilindros em linha, injeção eletrônica |
| **Corrente Nominal ($I_n$)** | 379,8 A | Dimensionamento para barramento e disjuntor de 400 A |
| **Fator de Potência** | 0,80 indutivo | Padrão NBR ISO 8528 |
| **Tipo de Transferência** | Transição Aberta (*Break-Before-Make*) | Intertravamento mecânico e elétrico duplo |
| **Tempo de Comutação Típico** | < 15 segundos | Da detecção de falha de rede até a assunção de carga |
| **Capacidade do Tanque** | 250 litros | Autonomia de aproximadamente 5,5 horas a 100% de carga |
| **Nível de Atenuação Acústica** | 75 dB(A) a 1,5 metro | Cabine insonorizada com atenuadores de ruído |

---

## 2. Índice de Pranchas (A3 Paisagem)

O conjunto é composto por 6 pranchas desenvolvidas em AutoCAD e salvas no formato DXF AC1027/R2013:

1. **`01_diagrama_unifilar_qta.dxf`:** Diagrama unifilar de potência do QTA (Rede, GMG, contatores K1/K2 intertravados, DPS e barramento de cargas essenciais).
2. **`02_diagrama_trifilar_potencia.dxf`:** Esquema trifilar detalhado de força (3F+N+PE), circuitos de alimentação auxiliar, carregador de baterias e resistor de bloco.
3. **`03_diagrama_funcional_comando.dxf`:** Diagrama funcional da USCA microprocessada, sensoriamento AC de rede/gerador, saídas de partida/parada e intertravamento de transferência.
4. **`04_regua_bornes_interligacao.dxf`:** Mapeamento de régua de bornes de potência (X1, X2, X3) e de controle/sensoriamento (XC1 e XC2) entre painel e cabine do GMG.
5. **`05_layout_painel_qta.dxf`:** Layout frontal da porta com IHM, comutador e sinalizadores, e placa de montagem interna com barramentos e componentes.
6. **`06_planta_instalacao_gmg.dxf`:** Planta de implantação da sala de geradores, atenuadores acústicos de admissão e descarga, escape de gases com silencioso hospitalar e bacia de contenção de diesel.

---

## 3. Rastreabilidade de Arquivos

```text
12-grupo-gerador-qta/
├── fonte/
│   ├── 01_diagrama_unifilar_qta.dxf
│   ├── 02_diagrama_trifilar_potencia.dxf
│   ├── 03_diagrama_funcional_comando.dxf
│   ├── 04_regua_bornes_interligacao.dxf
│   ├── 05_layout_painel_qta.dxf
│   ├── 06_planta_instalacao_gmg.dxf
│   ├── gerar_projeto_12.py
│   ├── renderizar_projeto_12.py
│   └── validar_projeto_12.py
├── exports/
│   ├── *.pdf (A3 vetorial para impressão)
│   ├── *.svg (visualização vetorial em navegador)
│   └── *.png (inspeção em 300 dpi)
├── README.md
├── memorial-descritivo.md
├── criterios-premissas.md
├── memoria-calculo.md
├── referencias-normativas.md
├── inspecao-visual.md
├── lista-materiais.csv
├── lista-cabos.csv
└── validacao.json
```

---

## 4. Como Abrir no AutoCAD

1. Abra o arquivo desejado diretamente na pasta `fonte/` com o AutoCAD 2013 ou posterior (incluindo o AutoCAD 2027 instalado).
2. Para salvar como `.dwg`, utilize o comando `SAVEAS` no AutoCAD e selecione o formato DWG padrão.
