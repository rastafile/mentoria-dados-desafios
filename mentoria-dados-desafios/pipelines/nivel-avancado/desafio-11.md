/*
=========================================================
DESAFIO 11: Dockerizar Pipeline
=========================================================
Nivel: Avancado

Objetivo:
Criar um Dockerfile que empacote o pipeline basico (desafio-05)
em um container Docker, permitindo execucao portavel e reproduzivel.

Requisitos:
- Usar imagem python:3.11-slim como base.
- Instalar dependencias do requirements.txt.
- Copiar o codigo do projeto para /app no container.
- Configurar o CMD para executar pipelines/nivel-basico/desafio-05.py.
- O container deve aceitar a variavel de ambiente DB_URL para conexao.

Dica Tecnica:
Utilize Docker multi-stage ou mantenha a imagem enxuta com
python:3.11-slim. Instale apenas psycopg2-binary e pandas
para reduzir o tamanho final.
*/
