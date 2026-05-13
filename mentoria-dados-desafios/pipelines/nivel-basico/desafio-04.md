/*
=========================================================
DESAFIO 04: Pipeline de Limpeza e Transformacao
=========================================================
Nivel: Basico

Objetivo:
Pipeline que extrai dados do banco, aplica limpeza e
transformacoes, e exibe os resultados.

Requisitos:
- Extrair customers do banco.
- Tratar valores nulos: preencher phone com 'N/A' e
  zip_code com '00000-000'.
- Padronizar a coluna status para letras minusculas.
- Converter colunas de data (created_at, updated_at) de
  string para datetime.
- Remover linhas duplicadas com base no email.
- Exibir o DataFrame final e salvar como CSV limpo.

Dica Tecnica:
Organize o codigo em funcoes separadas para cada etapa
de transformacao: tratar_nulos(), padronizar_status(),
converter_datas(), remover_duplicatas().
*/
