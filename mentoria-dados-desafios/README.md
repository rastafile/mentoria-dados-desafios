# Mentoria de Dados - Desafios Práticos

Bem-vindo ao repositório oficial de desafios práticos da **Mentoria de Dados**. Este ambiente foi estruturado profissionalmente para simular o dia a dia de um Engenheiro de Dados e Analista de Dados, abordando desde modelagem e SQL até pipelines avançados.

## 🎯 Objetivo

O objetivo deste projeto é fornecer uma plataforma hands-on com cenários de negócios reais (pedidos, clientes, produtos, pagamentos) para que os mentorados possam testar e aprimorar suas habilidades em um ambiente controlado, utilizando as melhores práticas do mercado.

## 🗺️ Roadmap de Evolução

A trilha de conhecimento foi desenhada para construir bases sólidas antes de avançar para a automação:
1. **SQL** (Básico, Intermediário, Avançado)
2. **Modelagem de Dados**
3. **Pipelines de Dados**

Para detalhes completos do roadmap, veja nosso [Roadmap Completo](docs/roadmap.md).

## 🛠️ Tecnologias Utilizadas

- **PostgreSQL**: Banco de dados relacional principal.
- **Docker & Docker Compose**: Orquestração do ambiente local.
- **Python**: Utilizado para geração de dados sintéticos (dummy data) e pipelines de dados.
- **GitHub Actions**: Pipeline de CI para validação contínua.
- **VS Code**: Editor sugerido.

## 🏗️ Estrutura do Projeto

```text
mentoria-dados-desafios/
├── docs/                # Documentação oficial da mentoria (regras, overview, roadmap)
├── datasets/            # Arquivos CSV gerados com dados fake consistentes
├── scripts/
│   ├── ddl/             # Scripts de criação de tabelas e constraints
│   ├── dml/             # Scripts de inserção (gerados via Python)
│   └── setup/           # Script Python para popular o banco de dados
├── sql/                 # Desafios SQL divididos em níveis
├── modelagem/           # Desafios de modelagem divididos em níveis
├── pipelines/           # Desafios de engenharia de dados divididos em níveis
├── notebooks/           # (reservado) Análises exploratórias com Jupyter
├── tests/               # (reservado) Testes de pipelines e qualidade de dados
└── docker-compose.yml   # Subida do banco PostgreSQL local
```

## 🚀 Como Subir o Ambiente

1. **Faça um Fork do Repositório**
   Acesse [github.com/anomalyco/mentoria-dados-desafios](https://github.com/rastafile/mentoria-dados-desafios) e clique em **Fork** para criar uma cópia na sua conta.

2. **Clone o seu Fork:**
   ```bash
   git clone https://github.com/SEU_USUARIO/mentoria-dados-desafios.git
   cd mentoria-dados-desafios
   ```

3. **Inicie o Banco de Dados com Docker:**
   ```bash
   docker compose up -d
   ```
   Isso criará uma instância do PostgreSQL rodando na porta `5432` com o banco `mentoria_dados` (Usuário: `postgres`, Senha: `postgres`).

4. **Instale as Dependências Python:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

5. **Gere os Dados (CSV + Scripts DML):**
   ```bash
   python scripts/setup/generate_data.py
   ```
   Isso gera arquivos CSV em `datasets/` e scripts de inserção em `scripts/dml/`.

6. **Crie as Tabelas e Popule o Banco:**
   ```bash
   # Opção A: passo a passo (DDL + DML)
   psql -h localhost -U postgres -d mentoria_dados -f scripts/ddl/create_tables.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/ddl/constraints.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_customers.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_products.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_orders.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_order_items.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_payments.sql
   psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_shipments.sql

   # Opção B: atalho (init_database.sql já inclui DDL + constraints)
   psql -h localhost -U postgres -d mentoria_dados -f scripts/setup/init_database.sql
   ```
   Quando pedir a senha, digite: `postgres`

   > **Alternativa sem psql instalado:** use `docker exec`
   > ```bash
   > docker exec -it mentoria_postgres psql -U postgres -d mentoria_dados
   > ```

   **Conexão com o Banco:**
   ```
   Host: localhost  |  Porta: 5432  |  Database: mentoria_dados
   Usuário: postgres  |  Senha: postgres
   String: postgresql://postgres:postgres@localhost:5432/mentoria_dados
   ```

## 💡 Como Executar os Desafios

Os desafios estão dentro da pasta correspondente à sua trilha atual (ex: `sql/nivel-basico`). 

1. Leia o arquivo `.sql` do desafio (ex: `desafio-01.sql`).
2. Escreva sua query dentro do próprio arquivo, após o comentário `-- Escreva sua query abaixo:`.
3. Valide o resultado executando a query no banco usando uma das ferramentas abaixo:
   - **Terminal:** `psql -h localhost -U postgres -d mentoria_dados`
   - **DBeaver / DataGrip / TablePlus:** conecte usando os dados acima e rode a query
   - **VS Code:** extensão "PostgreSQL" ou "SQLTools"

## 🤝 Como Versionar seus Desafios no Fork

1. Resolva os desafios editando os arquivos `.sql`.
2. Adicione e commite as alterações no seu fork:
   ```bash
   git add .
   git commit -m "feat: resolve desafio 01 a 05 de SQL basico"
   ```
3. Envie para o seu fork no GitHub:
   ```bash
   git push origin main
   ```
4. Avise seu mentor que os desafios estão prontos para revisão.

Para mais detalhes sobre a convivência e as metodologias, leia as [Regras da Mentoria](docs/regras.md) e o [Overview](docs/overview.md).
