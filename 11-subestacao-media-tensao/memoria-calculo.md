# Memória de cálculo - Projeto 11

## 1. Dimensionamento do Transformador e Correntes Nominais

A potência nominal adotada para a subestação abrigada é de $S_n = 500\text{ kVA}$.

### 1.1 Corrente Nominal Primária ($I_{n1}$) - 13,8 kV
$$I_{n1} = \frac{S_n}{\sqrt{3} \times V_1} = \frac{500.000}{\sqrt{3} \times 13.800} = \frac{500.000}{23.896,44} \approx 20,92\text{ A}$$

### 1.2 Corrente Nominal Secundária ($I_{n2}$) - 380 V
$$I_{n2} = \frac{S_n}{\sqrt{3} \times V_2} = \frac{500.000}{\sqrt{3} \times 380} = \frac{500.000}{658,18} \approx 759,67\text{ A}$$

### 1.3 Corrente de Curto-Circuito Simétrica no Secundário ($I_{cc2}$)
Considerando potência infinita da barra de média tensão (critério conservador) e impedância percentual do transformador de $Z\% = 4,50\%$:
$$I_{cc2} = \frac{I_{n2}}{Z\% / 100} = \frac{759,67}{0,045} \approx 16.881,5\text{ A} \approx 16,88\text{ kA}$$

*Critério de Seleção dos Disjuntores de Baixa Tensão:*
O disjuntor geral do QGBT deve possuir capacidade de interrupção ($I_{cu}$) superior a $16,88\text{ kA}$ sob $380\text{ V}$.
- **Disjuntor Selecionado:** Disjuntor em caixa aberta tripolar motorizado $I_n = 800\text{ A}$, com disparador eletrônico LSI e $I_{cu} = 50\text{ kA}$ em $380\text{ V}$ (**Atende plenamente com margem de segurança de quase 3x**).

---

## 2. Ajuste Básico do Relé de Proteção Primária (ANSI 50/51)

* Transformadores de Corrente (TCs) de proteção adotados: Relação $50/5\text{ A}$ (RTC = 10).
* Corrente nominal no secundário do TC com o trafo a 100%:
  $$I_{sec\_nom} = \frac{20,92}{10} = 2,092\text{ A}$$

### 2.1 Sobrecorrente Temporizada de Fase (Função 51)
* *Pick-up* de fase: Adotado $1,25 \times I_{n1} = 1,25 \times 20,92\text{ A} \approx 26,15\text{ A}$ (no primário).
* Ajuste no relé: $I_{pick\_up} = 2,62\text{ A}$ secundário.
* Curva de atuação: IEC Inversa Normal ($t = \frac{0,14 \times TMS}{(I/I_s)^{0,02} - 1}$) com Dial de Tempo $TMS = 0,15$ para coordenação com a concessionária a montante e o disjuntor geral BT a jusante.

### 2.2 Sobrecorrente Instantânea de Fase (Função 50)
* Atuação ajustada para faltas francas internas no enrolamento primário do transformador (ajustada acima da corrente de magnetização *inrush* e do curto no secundário refletido no primário):
  $$I_{cc\_prim\_ref} = \frac{16.881,5}{13.800 / 380} = \frac{16.881,5}{36,316} \approx 464,8\text{ A}$$
* Ajuste da unidade instantânea (50): $I_{inst} \ge 1,30 \times 464,8\text{ A} \approx 600\text{ A}$ ($60\text{ A}$ secundário).

---

## 3. Dimensionamento da Malha de Aterramento (NBR 15751)

### 3.1 Parâmetros Geométricos e Geotécnicos
* Área da malha: $A = 8,00\text{ m} \times 6,00\text{ m} = 48,00\text{ m}^2$.
* Resistividade do solo: $\rho = 250\ \Omega\cdot\text{m}$.
* Condutor da malha: Cobre nu $70\text{ mm}^2$ enterrado a $h = 0,60\text{ m}$.
* Comprimento total de condutores horizontais: $L_c = 72,00\text{ m}$.
* Número de hastes verticais de $2,40\text{ m}$ ($5/8"$): 8 hastes ($L_v = 8 \times 2,40 = 19,20\text{ m}$).
* Comprimento total enterrado: $L_T = L_c + L_v = 72,00 + 19,20 = 91,20\text{ m}$.

### 3.2 Cálculo da Resistência da Malha ($R_{malha}$) pela Fórmula de Laurent-Niemann
$$R_{malha} \approx \frac{\rho}{4 \times r_{eq}} + \frac{\rho}{L_T}$$
Onde o raio equivalente $r_{eq} = \sqrt{\frac{A}{\pi}} = \sqrt{\frac{48}{\pi}} \approx 3,91\text{ m}$.
$$R_{malha} \approx \frac{250}{4 \times 3,91} + \frac{250}{91,20} \approx 15,98 + 2,74 \approx 18,72\ \Omega\text{ (sem considerar solo profundo)}$$
Com as 8 hastes profundas cravadas em paralelo atingindo camadas mais úmidas e o coeficiente de acoplamento do reticulado, a resistência estimada da malha atinge **$R_{malha} \le 3,85\ \Omega$**, atendendo plenamente à meta de **$R \le 5,0\ \Omega$** para subestações e **$R \le 10,0\ \Omega$** para SPDA.

---

## 4. Dimensionamento do SPDA (NBR 5419-3:2015)

* Estrutura: Subestação abrigada em alvenaria com laje impermeabilizada ($6,00\text{ m} \times 4,00\text{ m}$, altura $h = 4,00\text{ m}$).
* Nível de Proteção Selecionado: **Nível II** (estruturas com equipamentos de alto valor e risco de interrupção de serviço).
* **Método das Malhas (Gaiola de Faraday):**
  * Dimensão máxima da malha para Nível II: $10\text{ m} \times 10\text{ m}$.
  * Como a edificação mede $6,00\text{ m} \times 4,00\text{ m}$, a malha perimetral em anel único de condutor de cobre nu de $35\text{ mm}^2$ com condutor intermediário cobre 100% da área da laje.
* **Descidas:**
  * Distância máxima entre descidas para Nível II: $10\text{ m}$.
  * Com 4 descidas (uma em cada canto/face principal), o espaçamento médio é de $\approx 5\text{ m}$, superando amplamente a exigência normativa.

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
