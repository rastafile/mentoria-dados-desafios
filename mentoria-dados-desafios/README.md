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
- **Python**: Utilizado para geração de dados sintéticos (dummy data) e, futuramente, pipelines.
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
├── notebooks/           # Espaço para análises exploratórias (Jupyter)
├── tests/               # Testes de pipelines e qualidade de dados
└── docker-compose.yml   # Subida do banco PostgreSQL local
```

## 🚀 Como Subir o Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/mentoria-dados-desafios.git
   cd mentoria-dados-desafios
   ```

2. **Inicie o Banco de Dados com Docker:**
   ```bash
   docker-compose up -d
   ```
   Isso criará uma instância do PostgreSQL rodando na porta `5432` com o banco `mentoria_dados` (Usuário: `postgres`, Senha: `postgres`).

3. **Instale as Dependências Python:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

4. **Gere e Popule os Dados:**
   Execute o script principal para gerar dados em CSV e inserir no banco:
   ```bash
   python scripts/setup/generate_data.py
   ```
   *(Este script irá recriar as tabelas e inserir centenas de registros consistentes simulando um cenário de e-commerce com clientes, pedidos, produtos, etc).*

## 💡 Como Executar os Desafios

Os desafios estão dentro da pasta correspondente à sua trilha atual (ex: `sql/nivel-basico`). 

1. Leia o arquivo `.sql` ou `.md` do desafio.
2. Escreva sua query no arquivo.
3. Valide o resultado contra o seu banco de dados local.

## 🤝 Como Contribuir e Versionar seus Desafios

Para os mentorados que desejam salvar o progresso:
1. Crie uma branch com seu nome e trilha: `git checkout -b fulano-sql-basico`
2. Resolva os desafios nos arquivos locais.
3. Faça o commit com mensagens claras: `git commit -m "feat: resolve desafio 01 a 05 de SQL basico"`
4. Suba para o repositório remoto ou para o seu fork: `git push origin fulano-sql-basico`

Para mais detalhes sobre a convivência e as metodologias, leia as [Regras da Mentoria](docs/regras.md) e o [Overview](docs/overview.md).
