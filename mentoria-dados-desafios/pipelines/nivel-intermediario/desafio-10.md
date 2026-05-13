/*
=========================================================
DESAFIO 10: Multi-ambiente (Dev vs Prod)
=========================================================
Nivel: Intermediario

Objetivo:
Criar um script que aceita o argumento --env dev|prod e
carrega configuracoes diferentes de conexao (host, database,
schema, etc.) dependendo do ambiente.

Requisitos:
- Definir configuracoes em um dicionario Python ou arquivo
  YAML/JSON com parametros para dev e prod.
- Usar argparse para capturar o argumento --env.
- Implementar funcao load_config(env) que retorna um dicionario
  com as configuracoes do ambiente selecionado.
- Conectar ao banco usando as configuracoes carregadas.
- Logar qual ambiente esta sendo utilizado e os parametros
  (sem expor senhas).
- Validar que o ambiente informado eh valido (dev ou prod).

Dica Tecnica:
Use `argparse.ArgumentParser` com `add_argument('--env',
choices=['dev', 'prod'], default='dev')`. A funcao
load_config() pode usar um dict aninhado ou carregar de
um arquivo config.yaml com PyYAML.
*/
