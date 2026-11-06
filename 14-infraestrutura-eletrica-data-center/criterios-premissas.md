# Critérios e premissas — P14

## Valores hipotéticos

| Item | Valor usado | Classificação |
| --- | ---: | --- |
| Carga de TI | 1.000 kW | Premissa didática |
| Climatização e auxiliares | 500 kW | Premissa didática |
| Potência total da instalação | 1.500 kW | Soma das cargas hipotéticas |
| PUE | 1,50 | Hipótese; não medido |
| Fator de potência da instalação | 0,95 | Hipótese para conversão kW/kVA |
| Transformador por caminho | 2.000 kVA | Capacidade nominal ilustrativa |
| Fator de potência de TR | 0,95 | Hipótese para comparação aritmética |
| Gerador por caminho | 2.000 kVA | Capacidade nominal ilustrativa |
| Fator de potência de GE | 0,90 | Hipótese para comparação aritmética |
| UPS por caminho | 5 módulos × 250 kW | Quatro requeridos + um reserva |

## Cálculos conferíveis

- Potência total: `1.000 kW TI + 500 kW suporte = 1.500 kW`.
- PUE ilustrativo: `1.500 kW / 1.000 kW = 1,50`.
- Potência aparente: `1.500 kW / 0,95 = 1.578,95 kVA`, exibida como `1.579 kVA`.
- Capacidade ativa comparativa de cada TR: `2.000 kVA × 0,95 = 1.900 kW`; margem aritmética sobre 1.500 kW: `400 kW`.
- Capacidade ativa comparativa de cada GE: `2.000 kVA × 0,90 = 1.800 kW`; margem aritmética: `300 kW`.
- Capacidade UPS instalada por caminho: `5 × 250 kW = 1.250 kW`; com um módulo reserva, capacidade requerida: `4 × 250 kW = 1.000 kW`.
- Em um evento de perda de caminho, a UPS remanescente deve sustentar a carga integral de TI assumida (1.000 kW); nessa hipótese, a margem modular fica em zero.

As comparações de TR e GE consideram apenas kW/kVA e fator de potência. Não incluem fator de demanda, corrente de magnetização, partida de cargas, derating, temperatura, altitude, harmônicos, eficiência, desequilíbrio, impedância, transientes ou critérios do fabricante.

## Critérios de representação

- Manter visualmente separados os caminhos A e B e marcar a terminação dupla da carga de TI.
- Indicar o módulo UPS reserva como N+1, sem alegar que toda a instalação atende a disponibilidade ou classificação de qualquer norma.
- Separar potência de TI, cargas de suporte e potência total da instalação.
- Tratar fontes MT A/B e segregação física como itens a confirmar; não chamar os caminhos de independentes até verificar todas as causas comuns.
- Não converter potência aparente em corrente, cabos ou ajustes de proteção sem dados de engenharia.

## Dados ainda necessários

Local e concessionária; tensão, curto-circuito e regime de aterramento; topologia e independência das alimentações; perfil e fator de potência das cargas; cargas de resfriamento e partida; equipamento e derating de TR/GE/UPS; autonomia e tecnologia das baterias; combustível e emissões; esquema de aterramento; cabos e rotas; proteção e coordenação; harmônicos e qualidade de energia; sistema de transferência; estratégia de manutenção; incêndio, ventilação, acústica, contenção, acesso e requisitos de operação.
