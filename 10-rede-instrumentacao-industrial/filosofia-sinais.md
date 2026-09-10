# Filosofia de sinais — P10

## Separação conceitual

| Natureza | O que transporta | Representação | Destino típico | Exemplo P10 |
| --- | --- | --- | --- | --- |
| alimentação | energia elétrica | 24 Vcc, corrente disponível e proteção | equipamento ou remota | P24-201 alimenta RIO-201 |
| sinal analógico | valor contínuo de processo | corrente de 4 a 20 mA | canal AI | C-101 leva TT-101 a AI0 |
| sinal digital | estado discreto | 0/1 em 24 Vcc | canal DI | C-105 leva LSH-105 a DI0 |
| comunicação | quadros, variáveis e diagnósticos | Ethernet entre nós endereçados | porta de rede | NET-102 interliga SW-101 e RIO-201 |

O fato de um transmissor de dois fios usar energia e informação no mesmo par não
transforma toda a distribuição 24 Vcc em sinal analógico. A fonte estabelece a energia
da malha; a corrente controlada pelo transmissor codifica a variável. Por outro lado,
uma entrada digital não representa valores intermediários e a comunicação não é uma
coleção de contatos físicos: ela depende de interfaces, endereçamento, protocolo e
tratamento de falhas.

## Convenções operacionais

- AI-001 a AI-004 são escalados linearmente a partir de 4–20 mA.
- DI-001 e DI-002 apresentam somente estado elétrico; a lógica ativa/inativa final
  depende do sensor selecionado e da análise de falha segura.
- O SCADA apresenta e registra dados, mas não é camada de proteção.
- PLC-101 executa controle normal; nenhuma função de segurança é atribuída.
- Perda de rede, perda de I/O, valor inválido e falha de alimentação precisam de uma
  matriz de causas e efeitos em uma etapa executiva.

## Blindagem e referência

Os pares analógicos têm blindagem terminada em BE-101 apenas no painel nesta revisão.
A extremidade de campo deve ser isolada. PE-101 protege carcaças e estabelece
equipotencialização; 0 V fecha circuitos funcionais; BE-101 recebe shields. A ligação
entre BE-101 e PE-101 é explícita e pontual no conceito. A implementação real deve ser
revista considerando frequências, topologia de bonding, fabricantes e EMC do conjunto.
