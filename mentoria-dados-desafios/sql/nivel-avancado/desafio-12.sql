/*
=========================================================
DESAFIO 12: Crescimento de Vendas (MoM)
=========================================================
Nível: Avançado

Objetivo:
Calcule a receita total por mês e o crescimento/queda percentual 
em relação ao mês anterior (Month-over-Month).

Requisitos:
- Considere apenas pedidos 'paid'.
- Retornar o Mês/Ano (ex: 2023-01), a receita daquele mês, a receita do mês anterior,
  e a variação percentual.
- Usar Window Functions.

Dica Técnica:
1. Extraia o mês/ano com `TO_CHAR(order_date, 'YYYY-MM')`.
2. Agrupe para achar a receita mensal.
3. Use a função `LAG(receita_mensal) OVER (ORDER BY mes)` para trazer o mês anterior.
*/

-- Escreva sua query abaixo:
