# Relatório de Inspeção Visual e Geometria CAD — Projeto 12

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

---

## 1. Critérios de Inspeção

Todas as 6 pranchas do Projeto 12 (`12-grupo-gerador-qta`) foram submetidas à auditoria geométrica, tipográfica e visual em 300 dpi (PNG) e em formato vetorial (PDF e SVG):

1. **Conformidade de Folha A3 Paisagem:** Dimensões exatas de $420 \times 297\text{ mm}$, margem esquerda de $25\text{ mm}$ para encadernação e margens superior/inferior/direita de $10\text{ mm}$.
2. **Reserva de Carimbo e Notas:** Área de desenho útil estritamente contida no retângulo $X \in [25, 402]$, $Y \in [100, 260]$, garantindo zero colisão com os blocos de legenda, notas, aviso obrigatório e carimbo técnico ($Y \le 94\text{ mm}$).
3. **Ausência de Sobreposição de Textos:** Uso de cabeçalhos estruturados (`panel_box`) com linha divisória antes dos itens internos das caixas e espaçamento vertical mínimo de $8\text{ mm}$ entre linhas de texto.
4. **Padronização de Layers:**
   - `00_MOLDURA` e `01_CARIMBO`: Estrutura de folha A3.
   - `02_TEXTO`: Textos descritivos e parâmetros técnicos.
   - `03_COTAS`: Linhas de cota e dimensões físicas.
   - `04_EQUIPAMENTOS`: Contornos de painéis, gerador, contatores e componentes.
   - `05_POTENCIA`: Barramentos trifásicos e circuitos principais 380/220 V.
   - `06_COMANDO`: Circuito de controle 12 Vcc / 220 Vca e USCA.
   - `07_INSTRUMENTACAO`: TCs, sensores de pressão/temperatura/nível.
   - `08_CABOS`: Condutores de interligação.
   - `09_BORNES`: Réguas X1, X2, X3, XC1 e XC2.
   - `10_ELETROCALHAS`: Leitos e canaletas de cabos.
   - `11_ARQUITETURA`: Alvenaria da sala do GMG, base civil e bacia de contenção.

---

## 2. Resultado por Prancha

| Prancha | Arquivo | Status | Observações de Inspeção |
| :---: | :--- | :---: | :--- |
| 01/06 | `01_diagrama_unifilar_qta.dxf` | **APROVADO** | Fontes Rede e GMG claramente separadas, intertravamento K1/K2 destacado e QCE legível. |
| 02/06 | `02_diagrama_trifilar_potencia.dxf` | **APROVADO** | Fases R, S, T, N e PE bem espaçadas, derivação para carregador e pré-aquecimento nítida. |
| 03/06 | `03_diagrama_funcional_comando.dxf` | **APROVADO** | Bloco da USCA centralizado, entradas de tensão AC à esquerda e saídas de relé/intertravamento à direita. |
| 04/06 | `04_regua_bornes_interligacao.dxf` | **APROVADO** | Réguas de potência e comando alinhadas com numeração sequencial e destino de cabos. |
| 05/06 | `05_layout_painel_qta.dxf` | **APROVADO** | Vista externa frontal e placa de montagem interna em escala, sem textos sobrepostos. |
| 06/06 | `06_planta_instalacao_gmg.dxf` | **APROVADO** | Planta baixa da sala e detalhe do escape hospitalar com cotas claras e organizadas. |
