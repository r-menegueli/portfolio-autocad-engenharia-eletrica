# Memorial descritivo — P17

## Objetivo

Registrar, em pranchas editáveis A3, uma arquitetura conceitual de automação digital para uma subestação. O estudo enfatiza a associação de bays, IEDs e MUs, a separação lógica entre rede de processo e rede de estação, e a rastreabilidade de sinais e verificações.

## Arranjo ilustrativo

O contexto elétrico considera duas linhas de 138 kV, barra A, transformador hipotético de 25 MVA e relação 138/13,8 kV, barra B de 13,8 kV e dois alimentadores. Esses dados servem para localizar as funções de proteção e controle; não definem uma subestação real.

As funções são agrupadas em IEDs de proteção de linha, transformador, barras e alimentadores, com IEDs de controle de bay representados separadamente. Unidades MU recebem grandezas de TC/TP e publicam amostras conceituais na rede de processo. Os IEDs de proteção consomem SV; eventos GOOSE ilustram troca entre IEDs para indicação de trip, falha de disjuntor e permissivo. Saídas finais para bobinas e circuitos de trip dependem de projeto aprovado. A rede de estação apresenta MMS para supervisão e controle, além de HMI, gateway, estação de engenharia e referência de tempo.

## Engenharia de configuração

O fluxo documental é representado por ICD (capacidade do IED), SSD (descrição de requisitos do sistema), SCD (descrição integrada da subestação) e CID (configuração associada a um IED). O fluxo é apenas didático: arquivos, namespaces, capacidades, datasets, assinaturas e regras dependem das ferramentas e declarações dos fabricantes e do projeto aprovado.

## Responsabilidade e limitações

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Este documento não fornece ajustes, lógica executável, circuitos de trip, arquitetura de rede validada, critérios de disponibilidade ou cibersegurança. Não foram produzidos nem validados arquivos SCL, nem executados testes de interoperabilidade, FAT, SAT ou ensaios em IEDs. O projeto não deve controlar ou proteger equipamento real.
