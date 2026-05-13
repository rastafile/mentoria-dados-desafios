# DESAFIO 08: Criar Tabela Fato

**Nível:** Intermediário

## Objetivo

Criar a **tabela Fato** (`sales_fact`) do Star Schema, conectando as dimensões através de chaves estrangeiras e armazenando as métricas de negócio no menor nível de granularidade possível.

## Requisitos

- Criar a tabela `sales_fact` contendo **chaves estrangeiras** para todas as dimensões criadas no desafio anterior:
  - `customer_sk` → `dim_customer`
  - `product_sk` → `dim_product`
  - `date_sk` → `dim_date`
  - `payment_method_sk` → `dim_payment_method`
  - `shipment_status_sk` → `dim_shipment_status`
- Incluir as seguintes **métricas**: `quantity`, `unit_price`, `total_price`, `discount`.
- Definir uma **chave primária** composta ou uma surrogate key para a Fato.
- Escrever o comando `INSERT ... SELECT` que popula a `sales_fact` a partir das tabelas transacionais (`orders`, `order_items`, `payments`, `shipments`) fazendo os joins necessários para resolver as surrogate keys nas dimensões.

## Dica Técnica

A Fato deve estar no **menor grau de granularidade** — cada linha representa um item de um pedido (`order_item`). Para popular as surrogate keys, faça JOIN com as tabelas dimensão usando as chaves naturais (ex: `customers.customer_id = dim_customer.customer_id`). Lembre-se de tratar pedidos sem pagamento ou sem envio com `LEFT JOIN`.

## Recursos

- [PostgreSQL FOREIGN KEY](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [PostgreSQL INSERT ... SELECT](https://www.postgresql.org/docs/current/sql-insert.html)
- [Modelagem Dimensional — Tabela Fato](https://www.kimballgroup.com/2012/02/design-tip-149-defining-the-grained-fact-table/)

---

## Resolução

```sql
-- Tabela Fato: sales_fact
CREATE TABLE sales_fact (
    sale_sk            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_sk        INTEGER NOT NULL,
    product_sk         INTEGER NOT NULL,
    date_sk            INTEGER NOT NULL,
    payment_method_sk  INTEGER,
    shipment_status_sk INTEGER,
    quantity           INTEGER NOT NULL,
    unit_price         DECIMAL(10,2) NOT NULL,
    total_price        DECIMAL(10,2) NOT NULL,
    discount           DECIMAL(10,2) DEFAULT 0,

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_sk) REFERENCES dim_customer (customer_sk),
    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_sk) REFERENCES dim_product (product_sk),
    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_sk) REFERENCES dim_date (date_sk),
    CONSTRAINT fk_sales_payment_method
        FOREIGN KEY (payment_method_sk) REFERENCES dim_payment_method (payment_method_sk),
    CONSTRAINT fk_sales_shipment_status
        FOREIGN KEY (shipment_status_sk) REFERENCES dim_shipment_status (shipment_status_sk)
);

-- Popular a Fato a partir do modelo transacional
INSERT INTO sales_fact (
    customer_sk,
    product_sk,
    date_sk,
    payment_method_sk,
    shipment_status_sk,
    quantity,
    unit_price,
    total_price,
    discount
)
SELECT
    dc.customer_sk,
    dp.product_sk,
    dd.date_sk,
    dpm.payment_method_sk,
    dss.shipment_status_sk,
    oi.quantity,
    oi.unit_price,
    oi.total_price,
    COALESCE(oi.discount, 0)
FROM order_items oi
JOIN orders o       ON oi.order_id = o.order_id
JOIN dim_customer dc ON o.customer_id = dc.customer_id
JOIN dim_product dp  ON oi.product_id = dp.product_id
JOIN dim_date dd     ON o.order_date = dd.data_completa
LEFT JOIN payments p       ON o.order_id = p.order_id
LEFT JOIN dim_payment_method dpm ON p.payment_method = dpm.method_name
LEFT JOIN shipments s      ON o.order_id = s.order_id
LEFT JOIN dim_shipment_status dss ON s.status = dss.status_name;
```
