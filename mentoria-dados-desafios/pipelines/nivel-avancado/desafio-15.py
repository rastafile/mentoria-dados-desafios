import logging
import pandas as pd
from pipelines.utils.db import get_engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract():
    # TODO: extrair dados de todas as tabelas
    engine = get_engine()
    tables = ['customers', 'products', 'orders', 'order_items', 'payments', 'shipments']
    data = {}
    for table in tables:
        logger.info(f'Extraindo tabela: {table}')
        data[table] = pd.read_sql(f'SELECT * FROM {table}', engine)
    return data


def transform(df_orders):
    # TODO: aplicar transformacoes e agregacoes
    df = df_orders.copy()
    df['order_date'] = pd.to_datetime(df['order_date'])
    aggregated = df.groupby(df['order_date'].dt.date)['total_amount'].sum().reset_index()
    aggregated.columns = ['data', 'total_faturamento']
    logger.info(f'Transformacao concluida: {len(aggregated)} registros')
    return aggregated


def validate(df_dict):
    # TODO: validar dados com Great Expectations
    try:
        from great_expectations.dataset import PandasDataset
        results = {}
        for name, df in df_dict.items():
            ds = PandasDataset(df)
            ds.expect_column_values_to_not_be_null(df.columns[0])
            result = ds.validate()
            results[name] = result['success']
            status = 'PASSOU' if result['success'] else 'FALHOU'
            logger.info(f'Validacao {name}: {status}')
        return results
    except ImportError:
        logger.warning('Great Expectations nao instalado. Pulando validacao.')
        return {}


def load(df, destination):
    # TODO: carregar dados no destino final
    output_path = f'{destination}.csv'
    df.to_csv(output_path, index=False)
    logger.info(f'Dados salvos em {output_path}')


def generate_report(extraction_counts, validation_results):
    # TODO: gerar relatorio final do pipeline
    lines = ['=' * 50, 'RELATORIO FINAL DO PIPELINE', '=' * 50, '']
    lines.append('Extracao:')
    for table, count in extraction_counts.items():
        lines.append(f'  - {table}: {count} registros')
    lines.append('')
    lines.append('Validacao:')
    for table, passed in validation_results.items():
        status = 'PASSOU' if passed else 'FALHOU'
        lines.append(f'  - {table}: {status}')
    return '\n'.join(lines)


if __name__ == '__main__':
    logger.info('Iniciando pipeline End-to-End')

    try:
        data = extract()
        extraction_counts = {k: len(v) for k, v in data.items()}
        logger.info('Extracao concluida')

        transformed_orders = transform(data['orders'])
        logger.info('Transformacao concluida')

        validation_results = validate(data)
        logger.info('Validacao concluida')

        load(transformed_orders, 'faturamento_diario')
        logger.info('Carga concluida')

        report = generate_report(extraction_counts, validation_results)
        with open('relatorio_pipeline.txt', 'w') as f:
            f.write(report)
        logger.info(f'Relatorio gerado:\n{report}')

    except Exception as e:
        logger.error(f'Pipeline falhou: {e}')
        raise
