/*
=========================================================
DESAFIO 15: Pipeline End-to-End
=========================================================
Nivel: Avancado

Objetivo:
Implementar um pipeline completo integrando todas as etapas
dos desafios anteriores: extracao, transformacao, validacao
com Great Expectations, e carga. O pipeline deve ser executado
via Docker, orquestrado por script, e pronto para CI/CD.

Requisitos:
- Extrair dados do banco PostgreSQL.
- Transformar e agregar conforme regras de negocio.
- Validar qualidade com Great Expectations (desafio-13).
- Carregar resultados em tabela final ou CSV.
- Utilizar logging estruturado com o modulo logging.
- Tratar erros com try/except e registrar falhas.
- Gerar relatorio final resumindo o pipeline.

Dica Tecnica:
Estrutura o codigo em funcoes modulares (extract, transform,
validate, load). Use o modulo logging com formatacao
'%(asctime)s - %(levelname)s - %(message)s'. O relatorio
final pode ser um simples print ou um arquivo .txt.
*/
