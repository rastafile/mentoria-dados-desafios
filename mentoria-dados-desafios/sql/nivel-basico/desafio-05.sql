/*
=========================================================
DESAFIO 05: Faturamento Diário
=========================================================
Nível: Básico

Objetivo:
Calcule a soma total dos pedidos (total_amount) para cada dia.
Apenas considere pedidos com status 'paid'.

Requisitos:
- Extrair apenas a data (sem a hora) da coluna order_date.
- Agrupar pela data e somar o total_amount.
- Filtrar status = 'paid'.
- Ordenar da data mais recente para a mais antiga.

Dica Técnica:
Use CAST(order_date AS DATE) ou a função DATE() no PostgreSQL para remover a hora.
*/

-- Escreva sua query abaixo:
