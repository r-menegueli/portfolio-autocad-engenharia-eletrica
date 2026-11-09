# Resultados resumidos — P24

Estudo analítico de triagem para uma LT de 138 kV e 30 km; corredor, cargas, terreno, estruturas e condições ambientais são sintéticos. Os CSVs de parâmetros e origem são a referência para valores e hipóteses.

## Matriz elétrica e térmica

- Matriz: 9 pares de P (50/100/140 MW) e fp (0,90/0,95/1,00). Corrente máxima: **650,80 A** no caso 140 MW/fp 0,90.
- No caso de maior corrente: perdas estimadas de **1,627 MW**, tensão de envio de **145,092 kV** e regulação de **5,139%** com 138 kV fixos no terminal receptor.
- Matriz térmica: 9 pares de ambiente (20/40/45 °C) e vento (0/0,61/1 m/s). Ampacidade mínima do feixe duplo: **892,04 A** a 45 °C/vento nulo; margem sobre a corrente máxima: **27,04%**.
- Modelo térmico de equilíbrio estacionário simplificado. Não é execução validada da IEEE 738, capacidade liberada ou rating sazonal/dinâmico.

## Matriz mecânica

- 900 registros: 100 vãos × 3 temperaturas (20/45/75 °C) × 3 ventos assumidos (0/15/30 m/s).
- Flecha vertical máxima no vão de 300 m: **9,046 m** a 75 °C/vento nulo.
- Deslocamento transversal idealizado máximo: **6,55 m** a 75 °C/30 m/s.
- Tração no apoio máxima: **32,76 kN** a 20 °C/30 m/s, 23,45% da carga de ruptura bruta de catálogo.
- Clearance vertical mínimo no perfil sintético: **12,679 m**. O cálculo não desloca o condutor lateralmente sobre terreno 2D e não libera travessias.

## Geometria e verificação

101 estruturas fecham o eixo de 30 km com 100 vãos de 300 m. Ancoragens em 0, 9,9, 20,1 e 30 km. A última estrutura tem vão até a próxima de 0 m.

Quatro testes automatizados Python passaram: fluxo nominal π e balanço de potência; fechamento do comprimento e ancoragens; compatibilidade mecânica/clearance em 900 linhas; equilíbrio térmico e margem em 9 condições. O validador estrutural do portfólio passou com 0 erros e 0 avisos, no seu escopo DXF/PDF/PNG. MATLAB R2026a gravou tabelas numa execução anterior, mas a versão anterior do script falhou ao construir uma colorbar por falta de memória. A versão atual de `run_analysis.m` ainda não foi reexecutada integralmente, e `test_project_24.m` não foi executado no MATLAB. A matriz mecânica atual e os seis PNGs foram gerados pelo fallback Python documentado, não são apresentados como gráficos MATLAB.

## Limitações relevantes

O módulo axial e a expansão térmica são proxies de uma tabela Nexans T-ACSR 26/7 sem equivalência confirmada com o produto CAA Drake. O cálculo de vento não inclui cargas normativas, blowout/clearance lateral sobre perfil 2D, creep, vibração, catenária completa, torres, fundações, curto-circuito, sequência zero, coordenação de isolamento ou estudo de aterramento. A avaliação não declara conformidade normativa nem aptidão para construção/operação. Veja `validacao/relatorio-validacao-tecnica.json`.
