import pytest
from sqlalchemy import create_engine, text

DB_URL = 'postgresql://postgres:postgres@localhost:5432/mentoria_dados'


@pytest.fixture(scope='session')
def engine():
    return create_engine(DB_URL)


@pytest.fixture(scope='session')
def tables(engine):
    query = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    with engine.connect() as conn:
        result = conn.execute(query)
        return [row[0] for row in result]


@pytest.fixture(scope='session')
def table_names():
    return ['customers', 'products', 'orders', 'order_items', 'payments', 'shipments']
