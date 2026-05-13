# DESAFIO 09: Views Analíticas

**Nível:** Intermediário

## Objetivo

Criar **views de negócio** sobre o Star Schema construído nos desafios anteriores, facilitando o consumo dos dados por ferramentas de BI e relatórios.

## Requisitos

Criar as seguintes views:

1. **`vw_vendas_por_categoria`** — Exibir `ano`, `categoria`, `total_vendas` (soma de `total_price`), `qtd_itens` (soma de `quantity`), ordenado por ano e categoria.
2. **`vw_top_clientes`** — Exibir `cliente` (nome completo), `total_gasto`, `total_pedidos` (pedidos distintos), ordenado do maior gastador para o menor.
3. **`vw_performance_mensal`** — Exibir `ano`, `mes`, `receita` (soma `total_price`), `pedidos` (pedidos distintos), `ticket_medio` (receita / pedidos), ordenado por ano e mês.

## Dica Técnica

Utilize `GROUP BY` e `JOIN`s entre a tabela Fato e as dimensões. Lembre-se que `total_pedidos` exige `COUNT(DISTINCT ...)` sobre o identificador do pedido (que está na Fato). Neste modelo, como a granularidade da Fato é por item, você pode incluir uma chave do pedido na Fato ou fazer a contagem distinta a partir do `sale_sk` agrupado por cliente em uma subconsulta.

## Recursos

- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- Esquema Star Schema: `sales_fact` + `dim_customer`, `dim_product`, `dim_date`, `dim_payment_method`, `dim_shipment_status`

---

## Resolução

```sql
-- View 1: Vendas por Categoria
CREATE VIEW vw_vendas_por_categoria AS
SELECT
    dd.ano,
    dp.categoria                     AS category,
    ROUND(SUM(sf.total_price), 2)    AS total_vendas,
    SUM(sf.quantity)                 AS qtd_itens
FROM sales_fact sf
JOIN dim_product dp ON sf.product_sk = dp.product_sk
JOIN dim_date dd    ON sf.date_sk    = dd.date_sk
GROUP BY dd.ano, dp.categoria
ORDER BY dd.ano, dp.categoria;

-- View 2: Top Clientes
CREATE VIEW vw_top_clientes AS
SELECT
    CONCAT(dc.first_name, ' ', dc.last_name) AS cliente,
    ROUND(SUM(sf.total_price), 2)            AS total_gasto,
    COUNT(DISTINCT ...)                      AS total_pedidos
FROM sales_fact sf
JOIN dim_customer dc ON sf.customer_sk = dc.customer_sk
GROUP BY dc.customer_sk, dc.first_name, dc.last_name
ORDER BY total_gasto DESC;

-- Observação: para COUNT(DISTINCT pedido), será necessário incluir
-- o order_id na sales_fact ou utilizar outra estratégia de agregação.

-- View 3: Performance Mensal
CREATE VIEW vw_performance_mensal AS
SELECT
    dd.ano,
    dd.nome_mes                            AS mes,
    ROUND(SUM(sf.total_price), 2)          AS receita,
    COUNT(DISTINCT ...)                    AS pedidos,
    ROUND(SUM(sf.total_price) / NULLIF(COUNT(DISTINCT ...), 0), 2) AS ticket_medio
FROM sales_fact sf
JOIN dim_date dd ON sf.date_sk = dd.date_sk
GROUP BY dd.ano, dd.mes, dd.nome_mes
ORDER BY dd.ano, dd.mes;
```
