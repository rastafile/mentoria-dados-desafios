/*
=========================================================
DESAFIO 15: Detecção de Possível Fraude
=========================================================
Nível: Avançado

Objetivo:
O time de Risco e Fraude precisa de uma query que alerte sobre 
possíveis fraudes com cartões de crédito.

Identifique pedidos que:
1. O método de pagamento seja 'credit_card'.
2. O total do pedido seja maior que 3.000,00.
3. O status do pagamento seja 'failed'.

Além de retornar as informações do pedido (id, valor, data) e 
cliente (id, email), retorne também quantos pagamentos 'failed'
este cliente já teve no histórico total dele.

Requisitos:
- Utilizar Subqueries ou CTEs para contar o histórico do cliente.
- Retornar: order_id, customer_id, email, total_amount, qtd_falhas_cliente.
- Ordenar pelo total_amount decrescente.

Dica Técnica:
Você pode usar uma Subquery correlacionada no SELECT ou uma CTE com GROUP BY.
*/

-- Escreva sua query abaixo:
