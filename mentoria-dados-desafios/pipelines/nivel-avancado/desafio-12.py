import pandas as pd
from pipelines.utils.db import get_engine


def pipeline(steps):
    # TODO: implementar decorator que registra etapas
    def decorator(func):
        def wrapper(*args, **kwargs):
            context = {}
            for step in steps:
                print(f'Executando etapa: {step.__name__}')
                result = step(context)
                context[step.__name__] = result
            return func(context)
        return wrapper
    return decorator


def extract_orders(context):
    # TODO: extrair tabela orders do banco
    engine = get_engine()
    df = pd.read_sql('SELECT * FROM orders', engine)
    context['orders'] = df
    return df


def transform_aggregate(context):
    # TODO: agregar dados (ex: total por dia)
    df = context.get('orders')
    if df is None:
        raise ValueError('Nenhum dado encontrado no contexto')
    aggregated = df.groupby(df['order_date'].dt.date)['total_amount'].sum().reset_index()
    context['aggregated'] = aggregated
    return aggregated


def load_star_schema(context):
    # TODO: carregar dados agregados no banco
    df = context.get('aggregated')
    if df is None:
        raise ValueError('Nenhum dado agregado encontrado')
    print('Dados prontos para load:')
    print(df.head())
    return df


@pipeline(steps=[extract_orders, transform_aggregate, load_star_schema])
def run_pipeline(context):
    print('Pipeline concluido com sucesso!')
    return context


if __name__ == '__main__':
    run_pipeline()
