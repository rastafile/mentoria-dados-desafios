/*
=========================================================
DESAFIO 14: CI/CD com GitHub Actions
=========================================================
Nivel: Avancado

Objetivo:
Criar um workflow de CI/CD no GitHub Actions que execute
o pipeline de dados automaticamente nos eventos de push e
agendamento, garantindo integridade continua dos dados.

Requisitos:
- Trigger: push na branch main e schedule diario (cron).
- Setup: Python 3.11, dependencias do requirements.txt.
- Executar o pipeline de extracao e validacao.
- Rodar testes automatizados.
- Falhar o workflow se as validacoes nao passarem.

Dica Tecnica:
Use services: postgres no GitHub Actions para subir um banco
de teste. Utilize variaveis de ambiente via secrets para
configurar a string de conexao.
*/
