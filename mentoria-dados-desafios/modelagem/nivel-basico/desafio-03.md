/*
=========================================================
DESAFIO 03: Aplicar 2FN
=========================================================
Nível: Básico

Objetivo:
Remover dependências parciais, identificando atributos que
dependem de apenas parte da chave primária composta.

Requisitos:
- Analisar se order_items tem chave composta ou dependências
  parciais.
- Separar categories de products em uma tabela própria.
- Isolar dados geográficos de customers (country, state, city,
  zip_code) se houver dependência parcial.
- Escrever DDL SQL para criar as novas tabelas normalizadas.

Dica Técnica:
2FN exige que todo atributo não-chave dependa da chave primária
COMPLETA. Aplique-se apenas a tabelas com chave composta.

Recursos:
- scripts/ddl/create_tables.sql
- scripts/ddl/constraints.sql
*/

-- DDL para normalização até 2FN

/*
=== ANÁLISE DAS TABELAS ===

1. order_items: chave é order_item_id (simples).
   NÃO há chave composta → 2FN não se aplica diretamente.

2. products: chave é product_id (simples).
   Porém, category depende apenas de product_id.
   category é um atributo que pode se repetir → candidato
   a tabela própria para evitar redundância.

3. customers: chave é customer_id (simples).
   country, state, city, zip_code dependem de customer_id,
   mas poderiam formar uma dimensão de endereço separada.

=== NOVAS TABELAS PROPOSTAS ===
*/

-- Tabela de categorias (separada de products)
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de endereços (separada de customers)
CREATE TABLE IF NOT EXISTS addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    zip_code VARCHAR(20),
    is_main BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela products alterada (referencia category_id)
CREATE TABLE IF NOT EXISTS products_2nf (
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

-- Tabela customers alterada (sem endereço embutido)
CREATE TABLE IF NOT EXISTS customers_2nf (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* === OBSERVAÇÕES ===
- order_items, orders, payments e shipments permanecem iguais.
- products ganha FK para categories.
- customers perde os campos de endereço, que vão para addresses.
- A 2FN é um passo intermediário; a 3FN refinará ainda mais.
*/
