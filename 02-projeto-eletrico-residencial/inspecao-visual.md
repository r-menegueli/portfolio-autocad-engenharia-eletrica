# Inspeção visual - Projeto 02

- Data da inspeção: 2026-09-05
- Revisão inspecionada: 00
- Resultado: aprovado após correções

## Método

- os oito PDFs foram rasterizados a 150 dpi com Poppler `pdftoppm` 26.07.0;
- os oito PNGs finais, gerados a 300 dpi, foram comparados com as rasterizações;
- os oito SVGs foram abertos em Chromium e capturados na proporção A3;
- cada prancha foi inspecionada inteira e as regiões densas foram ampliadas;
- os oito DXFs foram abertos e auditados individualmente no AutoCAD 2027.
- o gerador foi executado duas vezes consecutivas e os oito hashes DXF permaneceram
  idênticos entre as execuções.

## Primeira passagem e correções

- Os rótulos completos de ambiente competiam com tags de iluminação e eletrodutos.
  As plantas elétricas passaram a usar nomes simplificados e posições reservadas.
- As larguras das tabelas laterais excediam o painel útil em 18 mm. As colunas foram
  recalculadas para terminar em x = 402 mm, dentro da moldura.
- O arranjo inicial de QD1 totalizava 26 módulos. A reserva foi corrigida para 8 módulos
  livres, fechando 24 módulos: três trilhos de oito.
- A seção de C8 foi elevada para 4 mm². A verificação matemática subsequente também
  elevou C3 para 4 mm²; quedas combinadas conservadoras ficaram em 3,107% e 3,316%.
- O quadro de cargas foi ampliado para ocupar a largura útil e melhorar a leitura.

## Conferência final por prancha

| Prancha | Resultado visual |
| ---: | --- |
| 01/08 | arquitetura, cotas, vãos, quadro de ambientes e carimbo legíveis |
| 02/08 | dez luminárias, oito comandos e circuitos C1/C2 sem colisões |
| 03/08 | TUG, TUE, QD1 e tags C3 a C8 distinguíveis |
| 04/08 | caixas, rotas, DN e pendências técnicas legíveis |
| 05/08 | cadeia MED1-QG1-DR1, DPS1, N/PE e oito saídas legíveis |
| 06/08 | três trilhos, 24 módulos, reservas e barras N/PE coerentes |
| 07/08 | oito linhas, totais, demanda e quedas legíveis em A3 |
| 08/08 | TN-S, equipotencialização e eletrodo indicativo sem cortes |

Não foram observados cortes, desalinhamentos, texto ilegível, diferenças entre PDF/SVG/PNG
ou elementos gráficos fora da moldura na conferência final.
