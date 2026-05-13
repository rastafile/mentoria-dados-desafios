/*
=========================================================
DESAFIO 13: Data Vault — Hubs
=========================================================
Nível: Avançado

Objetivo:
Iniciar a modelagem Data Vault criando os Hubs que armazenam as
chaves de negócio (business keys) do sistema transacional.

Requisitos:
- Criar o hub_customer com:
    * hash_key (MD5 ou SERIAL) como PK
    * customer_id (business key original)
    * load_date (data de carga)
    * record_source (origem do registro)
- Criar o hub_product com:
    * hash_key como PK
    * product_id (business key original)
    * load_date, record_source
- Criar o hub_order com:
    * hash_key como PK
    * order_id (business key original)
    * load_date, record_source
- Os Hubs devem ser populados a partir das tabelas transacionais
  (customers, products, orders).

Dica Técnica:
Hubs armazenam apenas as chaves de negócio — nenhum atributo
descritivo. A hash_key pode ser gerada com md5(business_key::text)
ou identity sequence.

Recursos:
- DDL dos 3 Hubs.
- INSERTs para popular cada Hub a partir dos dados transacionais.
*/
