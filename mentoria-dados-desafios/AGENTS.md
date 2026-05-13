# AGENTS.md -- Mentoria de Dados

## Project Overview

Repositório de mentoria prática em Engenharia/Analise de Dados com cenário de e-commerce baseado em PostgreSQL. Trilha: SQL (básico/intermediário/avancado) -> Modelagem -> Pipelines. As pastas `notebooks/` e `tests/` estao vazias (esqueletos). Codigo ativo esta em `scripts/` (Python + SQL), `pipelines/` (Python), `sql/` (desafios) e `datasets/` (CSVs).

## Commands

### Environment Setup
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
docker compose up -d                          # Start PostgreSQL (port 5432)
```

### Generate / Reset Data
```bash
python scripts/setup/generate_data.py         # Generate CSVs + DML inserts
# Then apply DDL + DML to the database:
psql -h localhost -U postgres -d mentoria_dados -f scripts/ddl/create_tables.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/ddl/constraints.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_customers.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_products.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_orders.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_order_items.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_payments.sql
psql -h localhost -U postgres -d mentoria_dados -f scripts/dml/insert_shipments.sql

# Alternative without psql installed:
docker exec -it mentoria_postgres psql -U postgres -d mentoria_dados -f scripts/ddl/create_tables.sql
```

### Testing
```bash
python -m pytest                              # Run all tests
python -m pytest tests/test_database.py       # Run single test file
python -m pytest tests/test_database.py::TestDatabaseSchema  # Run single test class
python -m pytest tests/test_database.py::TestDatabaseSchema::test_tables_exist  # Run single test
python -m pytest -x --pdb                     # Stop on first failure, drop into debugger
python -m pytest --cov=. --cov-report=term    # With coverage
```

### Linting / Formatting
```bash
ruff check .                                  # Lint all Python files
ruff check . --fix                            # Auto-fix lint issues
ruff format .                                 # Auto-format all Python files
ruff format --check .                         # Check formatting without changes
```

### Docker
```bash
docker compose logs -f                        # Tail PostgreSQL logs
docker compose down -v                        # Destroy + remove volume
docker exec -it mentoria_postgres psql -U postgres -d mentoria_dados  # Interactive psql
```

## Code Style Guidelines

### Python (`scripts/`, `pipelines/`)

- **Imports**: Group in order: 1) built-in (`os`, `random`, `datetime`), 2) third-party (`pandas`, `numpy`, `faker`, `sqlalchemy`), 3) local. One import per line from `from` style.
- **Naming**: `snake_case` for variables/functions; `UPPER_CASE` for constants.
- **Formatting**: 4-space indentation, single quotes for strings (`'active'`), no trailing whitespace. Managed by Ruff.
- **Type Hints**: Not currently used (legacy code); add them for new code/functions.
- **Error Handling**: Use `try/except` with specific exception types; avoid bare `except:`.
- **Logging**: Use `print()` for simple scripts; prefer `logging` module for pipelines.
- **Functions**: Procedural style, no classes currently. Use descriptive `snake_case` names.
- **Comments**: In Portuguese (`# Gerando Customers...`). Explain "why", not "what".
- **Docstrings**: Not used in legacy code; add Google-style docstrings for new functions.
- **Data**: Use `pandas.DataFrame` for tabular data; SQLAlchemy for DB connections.
- **File paths**: Always use `os.path.join` for cross-platform compatibility.
- **DB connections**: Use `from pipelines.utils.db import get_engine` in pipeline scripts.

### SQL (`sql/`, `modelagem/`, `scripts/ddl/`, `scripts/dml/`)

- **Reserved Words**: UPPER CASE (`SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `WITH`, `DENSE_RANK`, `PARTITION BY`, `AS`, `ON`, `AND`, `OR`, `IN`, `NOT`, `NULL`, `INSERT INTO`, `VALUES`, `CREATE TABLE`, `ALTER TABLE`, `ADD CONSTRAINT`, `FOREIGN KEY`, `CHECK`, `DEFAULT`, `SERIAL`, `PRIMARY KEY`, `UNIQUE`, `DECIMAL`, `VARCHAR`, `TIMESTAMP`, `CASCADE`, `RESTRICT`, `IF NOT EXISTS`).
- **Identifiers**: `snake_case` (`customer_id`, `stock_quantity`, `total_amount`, `chk_products_price`, `fk_orders_customers`).
- **Indentation**: 4 spaces for subclauses, consistent alignment.
- **Aliases**: Descriptive (avoid `a`, `b`, `c`). Use explicit `AS` when defining.
- **Comments**: Block header `/* ... */` for challenge descriptions, `--` for inline.
- **Semicolons**: Every statement ends with `;`.
- **CTEs**: Prefer `WITH` for multi-step queries (window functions, filters).
- **Language**: Portuguese for comments and descriptions.

### Commit Messages

Follow conventional commits in Portuguese or English:
```
feat: resolve desafio 01 a 05 de SQL basico
fix: correct order total calculation
refactor: extract payment logic into CTE
```

## Project Structure (Key Paths)

```
sql/nivel-basico/           # desafio-01.sql .. desafio-05.sql
sql/nivel-intermediario/    # desafio-06.sql .. desafio-10.sql
sql/nivel-avancado/         # desafio-11.sql .. desafio-15.sql
modelagem/nivel-basico/     # desafio-01.md .. desafio-05.md (normalizacao)
modelagem/nivel-intermediario/  # desafio-06.md .. desafio-10.md (star schema)
modelagem/nivel-avancado/   # desafio-11.md .. desafio-15.md (scd, data vault)
pipelines/nivel-basico/     # desafio-01.py .. desafio-05.py (extracao full)
pipelines/nivel-intermediario/  # desafio-06.py .. desafio-10.py (carga incremental)
pipelines/nivel-avancado/   # desafio-11.py .. desafio-15.py (orquestracao, qualidade)
pipelines/utils/            # db.py (engine compartilhado)
pipelines/Dockerfile        # Container para execucao dos pipelines
scripts/ddl/                # create_tables.sql, constraints.sql
scripts/dml/                # insert_*.sql (auto-generated)
scripts/setup/              # generate_data.py, init_database.sql
datasets/                   # *.csv (auto-generated)
notebooks/                  # (reservado) analises exploratorias
tests/                      # test_database.py, conftest.py
.github/workflows/          # ci.yml (estrutura), pipeline.yml (dados)
```

## Database Schema (PostgreSQL, `mentoria_dados`)

6 tabelas: `customers`, `products`, `orders`, `order_items`, `payments`, `shipments`. Dados realistas com fraudes simuladas, cancelamentos, estornos, clientes inativos.

**Conn**: `postgresql://postgres:postgres@localhost:5432/mentoria_dados`

## Rules from `docs/regras.md`

1. Never commit directly to `main` -- always use feature branches.
2. SQL reserved words in UPPER CASE; descriptive aliases; comment complex code.
3. Never commit `.env` or real credentials.
4. Use GitHub Issues for questions about challenges.
5. If you used AI/forums to solve a challenge, add a comment explaining what you learned.

## CI / CD (`.github/workflows/`)

- **ci.yml**: Verifica estrutura de diretorios e existencia de DDLs em push/PR para `main`.
- **pipeline.yml**: Executa pipeline de dados (DDL + DML -> extracao -> validacao) em push para `main`, agendado diariamente, ou manualmente via `workflow_dispatch`.

## Additional Config

- `pyproject.toml`: Ruff config (line-length 100, single quotes, py311 target) + pytest config.
- `ruff` config: lint rules E/F/I/N/W/UP ativados; auto-format com single quotes.
