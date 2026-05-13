import pandas as pd
from sqlalchemy import text


class TestDatabaseSchema:
    """Validacoes basicas da estrutura do banco de dados."""

    def test_tables_exist(self, engine, table_names):
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            existing = [row[0] for row in result]

        for table in table_names:
            assert table in existing, f'Tabela {table} nao encontrada'

    def test_customers_columns(self, engine):
        df = pd.read_sql('SELECT * FROM customers LIMIT 1', engine)
        expected = {'customer_id', 'first_name', 'last_name', 'email', 'status'}
        assert expected.issubset(df.columns), f'Colunas esperadas: {expected}'


class TestDatabaseData:
    """Validacoes de qualidade dos dados."""

    def test_customers_not_empty(self, engine):
        df = pd.read_sql('SELECT COUNT(*) as total FROM customers', engine)
        assert df['total'].iloc[0] > 0, 'Tabela customers vazia'

    def test_products_not_empty(self, engine):
        df = pd.read_sql('SELECT COUNT(*) as total FROM products', engine)
        assert df['total'].iloc[0] > 0, 'Tabela products vazia'

    def test_orders_not_empty(self, engine):
        df = pd.read_sql('SELECT COUNT(*) as total FROM orders', engine)
        assert df['total'].iloc[0] > 0, 'Tabela orders vazia'

    def test_customers_status_valid(self, engine):
        df = pd.read_sql('SELECT DISTINCT status FROM customers', engine)
        valid = {'active', 'inactive', None}
        for status in df['status']:
            assert status in valid, f'Status invalido: {status}'

    def test_products_price_positive(self, engine):
        df = pd.read_sql('SELECT COUNT(*) as total FROM products WHERE price < 0', engine)
        assert df['total'].iloc[0] == 0, 'Existem produtos com preco negativo'
