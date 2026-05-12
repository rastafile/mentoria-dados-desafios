/*
=========================================================
DESAFIO 13: Tempo de Entrega
=========================================================
Nível: Avançado

Objetivo:
Descubra a média de tempo, em dias, que leva da data 
do pedido (order_date) até a data de entrega (delivery_date).
Agrupe esse resultado por país do cliente.

Requisitos:
- Tabelas: orders, shipments, customers.
- Apenas considere os envios com status 'delivered'.
- Calcular a diferença em dias.

Dica Técnica:
No PostgreSQL, ao subtrair duas datas TIMESTAMP, você obtém um `interval`.
Para extrair apenas os dias do `interval`, use `EXTRACT(DAY FROM data_final - data_inicial)`.
*/

-- Escreva sua query abaixo:
