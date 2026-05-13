/*
=========================================================
DESAFIO 13: Great Expectations
=========================================================
Nivel: Avancado

Objetivo:
Adicionar validacoes de qualidade de dados utilizando a
biblioteca Great Expectations para garantir a integridade
das tabelas do banco.

Requisitos:
- Usar PandasDataset do great_expectations para validar DataFrames.
- Criar expectativa de nao nulos em colunas obrigatorias.
- Validar que status da tabela orders esteja em {'paid', 'pending', 'cancelled'}.
- Validar que price da tabela products esteja entre 0 e 10000.
- Gerar um relatorio HTML com os resultados das validacoes.

Dica Tecnica:
Utilize o metodo .validate() do PandasDataset para executar
todas as expectativas de uma vez. O relatorio HTML pode ser
salvo com .save() ou convertendo o resultado em HTML manualmente.
*/
