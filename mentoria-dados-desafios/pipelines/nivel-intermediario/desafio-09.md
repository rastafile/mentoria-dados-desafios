/*
=========================================================
DESAFIO 09: Validacao Manual de Qualidade de Dados
=========================================================
Nivel: Intermediario

Objetivo:
Implementar validacoes manuais de qualidade de dados
utilizando apenas pandas e SQL, sem bibliotecas externas
de qualidade. O objetivo e entender os tipos de problemas
antes de automatizar com ferramentas como Great Expectations.

Requisitos:
- Verificar nulos em colunas obrigatorias (customer.email,
  product.price, orders.total_amount, order_items.quantity).
- Detectar duplicatas em colunas unique (customer.email).
- Checar consistencia de chaves estrangeiras:
  - orders com customer_id inexistente em customers
  - order_items com order_id ou product_id inexistente
- Validar valores inesperados em colunas de status:
  - orders.status deve estar em {paid, pending, cancelled, refunded}
  - customers.status deve estar em {active, inactive}
- Gerar um relatorio tabular (DataFrame) com os resultados,
  contendo: tabela, validacao, status (PASSOU/FALHOU), detalhes.

Dica Tecnica:
Estruture cada validacao como uma funcao separada que retorna
um dicionario {"tabela": nome, "validacao": descricao,
"status": "PASSOU"|"FALHOU", "detalhes": str}. Ao final,
converta a lista de dicionarios em DataFrame e exporte como CSV.

Recursos:
- pandas.DataFrame para as consultas
- pd.read_sql() para executar queries no banco
- from pipelines.utils.db import get_engine
*/
