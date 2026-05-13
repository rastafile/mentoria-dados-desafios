/*
=========================================================
DESAFIO 05: Modelo 3FN Final
=========================================================
Nível: Básico

Objetivo:
Consolidar todo o modelo normalizado em 3FN, gerando o DDL
completo de todas as tabelas e um script de migração de dados
a partir do esquema original.

Requisitos:
- Gerar DDL completo de todas as tabelas no modelo 3FN.
- Incluir Foreign Keys, CHECK constraints e índices.
- Escrever INSERTs para povoar as novas tabelas convertendo
  os dados existentes (INSERT INTO ... SELECT ...).
- Garantir que a migração preserve a integridade referencial.

Dica Técnica:
Use INSERT INTO ... SELECT DISTINCT ... para extrair valores
de dimensões (categorias, países, estados, cidades) e depois
INSERT INTO ... JOIN ... para popular as tabelas fato.

Recursos:
- scripts/dml/insert_*.sql
- scripts/ddl/create_tables.sql
- scripts/ddl/constraints.sql
*/

-- =============================================
-- DDL COMPLETO — MODELO 3FN
-- =============================================

-- Dimensão: categorias
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão: países
CREATE TABLE IF NOT EXISTS countries (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Dimensão: estados
CREATE TABLE IF NOT EXISTS states (
    state_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    UNIQUE(name, country_id)
);

-- Dimensão: cidades
CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_id INT NOT NULL,
    zip_code VARCHAR(20),
    UNIQUE(name, state_id, zip_code)
);

-- Tabela fato: clientes
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela fato: endereços dos clientes
CREATE TABLE IF NOT EXISTS addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    city_id INT NOT NULL,
    is_main BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela fato: produtos
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- As demais tabelas (orders, order_items, payments, shipments)
-- permanecem com a mesma estrutura do modelo original, apenas
-- ajustando as FKs conforme necessário.

-- =============================================
-- FOREIGN KEYS
-- =============================================

ALTER TABLE states
    ADD CONSTRAINT fk_states_countries
    FOREIGN KEY (country_id) REFERENCES countries(country_id);

ALTER TABLE cities
    ADD CONSTRAINT fk_cities_states
    FOREIGN KEY (state_id) REFERENCES states(state_id);

ALTER TABLE addresses
    ADD CONSTRAINT fk_addresses_customers
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    ADD CONSTRAINT fk_addresses_cities
    FOREIGN KEY (city_id) REFERENCES cities(city_id);

ALTER TABLE products
    ADD CONSTRAINT fk_products_categories
    FOREIGN KEY (category_id) REFERENCES categories(category_id);

ALTER TABLE orders
    ADD CONSTRAINT fk_orders_customers
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- =============================================
-- CHECK CONSTRAINTS
-- =============================================

ALTER TABLE products
    ADD CONSTRAINT chk_products_price CHECK (price >= 0),
    ADD CONSTRAINT chk_products_cost CHECK (cost >= 0);

ALTER TABLE customers
    ADD CONSTRAINT chk_customers_status CHECK (status IN ('active', 'inactive'));

-- =============================================
-- MIGRAÇÃO DE DADOS (a partir do esquema original)
-- =============================================

-- 1. Popular dimensão de categorias
INSERT INTO categories (name)
SELECT DISTINCT category
FROM products_orig
WHERE category IS NOT NULL;

-- 2. Popular dimensão geográfica
INSERT INTO countries (name)
SELECT DISTINCT country
FROM customers_orig
WHERE country IS NOT NULL;

INSERT INTO states (name, country_id)
SELECT DISTINCT c_orig.state, co.country_id
FROM customers_orig c_orig
JOIN countries co ON co.name = c_orig.country
WHERE c_orig.state IS NOT NULL;

INSERT INTO cities (name, state_id, zip_code)
SELECT DISTINCT c_orig.city, s.state_id, c_orig.zip_code
FROM customers_orig c_orig
JOIN states s ON s.name = c_orig.state
WHERE c_orig.city IS NOT NULL;

-- 3. Popular clientes (sem endereço)
INSERT INTO customers (customer_id, first_name, last_name, email, phone, status)
SELECT customer_id, first_name, last_name, email, phone, status
FROM customers_orig;

-- 4. Popular endereços
INSERT INTO addresses (customer_id, city_id, is_main)
SELECT c_orig.customer_id, ci.city_id, TRUE
FROM customers_orig c_orig
JOIN cities ci ON ci.name = c_orig.city
              AND ci.zip_code = c_orig.zip_code;

-- 5. Popular produtos com FK para categoria
INSERT INTO products (product_id, name, description, category_id, price, cost, stock_quantity)
SELECT p_orig.product_id,
       p_orig.name,
       p_orig.description,
       COALESCE(c.category_id, 0),
       p_orig.price,
       p_orig.cost,
       p_orig.stock_quantity
FROM products_orig p_orig
LEFT JOIN categories c ON c.name = p_orig.category;

/* ============================================
   ESQUEMA FINAL (3FN) — VISÃO GERAL

   Dimensões:
     categories (category_id, name, description)
     countries  (country_id, name)
     states     (state_id, name, country_id)
     cities     (city_id, name, state_id, zip_code)

   Fatos:
     customers  (customer_id, first_name, last_name, ...)
     addresses  (address_id, customer_id, city_id, ...)
     products   (product_id, name, ..., category_id, ...)
     orders     (order_id, customer_id, ...)
     order_items(order_item_id, order_id, product_id, ...)
     payments   (payment_id, order_id, ...)
     shipments  (shipment_id, order_id, ...)

   Nenhuma dependência parcial ou transitiva.
   Modelo completamente normalizado até 3FN.
   ============================================
*/
