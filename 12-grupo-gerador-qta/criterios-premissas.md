# Critérios de Projeto e Premissas Técnicas

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

---

## 1. Premissas Elétricas

* **Alimentação Primária:** Concessionária de energia em baixa tensão trifásica 380/220 V ($V_{FF} = 380\text{ V}$, $V_{FN} = 220\text{ V}$), 60 Hz, neutro diretamente aterrado na subestação (esquema TN-S).
* **Nível de Curto-Circuito da Rede:** Corrente de curto-circuito simétrica presumida no ponto de entrega de $I_{cc} = 25\text{ kA}$.
* **Alimentação de Emergência:** GMG diesel 250 kVA Standby / 200 kW, 380/220 V, $I_n = 379,8\text{ A}$, reatância subtransitória de eixo direto $X''_d = 12\%$, corrente de curto-circuito simétrica sustentada por excitação PMG limitada a aproximadamente $3 \times I_n \approx 1,14\text{ kA}$ durante 10 segundos para seletividade a jusante.
* **Corrente de Projeto do QTA:** $I_{b} = 380\text{ A}$. Barramento principal dimensionado com margem de segurança de 30% ($I_z \ge 500\text{ A}$).
* **Comutação Tetrapolar:** O contator K1 e o contator K2 manobram as três fases e o condutor neutro (4 polos comutáveis), garantindo o total isolamento galvânico entre as fontes de geração e evitando correntes circulantes de neutro/harmônicas indesejadas.

---

## 2. Premissas Mecânicas e Civis

* **Local de Instalação do GMG:** Abrigo técnico externo ao lado do bloco industrial/hospitalar, sobre radier de concreto armado com espessura de 20 cm, isolado das fundações prediais por junta de dilatação elastomérica para absorção de vibração mecânica.
* **Atenuação Acústica:** Limite de pressão sonora externa de $75\text{ dB(A)}$ a 1,5 metro de distância, em conformidade com a NBR 10151 para áreas industriais/comerciais no período diurno e noturno.
* **Sistema de Descarga de Gases:** Tubulação em aço carbono sem costura ASTM A53 Grau B, diâmetro nominal 4" (DN 100 mm), isolada termicamente com manta de lã de rocha (espessura 50 mm, densidade $64\text{ kg/m}^3$) revestida com chapa de alumínio corrugado 0,5 mm. Silencioso de absorção e reatividade com atenuação de 30 dB(A) e dreno de água condensada na base.
* **Combustível e Segurança Ambiental:** Tanque diário de 250 litros integrado na base do grupo gerador, provido de bacia de contenção em chapa de aço estanque soldada com volume útil mínimo de 275 litros (110% da capacidade total do reservatório).

---

## 3. Filosofia de Controle e Automação

1. **Modo Automático:** A USCA permanece monitorando as tensões de linha e de fase da rede da concessionária. Havendo sub/sobretensão prolongada (> 3 s) ou falta de fase, o comando de partida do GMG é ativado. Quando a tensão e frequência do gerador atingem a faixa estável nominal ($380\text{ V} \pm 2\%$ e $60\text{ Hz} \pm 1\%$), o contator K1 é aberto e, após o *dead time* de 1,5 s, o contator K2 é fechado.
2. **Modo Manual:** Permite a partida do motor via tecla de teste e manobra manual local dos contatores de transferência pelo painel frontal.
3. **Modo Teste com Carga e Sem Carga:** Permite a realização de rotinas semanais de teste programado do grupo gerador para verificação da saúde das baterias e integridade mecânica do motor.
4. **Circuito Auxiliar de Bateria:** Tensão de 12 Vcc com 1 bateria chumbo-ácido selada AGM de 150 Ah / 1000 CCA. O painel inclui carregador inteligente de flutuação de 12 Vcc / 5 A alimentado permanentemente pela rede da concessionária.
