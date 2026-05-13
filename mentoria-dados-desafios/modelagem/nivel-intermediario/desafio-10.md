# DESAFIO 10: Views Materializadas

**Nível:** Intermediário

## Objetivo

Otimizar a performance das consultas analíticas transformando as views do desafio anterior em **Materialized Views** (views materializadas) com suporte a `REFRESH MATERIALIZED VIEW CONCURRENTLY`.

## Requisitos

- Transformar as 3 views analíticas (`vw_vendas_por_categoria`, `vw_top_clientes`, `vw_performance_mensal`) em **Materialized Views**.
- Para cada Materialized View, criar um **índice único** que permita o uso de `REFRESH MATERIALIZED VIEW CONCURRENTLY`.
- Escrever um **script de refresh** que atualize todas as Materialized Views de forma concorrente (sem bloquear leituras).
- Garantir que as consultas funcionem exatamente como as views originais, mas com dados persistidos em disco.

## Dica Técnica

Materialized Views exigem um **índice único** para que o `REFRESH CONCURRENTLY` funcione (sem ele o comando falha). O `CONCURRENTLY` permite que a view permaneça disponível para leitura durante a atualização, mas é ligeiramente mais lento que o refresh padrão. Use `CREATE UNIQUE INDEX` na mesma coluna que compõe a chave do GROUP BY mais granular.

## Recursos

- [PostgreSQL CREATE MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- [PostgreSQL REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html)
- Documentação sobre CONCURRENTLY: https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html#SQL-REFRESHMATERIALIZEDVIEW-NOTES

---

## Resolução

```sql
-- Materialized View 1: Vendas por Categoria
CREATE MATERIALIZED VIEW mv_vendas_por_categoria AS
SELECT
    dd.ano,
    dp.categoria                     AS category,
    ROUND(SUM(sf.total_price), 2)    AS total_vendas,
    SUM(sf.quantity)                 AS qtd_itens
FROM sales_fact sf
JOIN dim_product dp ON sf.product_sk = dp.product_sk
JOIN dim_date dd    ON sf.date_sk    = dd.date_sk
GROUP BY dd.ano, dp.categoria
ORDER BY dd.ano, dp.categoria
WITH DATA;

CREATE UNIQUE INDEX uq_mv_vendas_categoria
ON mv_vendas_por_categoria (ano, category);

-- Materialized View 2: Top Clientes
CREATE MATERIALIZED VIEW mv_top_clientes AS
SELECT
    CONCAT(dc.first_name, ' ', dc.last_name) AS cliente,
    ROUND(SUM(sf.total_price), 2)            AS total_gasto,
    COUNT(DISTINCT ...)                      AS total_pedidos
FROM sales_fact sf
JOIN dim_customer dc ON sf.customer_sk = dc.customer_sk
GROUP BY dc.customer_sk, dc.first_name, dc.last_name
ORDER BY total_gasto DESC
WITH DATA;

CREATE UNIQUE INDEX uq_mv_top_clientes
ON mv_top_clientes (cliente);

-- Materialized View 3: Performance Mensal
CREATE MATERIALIZED VIEW mv_performance_mensal AS
SELECT
    dd.ano,
    dd.nome_mes                            AS mes,
    ROUND(SUM(sf.total_price), 2)          AS receita,
    COUNT(DISTINCT ...)                    AS pedidos,
    ROUND(SUM(sf.total_price) / NULLIF(COUNT(DISTINCT ...), 0), 2) AS ticket_medio
FROM sales_fact sf
JOIN dim_date dd ON sf.date_sk = dd.date_sk
GROUP BY dd.ano, dd.mes, dd.nome_mes
ORDER BY dd.ano, dd.mes
WITH DATA;

CREATE UNIQUE INDEX uq_mv_performance_mensal
ON mv_performance_mensal (ano, mes);

-- Script de Refresh Concorrente
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_vendas_por_categoria;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_top_clientes;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_performance_mensal;
```
