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
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'order_items')


def extrair_orders_order_items(engine):
    # TODO: Extrair dados com JOIN entre orders e order_items
    logger.info('Extraindo orders e order_items do banco.')
    query = """
        SELECT
            oi.order_item_id,
            oi.order_id,
            oi.product_id,
            oi.quantity,
            oi.unit_price,
            oi.total_price,
            o.order_date
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        ORDER BY o.order_date
    """
    df = pd.read_sql(text(query), engine)
    logger.info(f'Total de registros extraidos: {len(df)}.')
    return df


def criar_colunas_data(df):
    # TODO: Criar colunas year e month a partir de order_date
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    logger.info('Colunas year e month criadas.')
    return df


def salvar_particionado(df):
    # TODO: Salvar dados particionados por year/month
    logger.info(f'Salvando dados particionados em {OUTPUT_DIR}.')

    for (year, month), grupo in df.groupby(['year', 'month']):
        partition_path = os.path.join(
            OUTPUT_DIR,
            f'year={year}',
            f'month={str(month).zfill(2)}'
        )
        os.makedirs(partition_path, exist_ok=True)

        arquivo = os.path.join(partition_path, 'data.csv')
        grupo.to_csv(arquivo, index=False)
        logger.info(
            f'Particao year={year}, month={month}: '
            f'{len(grupo)} registros salvos em {arquivo}.'
        )


def main():
    logger.info('Iniciando pipeline de particionamento por data.')
    engine = get_engine()

    df = extrair_orders_order_items(engine)
    df = criar_colunas_data(df)
    salvar_particionado(df)

    logger.info('Pipeline de particionamento concluida.')


if __name__ == '__main__':
    main()
