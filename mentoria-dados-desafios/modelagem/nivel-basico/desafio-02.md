/*
=========================================================
DESAFIO 02: Identificar Violações de 1FN
=========================================================
Nível: Básico

Objetivo:
Analisar cada tabela do esquema atual e identificar possíveis
violações da Primeira Forma Normal (1FN).

Requisitos:
- Verificar se existem atributos multivalorados em alguma tabela.
- Verificar se existem atributos compostos (divisíveis).
- Verificar se existe repetição de grupos ou arrays.
- Listar cada tabela e dizer se viola ou não a 1FN, justificando.

Dica Técnica:
1FN exige que todos os atributos sejam atômicos (indivisíveis)
e que não existam grupos repetitivos de colunas.

Recursos:
- scripts/ddl/create_tables.sql (definição das tabelas)
- Documentação sobre 1FN (Codd, 1970)
*/

-- Análise de violações da 1FN

/*
=== 1. customers ===
- NÃO viola 1FN.
- Todos os atributos são atômicos (first_name, last_name, email,
  phone, country, state, city, zip_code, status).
- Os campos de endereço (country, state, city, zip_code) são
  atributos simples separados, não um campo composto único.
- Nenhum atributo armazena múltiplos valores (lista, array, JSON).

=== 2. products ===
- NÃO viola 1FN.
- Atributos atômicos: name, description, category, price, cost,
  stock_quantity.
- category é um único valor VARCHAR, não uma lista de categorias.
- description pode ser longa, mas é atômica (texto indivisível).

=== 3. orders ===
- NÃO viola 1FN.
- Atributos atômicos: customer_id, order_date, status, total_amount.
- Nenhum grupo repetitivo de colunas.

=== 4. order_items ===
- NÃO viola 1FN.
- Atributos atômicos: order_id, product_id, quantity, unit_price,
  total_price.
- Cada linha representa exatamente um item de pedido; não há
  armazenamento de múltiplos produtos em uma única linha.

=== 5. payments ===
- NÃO viola 1FN.
- Atributos atômicos: order_id, payment_method, payment_date,
  amount, status.

=== 6. shipments ===
- NÃO viola 1FN.
- Atributos atômicos: order_id, tracking_number, shipment_date,
  delivery_date, status.

=== CONCLUSÃO ===
O esquema atual já respeita a 1FN. Todas as colunas são
atômicas e não há grupos repetitivos. As violações de
normalização aparecerão ao analisar 2FN e 3FN.
*/
