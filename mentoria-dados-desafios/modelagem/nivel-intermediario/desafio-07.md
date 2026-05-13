# DESAFIO 07: Criar Dimensões

**Nível:** Intermediário

## Objetivo

Implementar as **tabelas Dimensão** do Star Schema em SQL DDL, utilizando surrogate keys e desnormalização de atributos para otimizar consultas analíticas.

## Requisitos

- Criar a dimensão **`dim_customer`** com uma surrogate key (`customer_sk`), mantendo os atributos descritivos do cliente (nome, email, cidade, estado, data de cadastro, status).
- Criar a dimensão **`dim_product`** com surrogate key e **categoria desnormalizada** (nome da categoria dentro da própria dimensão, em vez de uma chave estrangeira para uma tabela separada).
- Criar a dimensão **`dim_date`** com pelo menos: `date_sk`, `data_completa`, `ano`, `mes`, `dia`, `trimestre`, `nome_mes`, `dia_da_semana`, `flag_fim_de_semana`.
- Criar a dimensão **`dim_payment_method`** com os métodos de pagamento existentes (credit_card, boleto, pix, etc.).
- Criar a dimensão **`dim_shipment_status`** com os status de envio (pending, shipped, delivered, returned).
- Utilizar `IDENTITY` ou `SERIAL` para as surrogate keys.
- Escrever os comandos `INSERT` para popular todas as dimensões a partir dos dados existentes no modelo 3FN.

## Dica Técnica

Use `IDENTITY` (Postgres 10+) ou `SERIAL` para gerar automaticamente as surrogate keys. Lembre-se de que em Star Schema a desnormalização é intencional — colocar a categoria dentro de `dim_product` evita joins desnecessários em consultas analíticas.

## Recursos

- [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL IDENTITY Columns](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
- Modelo 3FN de origem: `customers`, `products`, `orders`, `order_items`, `payments`, `shipments`

---

## Resolução

```sql
-- Dimensão: dim_customer
CREATE TABLE dim_customer (
    customer_sk   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    email         VARCHAR(100) NOT NULL,
    city          VARCHAR(100),
    state         VARCHAR(50),
    signup_date   DATE,
    status        VARCHAR(20),
    UNIQUE (customer_id)
);

INSERT INTO dim_customer (customer_id, first_name, last_name, email, city, state, signup_date, status)
SELECT customer_id, first_name, last_name, email, city, state, signup_date, status
FROM customers;

-- Dimensão: dim_product
CREATE TABLE dim_product (
    product_sk    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id    INTEGER NOT NULL,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50) NOT NULL,
    unit_price    DECIMAL(10,2),
    UNIQUE (product_id)
);

INSERT INTO dim_product (product_id, product_name, category, unit_price)
SELECT product_id, product_name, category, unit_price
FROM products;

-- Dimensão: dim_date
CREATE TABLE dim_date (
    date_sk          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_completa    DATE NOT NULL UNIQUE,
    ano              SMALLINT NOT NULL,
    mes              SMALLINT NOT NULL,
    dia              SMALLINT NOT NULL,
    trimestre        SMALLINT NOT NULL,
    nome_mes         VARCHAR(20) NOT NULL,
    dia_da_semana    VARCHAR(20) NOT NULL,
    flag_fim_de_semana BOOLEAN NOT NULL
);

INSERT INTO dim_date (data_completa, ano, mes, dia, trimestre, nome_mes, dia_da_semana, flag_fim_de_semana)
SELECT DISTINCT
    o.order_date,
    EXTRACT(YEAR  FROM o.order_date)::SMALLINT,
    EXTRACT(MONTH FROM o.order_date)::SMALLINT,
    EXTRACT(DAY   FROM o.order_date)::SMALLINT,
    EXTRACT(QUARTER FROM o.order_date)::SMALLINT,
    TO_CHAR(o.order_date, 'Month'),
    TO_CHAR(o.order_date, 'Day'),
    EXTRACT(DOW FROM o.order_date) IN (0, 6)
FROM orders o;

-- Dimensão: dim_payment_method
CREATE TABLE dim_payment_method (
    payment_method_sk INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    method_name       VARCHAR(30) NOT NULL UNIQUE,
    method_type       VARCHAR(20)
);

INSERT INTO dim_payment_method (method_name, method_type)
SELECT DISTINCT payment_method, 'credit'
FROM payments;

-- Dimensão: dim_shipment_status
CREATE TABLE dim_shipment_status (
    shipment_status_sk INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status_name        VARCHAR(30) NOT NULL UNIQUE,
    status_description VARCHAR(100)
);

INSERT INTO dim_shipment_status (status_name, status_description)
SELECT DISTINCT status, 'Status de entrega'
FROM shipments;
```
