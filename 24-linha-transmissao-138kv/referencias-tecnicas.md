# Referências técnicas — P24

Consulta documental revisada em 09/11/2026. Referências orientam o desenvolvimento; sua citação não demonstra conformidade do estudo.

## Condutor selecionado

- [Nexans Brasil — CAA 795 KCM 26/7F Drake Classe A, ref. 64719](https://www.nexans.com.br/pt/products/Transmission.and.Distribution/OHL.AWG/OHL/Aluminium541/product~64719~.html). Fonte para seção, diâmetro, GMR, massa, resistência CC/CA, ampacidade e carga de ruptura. A página informa o cenário associado à ampacidade de catálogo: condutor 75 °C, ambiente 25 °C, vento 1 m/s e sol. A página do produto cita ABNT NBR 7270/88 como padrão do cabo; isto não é critério de projeto da linha.
- [Ficha de produto Nexans ref. 64719 (PDF)](https://www.nexans.com.br/.rest/catalog/v1/product/pdf/64719). Fonte complementar de dados do produto.
- [Nexans — características de tensão/deformação para cabos T-ACSR (PDF)](https://www.nexans.com.br/.rest/eservice/dam/v1/file/223724/StressStrainACSR_br.pdf). A linha 26/7 fornece módulo e expansão para cabo T-ACSR; a equivalência com o CAA Drake da página anterior não foi demonstrada. Por isso `EA` e `α` aparecem como aproximações mecânicas provisórias, não como dados confirmados do condutor selecionado.

## Normas e método

- [IEEE Std 738-2023](https://standards.ieee.org/ieee/738/10207/) — método de relação corrente-temperatura para condutores nus aéreos; a página oficial indica status ativo. A norma não recomenda, por si, clima e parâmetros do condutor. O cálculo deste P24 usa coeficientes convectivos simplificados e não foi validado como implementação IEEE 738.
- [IEC 60826:2017](https://webstore.iec.ch/en/publication/33148) — critérios de projeto de linhas aéreas de 45 kV ou superiores com requisitos de carga/resistência baseados em confiabilidade. A IEC informa que a publicação não cobre projeto detalhado de suportes, fundações, condutores ou cadeias de isoladores e requer dados climáticos locais. Nenhuma dessas verificações foi executada aqui.
- ABNT NBR 7270/88 — citada pelo fabricante como padrão do produto CAA. A edição, eventuais revisões e aplicabilidade contratual devem ser confirmadas antes de uma especificação.

## Aplicabilidade e lacunas

Não houve seleção de vento de projeto, classe de confiabilidade, combinação de cargas, isolação, aterramento, curto-circuito, proteção, requisitos de acesso/conexão ou limites de tensão com o proprietário. Dados do fabricante não substituem estudo de clima e geometria local. A avaliação não declara atendimento à IEEE, IEC, ABNT, ONS, concessionária ou qualquer agente.
