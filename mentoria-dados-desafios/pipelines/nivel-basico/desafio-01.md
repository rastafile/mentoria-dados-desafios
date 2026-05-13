/*
=========================================================
DESAFIO 01: Conectar e Extrair Dados
=========================================================
Nivel: Basico

Objetivo:
Conectar ao banco PostgreSQL via SQLAlchemy e extrair a tabela
customers para um DataFrame. Exibir as primeiras linhas e
informacoes estruturais do DataFrame.

Requisitos:
- Usar SQLAlchemy para conectar ao banco 'mentoria_dados'.
- Executar uma consulta SELECT * FROM customers.
- Carregar o resultado em um pandas DataFrame.
- Exibir as 5 primeiras linhas com df.head().
- Exibir informacoes do DataFrame com df.info().

Dica Tecnica:
Utilize pd.read_sql(query, engine) para carregar os dados
diretamente do banco para um DataFrame. O engine pode ser
obtido de pipelines.utils.db ou criado diretamente com
create_engine.
*/
