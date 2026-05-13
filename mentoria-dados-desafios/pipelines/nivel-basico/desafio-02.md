/*
=========================================================
DESAFIO 02: Exportar Tabelas para CSV
=========================================================
Nivel: Basico

Objetivo:
Pipeline que exporta todas as 6 tabelas do banco de dados
PostgreSQL para arquivos CSV no diretorio datasets/.

Requisitos:
- Conectar ao banco e listar as tabelas: customers, products,
  orders, order_items, payments, shipments.
- Para cada tabela, executar SELECT * e salvar como CSV.
- Utilizar df.to_csv(index=False) para exportacao.
- Exibir mensagem de status para cada exportacao.

Dica Tecnica:
Itere sobre uma lista de nomes de tabelas e use pd.read_sql
dentro do loop. Salve cada CSV em datasets/<tabela>.csv
usando os.path.join para o caminho.
*/
