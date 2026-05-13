/*
=========================================================
DESAFIO 15: Information Mart (Business Vault)
=========================================================
Nível: Avançado

Objetivo:
Construir a camada de consumo (Business Vault) a partir dos Hubs,
Links e Satellites criados nos desafios anteriores, entregando uma
visão dimensional pronta para análise.

Requisitos:
- Criar a view vw_vendas_completa que junta:
    * Link_order_items (base dos fatos)
    * Hub_order + sat_order_detail (dimensão pedido)
    * Hub_customer + sat_customer_detail (dimensão cliente)
    * Hub_product + sat_product_detail (dimensão produto)
- A view deve mostrar apenas os registros vigentes nos Satellites
  (current_flag = 'Y').
- Criar a view vw_vendas_mensal com agregação por mês contendo:
    * ano/mês
    * total de pedidos
    * receita total
    * quantidade de itens vendidos
    * ticket médio

Dica Técnica:
Faça JOINs entre Links e Satellites usando as hash_keys. Filtrar
por current_flag = 'Y' nos Satellites garante que apenas dados
atuais sejam expostos na camada de consumo.

Recursos:
- View vw_vendas_completa (visão detalhada).
- View vw_vendas_mensal (visão agregada por mês).
*/
