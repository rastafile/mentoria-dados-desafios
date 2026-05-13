/*
=========================================================
DESAFIO 03: Importar CSV para o Banco
=========================================================
Nivel: Basico

Objetivo:
Ler arquivos CSV do diretorio datasets/ e inserir os dados
no banco PostgreSQL utilizando df.to_sql.

Requisitos:
- Listar os arquivos CSV disponiveis em datasets/.
- Para cada CSV, ler com pd.read_csv e inserir no banco
  com df.to_sql(if_exists='replace', index=False).
- Exibir mensagens de progresso para cada tabela importada.
- Tratar possiveis erros com try/except.

Dica Tecnica:
Use df.to_sql(nome_tabela, engine, if_exists='replace',
index=False) para sobrescrever a tabela no banco. O nome
da tabela pode ser extraido do nome do arquivo.
*/
