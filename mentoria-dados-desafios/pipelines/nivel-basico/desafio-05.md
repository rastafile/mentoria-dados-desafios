/*
=========================================================
DESAFIO 05: Pipeline ETL Completo com Argumentos
=========================================================
Nivel: Basico

Objetivo:
Pipeline ETL completo que aceita argumentos via linha de
comando para selecionar tabelas e formato de saida.

Requisitos:
- Usar argparse para aceitar --tables (lista separada por
  virgula) e --format (csv, json ou parquet).
- Implementar funcao extract(): ler tabelas do banco.
- Implementar funcao transform(): limpeza basica (nulos,
  padronizacao, conversao de datas).
- Implementar funcao load(): salvar no formato escolhido
  em datasets/etl/.
- Exibir metricas: numero de linhas extraidas, limpas e
  carregadas.

Dica Tecnica:
Estruture o pipeline chamando extract() -> transform() ->
load() sequencialmente. Use o json ou parquet como formato
alternativo ao CSV. O parquet requer a biblioteca pyarrow.
*/
