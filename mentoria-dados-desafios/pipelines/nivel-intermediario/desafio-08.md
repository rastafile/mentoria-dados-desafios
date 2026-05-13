/*
=========================================================
DESAFIO 08: Upsert / Merge
=========================================================
Nivel: Intermediario

Objetivo:
Implementar um pipeline de upsert que sincroniza dados
atualizados da origem (CSV ou query) para uma tabela de
destino sem duplicar registros. Utilizar a clausula
INSERT ... ON CONFLICT (id) DO UPDATE.

Requisitos:
- Criar uma funcao generica upsert_table() que aceite
  nome da tabela, chave primaria e DataFrame de origem.
- Construir dinamicamente o SQL de merge com
  ON CONFLICT (primary_key) DO UPDATE.
- Comparar as colunas da origem com as do destino para
  decidir quais atualizar.
- Executar o upsert dentro de uma transacao.
- Logar quantos registros foram inseridos vs atualizados.

Dica Tecnica:
Use `df.to_sql()` com if_exists='append' para inserir em
lote, combinado com uma CTE ou tabela temporaria antes
do upsert final. O SQLAlchemy `text()` permite construir
o SQL de merge de forma segura.
*/
