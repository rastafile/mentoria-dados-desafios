import os
import argparse
import logging
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# TODO: Mover para um arquivo config.yaml ou config.json
CONFIG = {
    'dev': {
        'host': 'localhost',
        'port': 5432,
        'database': 'mentoria_dados',
        'user': 'postgres',
        'password': 'postgres',
        'schema': 'public',
    },
    'prod': {
        'host': 'proddb.example.com',
        'port': 5432,
        'database': 'mentoria_dados_prod',
        'user': 'app_user',
        'password': os.getenv('DB_PASSWORD_PROD', ''),
        'schema': 'app',
    },
}


def load_config(env):
    # TODO: Carregar configuracoes do ambiente
    if env not in CONFIG:
        raise ValueError(
            f'Ambiente invalido: {env}. '
            f'Use um dos: {list(CONFIG.keys())}.'
        )
    config = CONFIG[env]
    logger.info(f'Configuracoes carregadas para ambiente: {env}.')
    logger.info(f'Host: {config["host"]}, Database: {config["database"]}.')
    return config


def criar_engine_por_config(config):
    # TODO: Criar engine SQLAlchemy a partir da config
    url = (
        f'postgresql://{config["user"]}:{config["password"]}'
        f'@{config["host"]}:{config["port"]}/{config["database"]}'
    )
    engine = create_engine(url)
    logger.info('Engine criada com base na config do ambiente.')
    return engine


def main():
    parser = argparse.ArgumentParser(
        description='Pipeline multi-ambiente (Dev vs Prod).'
    )
    parser.add_argument(
        '--env',
        type=str,
        choices=['dev', 'prod'],
        default='dev',
        help='Ambiente de execucao (dev ou prod).'
    )
    args = parser.parse_args()

    logger.info(f'Iniciando pipeline no ambiente: {args.env}.')
    config = load_config(args.env)
    engine = criar_engine_por_config(config)

    # TODO: Executar pipeline de acordo com o ambiente
    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT COUNT(*) FROM information_schema.tables '
                 'WHERE table_schema = :schema'),
            {'schema': config['schema']}
        )
        total_tabelas = result.scalar()
        logger.info(f'Ambiente {args.env}: {total_tabelas} tabelas encontradas '
                    f'no schema {config["schema"]}.')

    logger.info(f'Pipeline no ambiente {args.env} concluida.')


if __name__ == '__main__':
    main()
