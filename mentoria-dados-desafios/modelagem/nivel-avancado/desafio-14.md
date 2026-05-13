/*
=========================================================
DESAFIO 14: Data Vault — Links e Satellites
=========================================================
Nível: Avançado

Objetivo:
Criar os Links (associações entre Hubs) e os Satellites (atributos
descritivos de cada Hub) para completar a modelagem Data Vault.

Requisitos:
- Criar o link_order_customer com as hash_keys dos Hubs order e
  customer, mais load_date e record_source.
- Criar o link_order_items com as hash_keys dos Hubs order e product,
  mais load_date e record_source, quantidade e preço.
- Criar os Satellites para atributos descritivos de cada Hub:
    * sat_customer_detail (first_name, last_name, email, phone, etc.)
    * sat_product_detail (product_name, category, price, etc.)
    * sat_order_detail (order_date, status, total_amount, etc.)
- Cada Satellite deve ter hash_key, valid_from, valid_to, current_flag
  e os atributos descritivos.
- Popular as tabelas a partir dos dados transacionais originais.

Dica Técnica:
Links representam associações muitos-para-muitos entre Hubs e não
possuem atributos descritivos (exceto métricas no caso de Link com
detalhes). Satellites armazenam os atributos descritivos e suportam
histórico (SCD2).

Recursos:
- DDL dos Links (link_order_customer, link_order_items).
- DDL dos Satellites (sat_customer_detail, sat_product_detail,
  sat_order_detail).
- INSERTs para popular Links e Satellites.
*/
