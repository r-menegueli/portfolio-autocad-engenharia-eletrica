# Memória de Cálculo: Grupo Moto-Gerador e QTA (250 kVA)

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

---

## 1. Dimensionamento Elétrico da Geração e Comutação

### 1.1 Corrente Nominal do GMG
A potência aparente nominal em regime de emergência (*standby*) é $S = 250\text{ kVA}$ sob tensão trifásica de linha $V = 380\text{ V}$:

$$I_n = \frac{S}{\sqrt{3} \times V} = \frac{250 \times 10^3}{\sqrt{3} \times 380} = \frac{250.000}{658,18} = 379,83\text{ A}$$

### 1.2 Dispositivos de Manobra e Proteção no QTA
* **Disjuntor de Entrada da Rede (DJ-REDE):** Caixa moldada $400\text{ A}$, proposta 3P+N para acompanhar o neutro comutado, $I_{cu} = 25\text{ kA}$ em 380 V.
* **Disjuntor de Entrada do Gerador (DJ-GER):** Caixa moldada $400\text{ A}$, proposta 3P+N para acompanhar o neutro comutado, $I_{cu} = 16\text{ kA}$ em 380 V.
* **Contatores de Comutação (K1 e K2):**
  - Categoria de emprego AC-1 (cargas resistivas/mistas): $I_e = 450\text{ A} > I_n$.
  - Categoria de emprego AC-3 (cargas de motores): $I_e = 400\text{ A} \ge I_n$.
  - Bobinas de comando: 220 Vca, 60 Hz.
  - Neutro comutado por polo dedicado. Proteção do neutro, compatibilidade com o esquema de aterramento e coordenação devem ser definidos para os equipamentos e a instalação reais.

### 1.3 Dimensionamento do Barramento de Cobre do QTA
* **Critério de Ampacidade:** Para corrente nominal de $380\text{ A}$ e considerando fator de sobrecarga de 25%:
  $$I_{projeto} = 1,25 \times 379,83 = 474,8\text{ A}$$
* **Barra Selecionada:** Cobre eletrolítico chato de $40 \times 5\text{ mm}$ (seção transversal $200\text{ mm}^2$):
  - Capacidade de condução contínua ao ar livre (elevação de temperatura $30^\circ\text{C}$): $I_z = 520\text{ A}$.
  - Condição atendida: $I_z = 520\text{ A} > 475\text{ A}$.
* **Barramento de Neutro:** Dimensão $30 \times 5\text{ mm}$ ($I_z = 400\text{ A}$), isolado do chassi do quadro.
* **Barramento de Terra (PE):** Dimensão $30 \times 5\text{ mm}$, aparafusado diretamente à carcaça e interligado ao BEP.

### 1.4 Cabos de Interligação GMG $\rightarrow$ QTA
* **Condições de Instalação:** Condutores de cobre unipolares, isolação EPR 90°C 0,6/1 kV, instalados em eletrocalha metálica perfurada em vão livre (Método F da NBR 5410).
* **Solução com Condutores em Paralelo por Fase:**
  - 2 cabos de $120\text{ mm}^2$ por fase ($2 \times 120\text{ mm}^2$).
  - Capacidade nominal de 1 condutor $120\text{ mm}^2$ no Método F: $I_{z1} = 299\text{ A}$.
  - Capacidade total por fase (fator de agrupamento $0,80$):
    $$I_{z,total} = 2 \times 299 \times 0,80 = 478,4\text{ A} > 380\text{ A}$$
  - Condutores de Neutro: $2 \times 120\text{ mm}^2$ EPR.
  - Condutor de Proteção (PE): $1 \times 120\text{ mm}^2$ cobre isolado Verde/Amarelo.

---

## 2. Dimensionamento Térmico e Mecânico

### 2.1 Consumo Específico e Autonomia de Combustível
Para motores diesel turboalimentados de alta rotação (1800 rpm), o consumo específico em carga nominal é aproximadamente $0,22\text{ litros/(kWh)}$.
* A 100% de carga ($P = 200\text{ kW}$):
  $$C_{100\%} = 200\text{ kW} \times 0,22\text{ l/kWh} = 44,0\text{ l/h}$$
* A 75% de carga ($P = 150\text{ kW}$):
  $$C_{75\%} = 150\text{ kW} \times 0,22\text{ l/kWh} = 33,0\text{ l/h}$$
* Autonomia com tanque diário de 250 litros:
  $$T_{aut, 100\%} = \frac{250\text{ l}}{44,0\text{ l/h}} \approx 5,68\text{ horas (5h 41min)}$$
  $$T_{aut, 75\%} = \frac{250\text{ l}}{33,0\text{ l/h}} \approx 7,58\text{ horas (7h 35min)}$$

### 2.2 Volume da Bacia de Contenção de Diesel
Conforme preceito da ABNT NBR 17505 e diretrizes ambientais:

$$V_{bacia} \ge 1,10 \times V_{tanque} = 1,10 \times 250\text{ l} = 275\text{ litros} = 0,275\text{ m}^3$$

Dimensões da bacia integrada sob a base do GMG: $2,20\text{ m} \times 0,90\text{ m} \times 0,15\text{ m} = 0,297\text{ m}^3 = 297\text{ litros} > 275\text{ litros}$ (**Aprovado**).

### 2.3 Vazão de Ar de Arrefecimento e Áreas de Venezianas
* Vazão de ar do radiador: $Q_{rad} = 5,2\text{ m}^3/\text{s}$.
* Vazão de ar para combustão: $Q_{comb} = 0,28\text{ m}^3/\text{s}$.
* Vazão total de admissão: $Q_{adm} = 5,48\text{ m}^3/\text{s}$.
* Velocidade máxima admitida na tomada de ar frio: $v_{adm} = 3,0\text{ m/s}$.
  $$A_{util, adm} = \frac{5,48}{3,0} = 1,83\text{ m}^2$$
  Considerando veneziana acústica com área livre de 50%, área frontal total: $A_{frontal, adm} = 3,66\text{ m}^2$.
* Velocidade máxima admitida na descarga de ar quente: $v_{desc} = 4,5\text{ m/s}$.
  $$A_{util, desc} = \frac{5,20}{4,5} = 1,16\text{ m}^2$$
  Área frontal com veneziana com 50% de passagem livre: $A_{frontal, desc} = 2,32\text{ m}^2$.
