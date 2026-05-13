import os
import logging
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from pipelines.utils.db import get_engine

# Configuracao de logging basico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PIPELINE_NAME = 'carga_incremental_orders'
DEFAULT_LAST_RUN = '2020-01-01 00:00:00'

TABLE_METADATA = 'pipeline_metadata'
TABLE_ORIGEM = 'orders'


def criar_tabela_metadata(engine):
    # TODO: Criar tabela de controle se nao existir
    query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_METADATA} (
            pipeline_name VARCHAR(100) PRIMARY KEY,
            last_run TIMESTAMP NOT NULL
        )
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
    logger.info(f'Tabela {TABLE_METADATA} verificada/criada com sucesso.')


def obter_last_run(engine):
    # TODO: Buscar o timestamp da ultima execucao
    query = text(
        f'SELECT last_run FROM {TABLE_METADATA} '
        f'WHERE pipeline_name = :pipeline_name'
    )
    with engine.connect() as conn:
        result = conn.execute(
            query, {'pipeline_name': PIPELINE_NAME}
        ).fetchone()

    if result is None:
        logger.info(
            f'Nenhum ultimo run encontrado para {PIPELINE_NAME}. '
            f'Usando default: {DEFAULT_LAST_RUN}'
        )
        return datetime.strptime(DEFAULT_LAST_RUN, '%Y-%m-%d %H:%M:%S')
    return result[0]


def atualizar_last_run(engine, execution_time):
    # TODO: Atualizar o timestamp da ultima execucao
    query = text(f"""
        INSERT INTO {TABLE_METADATA} (pipeline_name, last_run)
        VALUES (:pipeline_name, :last_run)
        ON CONFLICT (pipeline_name)
        DO UPDATE SET last_run = EXCLUDED.last_run
    """)
    with engine.connect() as conn:
        conn.execute(query, {
            'pipeline_name': PIPELINE_NAME,
            'last_run': execution_time
        })
        conn.commit()
    logger.info(f'Last_run atualizado para {execution_time}.')


def extrair_incremental(engine, last_run):
    # TODO: Extrair apenas registros atualizados apos o ultimo run
    logger.info(f'Extraindo registros com updated_at > {last_run}.')
    query = f"""
        SELECT *
        FROM {TABLE_ORIGEM}
        WHERE updated_at > :last_run
        ORDER BY updated_at ASC
    """
    df = pd.read_sql(text(query), engine, params={'last_run': last_run})
    logger.info(f'Registros extraidos: {len(df)}.')
    return df


def main():
    logger.info('Iniciando pipeline de carga incremental.')
    engine = get_engine()
    execution_time = datetime.now()

    criar_tabela_metadata(engine)
    last_run = obter_last_run(engine)

    try:
        df = extrair_incremental(engine, last_run)
        # TODO: Adicionar etapa de carga no destino (arquivo ou tabela)
        df.to_csv(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'datasets',
                f'orders_incremental_{execution_time.strftime("%Y%m%d_%H%M%S")}.csv'
            ),
            index=False
        )
        logger.info(f'Arquivo salvo com {len(df)} registros.')

        atualizar_last_run(engine, execution_time)
    except Exception as e:
        logger.error(f'Erro durante a extracao: {e}. Last_run nao atualizado.')
        raise

    logger.info('Pipeline concluida com sucesso.')


if __name__ == '__main__':
    main()
