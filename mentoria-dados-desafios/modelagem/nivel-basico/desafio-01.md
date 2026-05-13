/*
=========================================================
DESAFIO 01: Mapear Esquema Atual
=========================================================
Nível: Básico

Objetivo:
Desenhar o DER (Diagrama Entidade-Relacionamento) conceitual
das 6 tabelas do banco de dados, identificando entidades,
atributos, chaves e relacionamentos.

Requisitos:
- Identificar todas as Primary Keys (PKs) de cada tabela.
- Identificar todas as Foreign Keys (FKs) e suas referências.
- Descrever os relacionamentos entre as tabelas (1:N, N:N).
- Listar as cardinalidades mínima e máxima de cada lado.
- Criar uma representação textual do esquema com campos e tipos.

Dica Técnica:
Analise os arquivos `scripts/ddl/create_tables.sql` e
`scripts/ddl/constraints.sql` para extrair PKs, FKs,
tipos de dados e constraints de cada tabela.

Recursos:
- scripts/ddl/create_tables.sql
- scripts/ddl/constraints.sql
*/

-- Representação textual do esquema atual (preencha abaixo)

/*
=== TABELAS E CAMPOS ===

1. customers (customer_id SERIAL PK)


2. products (product_id SERIAL PK)


3. orders (order_id SERIAL PK)


4. order_items (order_item_id SERIAL PK)


5. payments (payment_id SERIAL PK)


6. shipments (shipment_id SERIAL PK)


=== RELACIONAMENTOS ===

customers ──── orders


orders ──── order_items


products ──── order_items


orders ──── payments


orders ──── shipments


=== OBSERVAÇÕES ===

*/
