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

## 3. Estudo da malha: entradas requeridas, sem resultado numérico

A revisão 02 retira a estimativa geométrica anterior porque área, resistividade, corrente de falta e condutores não foram medidos ou confirmados. Não há resistência de malha calculada ou medida e nenhum resultado de segurança pode ser inferido.

O arquivo [`dados-estudo-aterramento.csv`](dados-estudo-aterramento.csv) mantém 22 entradas como `A DEFINIR/PENDENTE`. Antes de registrar resultados, obter e rastrear, no mínimo:

- perfil de resistividade do solo, camadas, resistividade e espessura da camada superficial e condição sazonal;
- cenários de falta, parcela de corrente que entra na malha, fontes/retornos remotos e tempo de eliminação baseado na proteção selecionada;
- levantamento do pátio, geometria e profundidade dos condutores, eletrodos, conexões, BEP, cercas e interfaces metálicas externas;
- zonas de acesso e condições de superfície consideradas no estudo;
- método, critérios, memória de cálculo e revisão técnica documentada.

A folha 07 organiza esse fluxo. Ela não executa cálculos, define limites admissíveis ou declara segurança/aprovação. GPR, potenciais de toque, passo e transferência, resistência/impedância da malha e dimensionamento de condutores permanecem sem resultados até haver dados e critérios válidos.

---

## 4. Premissas conceituais de SPDA (sem verificação de conformidade)

* A prancha ilustra uma edificação assumida de $6,00\text{ m} \times 4,00\text{ m}$ e condutores/descidas propostos.
* A classe, o método, a geometria, os componentes e as distâncias são premissas de estudo, não uma seleção validada.
* Não há análise de risco, levantamento, projeto de captação/descidas, cálculo de distâncias de segurança ou coordenação completa de DPS.
* Confirmar as edições vigentes das normas e desenvolver o projeto com dados reais antes de qualquer conclusão de conformidade.

---
> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
