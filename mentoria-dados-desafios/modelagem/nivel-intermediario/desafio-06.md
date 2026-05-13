# DESAFIO 06: Desenhar Star Schema

**Nível:** Intermediário

## Objetivo

A partir do modelo normalizado (3FN) composto por 6 tabelas (`customers`, `products`, `orders`, `order_items`, `payments`, `shipments`), desenhar um modelo dimensional **Star Schema** que permita consultas analíticas eficientes sobre vendas, clientes e produtos.

## Requisitos

- Identificar qual(is) tabela(s) do modelo 3FN devem se tornar a **tabela Fato** (eventos que geram métricas).
- Identificar quais entidades devem se tornar **Dimensões** (tabelas descritivas que contextualizam os fatos).
- Propor a **granularidade** da tabela Fato (o que cada linha representa).
- Listar todas as **dimensões propostas** com seus principais atributos.
- Justificar cada decisão de modelagem (por que algo virou Fato vs. Dimensão).

## Dica Técnica

Geralmente as tabelas `orders` + `order_items` se combinam para formar a **Fato** (cada item de pedido vira uma linha). `customers`, `products` e datas viram **Dimensões**. Pagamentos e envios podem ser dimensões separadas ou englobadas na Fato, dependendo da granularidade desejada.

## Recursos

- [Modelagem Dimensional (Kimball)](https://www.kimballgroup.com/data-warehouse-bus-archive/)
- Esquema relacional de origem: `customers`, `products`, `orders`, `order_items`, `payments`, `shipments`
- Documentação PostgreSQL sobre modelagem: https://www.postgresql.org/docs/current/ddl.html

---

## Resolução

Descreva abaixo o Star Schema escolhido, listando:

1. **Tabela Fato** — nome, granularidade e métricas.
2. **Tabelas Dimensão** — nome, surrogate key, principais atributos descritivos.
3. **Justificativas** — explique por que cada elemento foi classificado como Fato ou Dimensão.

```sql
-- Exemplo de rascunho organizacional (não executável):
-- Fato:      sales_fact (1 linha por item de pedido)
-- Dimensões: dim_customer, dim_product, dim_date,
--            dim_payment_method, dim_shipment_status
```
