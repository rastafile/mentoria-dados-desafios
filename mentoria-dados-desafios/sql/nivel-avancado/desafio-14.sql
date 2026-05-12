/*
=========================================================
DESAFIO 14: Running Total (Soma Acumulada)
=========================================================
Nível: Avançado

Objetivo:
Calcule a soma acumulada da receita de vendas ao longo dos dias.
Isso ajuda a visualizar como a receita vai subindo dia após dia.

Requisitos:
- Apenas pedidos pagos ('paid').
- Retornar: dia (YYYY-MM-DD), receita do dia, e receita acumulada até aquele dia.
- Ordenar por data.

Dica Técnica:
A função de janela `SUM(receita_do_dia) OVER (ORDER BY dia)` 
produzirá o Running Total automaticamente.
*/

-- Escreva sua query abaixo:
