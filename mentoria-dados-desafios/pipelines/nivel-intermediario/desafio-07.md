/*
=========================================================
DESAFIO 07: Particionamento por Data
=========================================================
Nivel: Intermediario

Objetivo:
Criar um pipeline que exporta os dados de order_items
particionados por ano e mes em pastas no estilo Hive:
data/order_items/year=2026/month=05/data.csv.

Requisitos:
- Realizar JOIN entre orders e order_items para obter
  a data do pedido.
- Criar colunas `year` e `month` a partir de order_date.
- Iterar pelos grupos (year, month) e salvar cada grupo
  em um arquivo CSV dentro da estrutura de pastas
  particionada.
- Garantir que as pastas sejam criadas com exist_ok.
- Logar quantos registros foram salvos em cada particao.

Dica Tecnica:
Use `df.groupby(['year', 'month'])` para iterar pelos
grupos. A funcao `os.makedirs(os.path.join(...), exist_ok=True)`
garante a criacao das pastas sem erro se ja existirem.
*/
