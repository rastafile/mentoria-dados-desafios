import os
import logging
import pandas as pd
from sqlalchemy import text
from pipelines.utils.db import get_engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def carregar_csv(table_name):
    # TODO: Carregar CSV atualizado da tabela
    caminho = os.path.join(BASE_DIR, 'datasets', f'{table_name}.csv')
    logger.info(f'Carregando CSV: {caminho}.')
    return pd.read_csv(caminho)


def upsert_table(engine, df, table_name, primary_key):
    # TODO: Realizar upsert usando INSERT ... ON CONFLICT
    logger.info(f'Executando upsert na tabela {table_name}.')

    # Cria tabela temporaria com os dados de origem
    temp_table = f'temp_{table_name}'
    df.to_sql(temp_table, engine, if_exists='replace', index=False)

    # Descobre as colunas (exceto a primary key)
    colunas = [col for col in df.columns if col != primary_key]

    # Constroi a clausula de update dinamicamente
    updates = ', '.join([f'{col} = EXCLUDED.{col}' for col in colunas])

    upsert_sql = text(f"""
        INSERT INTO {table_name} ({', '.join(df.columns)})
        SELECT {', '.join(df.columns)}
        FROM {temp_table}
        ON CONFLICT ({primary_key})
        DO UPDATE SET {updates}
    """)

    with engine.connect() as conn:
        conn.execute(upsert_sql)
        conn.commit()
        logger.info(f'Upsert concluido para tabela {table_name}.')

    # Limpa tabela temporaria
    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS {temp_table}'))
        conn.commit()


def main():
    logger.info('Iniciando pipeline de upsert.')

    engine = get_engine()
    tabelas = [
        ('customers', 'customer_id'),
        ('products', 'product_id'),
        ('orders', 'order_id'),
    ]

    for table_name, pk in tabelas:
        try:
            df = carregar_csv(table_name)
            upsert_table(engine, df, table_name, pk)
        except Exception as e:
            logger.error(f'Erro ao processar {table_name}: {e}')

    logger.info('Pipeline de upsert concluida.')


if __name__ == '__main__':
    main()
