# Memorial descritivo — P24

## Objeto

Estudo conceitual de uma linha aérea trifásica de 138 kV, 60 Hz e 30 km, com 100 vãos nominais de 300 m, 101 estruturas sintéticas, terminais em subestações fictícias, torres de suspensão/ancoragem, feixe duplo por fase, dois cabos de guarda conceituais e sistema de aterramento esquemático.

## Arranjo

A configuração de fase é horizontal, com espaçamentos de 7,5 m e altura média de fixação de 22 m. O condutor selecionado como referência de catálogo é CAA 795 kcmil 26/7 Drake Classe A, Nexans ref. 64719. O feixe de dois subconductores a 0,40 m é uma hipótese de estudo. O perfil de terreno e o eixo XY em coordenadas locais são fictícios, interpolados de marcos sintéticos a cada 2 km. As ancoragens são localizadas nas estacas 0+000, 9+900, 20+100 e 30+000.

## Análises

O conjunto inclui fluxo de potência positivo-sequência por modelo nominal π para nove pares de carga/fator de potência, triagem térmica estacionária para nove pares de temperatura ambiente/vento e modelo parabólico compatível de um vão para nove pares de temperatura/vento mecânico em todos os 100 vãos. O cálculo registra flechas vertical, transversal e resultante, tração de apoio e clearance vertical sobre o perfil sintético.

Para os cenários definidos, a corrente máxima é 650,80 A, a margem térmica mínima na triagem simplificada é 27,04% e a flecha vertical máxima no vão de 300 m é 9,046 m. O deslocamento lateral idealizado chega a 6,55 m a 30 m/s. O clearance mínimo de 12,679 m considera apenas o eixo de referência e a componente vertical do condutor; não incorpora a translação lateral no terreno 2D. Os resultados e equações estão em `memoria-calculo.md`.

## Desenhos

São dez pranchas A3 em DXF editável e PDF/SVG/PNG. São desenhos conceituais sem viewport de escala física; carimbos indicam `S/ESC.`. O perfil P24-02 apresenta escalas gráfica horizontal/vertical diferentes e informa exagero vertical de 100×. As dimensões das estruturas, fundações, isoladores, bays e ferragens não são dimensionamentos de fabricação.

## Ferramentas, reprodução e limitações

Os parâmetros numéricos vêm de `portfolio.toml` e são exportados em `dados/parametros.csv`; as fontes e classes de evidência ficam em `dados/origem-parametros.csv`. O MATLAB R2026a gravou tabelas numa execução anterior, mas falhou durante a exportação gráfica por erro de memória. O código foi atualizado depois dessa execução e ainda não passou por uma execução MATLAB completa. A matriz mecânica e os seis gráficos desta revisão foram regenerados pelo fallback Python e verificados por quatro testes automatizados. Os testes MATLAB permanecem implementados, mas não foram concluídos no ambiente por falta de memória disponível. O relatório técnico detalha a diferença entre validador estrutural e verificação numérica.

Não foram obtidos topografia, clima, travessias, servidão, cargas de vento de projeto, dados mecânicos confirmados do cabo, parâmetros completos de torre/fundação, dados de curto-circuito, sequência zero, proteção, coordenação de isolamento, grounding study, licença ou requisitos do agente. A aproximação mecânica não inclui catenária completa, creep, vibração, galope, flecha lateral sobre terreno real ou cargas normativas. A triagem térmica não é uma implementação validada da IEEE 738. Não foi criado nem executado modelo Simulink. Consulte `validacao/relatorio-validacao-tecnica.json`.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação, energização ou operação sem projeto executivo, verificações específicas e responsabilidade profissional habilitada.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
