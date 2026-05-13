/*
=========================================================
DESAFIO 04: Aplicar 3FN
=========================================================
Nível: Básico

Objetivo:
Remover dependências transitivas do modelo, garantindo que
todo atributo não-chave dependa exclusivamente da chave
primária.

Requisitos:
- Identificar dependências transitivas em customers
  (cidade → estado → país?).
- Verificar outras tabelas em busca de dependências transitivas.
- Propor nova estrutura separando dimensão geográfica.
- Escrever DDL para criar as tabelas normalizadas.

Dica Técnica:
3FN exige que atributos não-chave dependam apenas da chave
primária, e não de outros atributos não-chave.

Recursos:
- scripts/ddl/create_tables.sql
- scripts/ddl/constraints.sql
*/

-- DDL para normalização até 3FN

/*
=== IDENTIFICAÇÃO DE DEPENDÊNCIAS TRANSITIVAS ===

1. customers (tabela original):
   customer_id → city
   city → state (dependência transitiva: estado depende da cidade)
   state → country (dependência transitiva: país depende do estado)
   Portanto: customer_id → city → state → country
   Isso viola 3FN.

2. products (tabela original):
   product_id → category_id → category_name
   Com a separação da 2FN, a categoria virou FK.
   Agora product_id → category_id (FK), sem transitividade.

3. orders, order_items, payments, shipments:
   Não possuem dependências transitivas identificadas.

=== SOLUÇÃO: DIMENSÃO GEOGRÁFICA ===

Criar tabelas hierárquicas para eliminar as transitividades:
   countries (country_id, name)
   states (state_id, name, country_id)
   cities (city_id, name, state_id)

Assim: address_id → city_id (FK apenas para city).
city_id → state_id → country_id fica na dimensão.
*/

CREATE TABLE IF NOT EXISTS countries (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS states (
    state_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    UNIQUE(name, country_id)
);

CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_id INT NOT NULL,
    zip_code VARCHAR(20),
    UNIQUE(name, state_id, zip_code)
);

-- Tabela addresses refatorada (3FN)
CREATE TABLE IF NOT EXISTS addresses_3nf (
    address_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    city_id INT NOT NULL,
    street VARCHAR(255),
    number VARCHAR(20),
    complement VARCHAR(100),
    is_main BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* === OBSERVAÇÕES ===
- addresses_3nf.city_id referencia cities, eliminando a
  dependência transitiva.
- A sequência de FK é: address → city → state → country.
- Cada nível geográfico é uma entidade independente,
  evitando redundância de nomes de estado/pais.
*/
