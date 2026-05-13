/*
=========================================================
DESAFIO 06: Carga Incremental por Watermark
=========================================================
Nivel: Intermediario

Objetivo:
Implementar um pipeline que extrai apenas os registros
atualizados desde a ultima execucao, utilizando uma tabela
de controle `pipeline_metadata` para armazenar o timestamp
da ultima execucao (watermark).

Requisitos:
- Criar a tabela de controle `pipeline_metadata` com ao
  menos as colunas: pipeline_name, last_run.
- Verificar se ja existe um last_run registrado; caso
  contrario, usar uma data default (ex: '2020-01-01').
- Extrair dados da tabela `orders` filtrando por
  WHERE updated_at > last_run.
- Utilizar transacao para atualizar o last_run apos a
  extracao bem-sucedida.
- Tratar erros: reverter a atualizacao do last_run em caso
  de falha na extracao.

Dica Tecnica:
Use `pd.read_sql()` com parametros de consulta para evitar
SQL injection. Para atomicidade, execute a extracao e a
atualizacao do watermark dentro de uma mesma transacao
do SQLAlchemy.
*/
