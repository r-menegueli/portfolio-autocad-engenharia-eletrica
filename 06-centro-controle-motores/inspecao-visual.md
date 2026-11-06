# Inspeção visual e geométrica — Projeto 06

> Projeto acadêmico e conceitual. Esta inspeção não libera fabricação, instalação ou operação.

## Revisão 03

O conjunto contém nove pranchas A3. As nove foram regeneradas na revisão gráfica 03;
revisei o contato atualizado para numeração, carimbos e composição geral. A inspeção
ampliada desta revisão foi feita na nova P06-09.

| Prancha | Conferência | Resultado observado |
| :---: | :--- | :--- |
| 01–08 | Folha de contato das nove pranchas | Numeração 01/09–08/09, carimbos da revisão 03 e margens sem cortes evidentes. O contato não substitui releitura detalhada dessas folhas. |
| 09 | PNG de produção e PDF rasterizado a 150 dpi | Tabela de oito colunas, barras instaladas/demandadas, relação do alimentador, notas e carimbo legíveis; sem cortes ou colisões visíveis. |

O PNG P06-09 foi gerado a 300 dpi. O PDF foi rasterizado pelo Poppler a 150 dpi.
O contato das nove folhas está em
`work/revisao-portfolio/contatos/06-centro-controle-motores.png`.

## Conferências estruturais e limites

- O validador específico passou em 864 verificações; o portfólio estrito passou em
  561.440 verificações, ambos sem erros ou avisos.
- O AutoCAD AcCoreConsole 2027 abriu e auditou 9/9 DXFs.
- A tabela P06-09 confere com `lista-cargas.csv`: 18,184584 kW e 20,893255 kVA
  instalados; 16,645368 kW e 19,133709 kVA demandados. W600 indica 29,070663 A,
  50 A de disjuntor e Iz de 57 A assumida. A relação aritmética `Ib <= In <= Iz` não
  substitui verificações de instalação, capacidade térmica, curto-circuito ou
  coordenação.
- Fatores de demanda, proteção e Iz são premissas. Não foi verificada simultaneidade
  real, seletividade ou adequação a uma instalação física.
- A inspeção visual de SVGs no navegador aguarda autorização do usuário.
- Não declaro conformidade normativa, segurança funcional ou funcionamento em hardware real.
