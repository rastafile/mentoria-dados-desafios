# AGENTS.md -- Mentoria de Dados

## Project Overview

Repositório de mentoria prática em Engenharia/Analise de Dados com cenário de e-commerce baseado em PostgreSQL. Trilha: SQL (básico/intermediário/avancado) -> Modelagem -> Pipelines. As pastas `modelagem/`, `pipelines/`, `notebooks/` e `tests/` estao vazias (esqueletos). Codigo ativo esta em `scripts/` (Python + SQL) e `datasets/` (CSVs).

## Commands

### Environment Setup
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
docker-compose up -d                          # Start PostgreSQL (port 5432)
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
```

### Testing (not yet configured -- pytest expected when added)
```bash
python -m pytest                              # Run all tests
python -m pytest tests/test_file.py           # Run single test file
python -m pytest tests/test_file.py::test_fn  # Run single test
python -m pytest -x --pdb                     # Stop on first failure, drop into debugger
python -m pytest --cov=. --cov-report=term    # With coverage
```

### Linting / Formatting (not yet configured -- suggestions below)
```bash
# Ruff (when added):
# ruff check .                               # Lint
# ruff check . --fix                         # Auto-fix lint issues
# ruff format .                              # Auto-format

# SQLFluff (when added):
# sqlfluff lint sql/ --dialect postgres      # Lint SQL
# sqlfluff fix sql/ --dialect postgres       # Fix SQL
```

### Docker
```bash
docker-compose logs -f                       # Tail PostgreSQL logs
docker-compose down -v                       # Destroy + remove volume
```

## Code Style Guidelines

### Python (`scripts/`)

- **Imports**: Group in order: 1) built-in (`os`, `random`, `datetime`), 2) third-party (`pandas`, `numpy`, `faker`, `sqlalchemy`), 3) local. One import per line from `from` style.
- **Naming**: `snake_case` for variables/functions; `UPPER_CASE` for constants.
- **Formatting**: 4-space indentation, single quotes for strings (`'active'`), no trailing whitespace.
- **Type Hints**: Not currently used (legacy code); add them for new code/functions.
- **Error Handling**: Use `try/except` with specific exception types; avoid bare `except:`.
- **Logging**: Use `print()` for simple scripts; prefer `logging` module for pipelines.
- **Functions**: Procedural style, no classes currently. Use descriptive `snake_case` names.
- **Comments**: In Portuguese (`# Gerando Customers...`). Explain "why", not "what".
- **Docstrings**: Not used in legacy code; add Google-style docstrings for new functions.
- **Data**: Use `pandas.DataFrame` for tabular data; SQLAlchemy for DB connections.
- **File paths**: Always use `os.path.join` for cross-platform compatibility.

### SQL (`sql/`, `scripts/ddl/`, `scripts/dml/`)

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
scripts/ddl/                # create_tables.sql, constraints.sql
scripts/dml/                # insert_*.sql (auto-generated)
scripts/setup/              # generate_data.py
datasets/                   # *.csv (auto-generated)
modelagem/                  # Empty -- desafios futuros
pipelines/                  # Empty -- desafios futuros
notebooks/                  # Empty -- analises exploratorias
tests/                      # Empty -- testes futuros
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

## CI (`.github/workflows/ci.yml`)

Minimal -- only verifies directory structure and DDL file existence on push/PR to `main`.

## Recommendations for Future Setup

When adding tooling to this project, prefer:
- **Ruff** for Python linting + formatting (single tool, fast, covers flake8/isort/black)
- **SQLFluff** for SQL linting (`--dialect postgres`)
- **pytest** for testing (already referenced in `.gitignore` via `.pytest_cache/` and `.coverage`)
- **pre-commit** for automated lint checks before commits
- Add `pyproject.toml` at root to consolidate tool configs
- Consider `.editorconfig` for cross-editor consistency
