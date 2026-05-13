/*
=========================================================
DESAFIO 12: SCD Tipo 2 (Histórico)
=========================================================
Nível: Avançado

Objetivo:
Implementar SCD Tipo 2 na dimensão product_dim, preservando o
histórico completo de mudanças nos atributos do produto.

Requisitos:
- Adicionar as colunas valid_from, valid_to, current_flag e version
  à tabela product_dim.
- Criar a procedure sp_upsert_product_dim_scd2 que:
    * Fecha o registro anterior (valid_to = CURRENT_DATE,
      current_flag = 'N') quando um atributo relevante mudar.
    * Abre um novo registro com version incrementada, valid_from =
      CURRENT_DATE, valid_to = NULL, current_flag = 'Y'.
- Demonstrar uma consulta histórica que mostre a evolução de um
  produto ao longo do tempo.

Dica Técnica:
current_flag = 'Y' indica o registro vigente; valid_to = NULL
significa que o registro é o atual (ainda não foi substituído).

Recursos:
- DDL alterado da product_dim com as colunas SCD2.
- Procedure sp_upsert_product_dim_scd2.
- Consulta histórica com ORDER BY version.
*/
