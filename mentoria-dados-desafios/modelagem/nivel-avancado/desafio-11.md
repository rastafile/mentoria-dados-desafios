/*
=========================================================
DESAFIO 11: SCD Tipo 1 (Sobrescrita)
=========================================================
Nível: Avançado

Objetivo:
Implementar SCD Tipo 1 na dimensão customer_dim, sobrescrevendo
atributos sem manter histórico.

Requisitos:
- Alterar a tabela customer_dim para que ela possa receber upserts.
- Criar uma stored procedure sp_upsert_customer_dim que receba dados
  atualizados do cliente (phone, address, city, state, zip_code) e
  faça upsert (INSERT ou UPDATE conforme o registro exista ou não).
- Demonstrar o funcionamento com um exemplo prático de UPDATE no
  telefone e endereço de um cliente existente.

Dica Técnica:
SCD Tipo 1 não mantém histórico — o valor antigo é simplesmente
sobrescrito. Use INSERT ... ON CONFLICT (customer_id) DO UPDATE.

Recursos:
- Escrever a definição da tabela customer_dim (DDL).
- Escrever a procedure sp_upsert_customer_dim.
- Escrever um bloco anônimo (DO) ou chamada CALL exemplificando o uso.
*/
