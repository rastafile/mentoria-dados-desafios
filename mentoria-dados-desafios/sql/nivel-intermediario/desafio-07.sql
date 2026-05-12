/*
=========================================================
DESAFIO 07: Receita Total por Categoria
=========================================================
Nível: Intermediário

Objetivo:
Descubra qual categoria de produtos gerou mais receita (vendas). 
A receita é calculada somando o `total_price` dos itens vendidos 
pertencentes àquela categoria, considerando apenas pedidos pagos ('paid').

Requisitos:
- Tabelas: products, order_items, orders.
- Agrupar por categoria do produto.
- Ordenar pela receita total decrescente.

Dica Técnica:
Você precisará de múltiplos JOINs (orders -> order_items -> products).
*/

-- Escreva sua query abaixo:
