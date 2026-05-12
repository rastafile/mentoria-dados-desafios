/*
=========================================================
DESAFIO 11: Top 3 Clientes por País (Window Function)
=========================================================
Nível: Avançado

Objetivo:
Descubra quem são os 3 clientes que mais gastaram (total pago)
em cada país. Apenas considere pedidos com status 'paid'.

Requisitos:
- Tabelas: customers, orders.
- Utilizar funções de janelamento (Window Functions).
- Retornar: country, customer_id, nome completo, gasto total, e o rank (1, 2 ou 3).

Dica Técnica:
Use `DENSE_RANK()` particionando pelo país e ordenando pelo gasto total decrescente
dentro de uma CTE (Common Table Expression), e então filtre os ranks <= 3.
*/

-- Escreva sua query abaixo:
