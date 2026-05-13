import pandas as pd
from pipelines.utils.db import get_engine


def check_row_count(df, table, min_rows=1):
    # TODO: verificar se a tabela tem pelo menos min_rows linhas
    count = len(df)
    if count < min_rows:
        print(f'FALHA: {table} possui {count} linhas (minimo: {min_rows})')
        return False
    print(f'OK: {table} possui {count} linhas')
    return True


def check_null_columns(df, table, columns):
    # TODO: verificar se colunas especificas nao possuem nulos
    nulls = df[columns].isnull().sum()
    has_null = nulls.any()
    if has_null:
        print(f'FALHA: {table} possui valores nulos:\n{nulls[nulls > 0]}')
    return not has_null


def check_schema(df, table, expected_columns):
    # TODO: verificar se o schema da tabela corresponde ao esperado
    actual = list(df.columns)
    missing = [col for col in expected_columns if col not in actual]
    if missing:
        print(f'FALHA: {table} colunas faltando: {missing}')
        return False
    print(f'OK: {table} schema valido')
    return True


if __name__ == '__main__':
    engine = get_engine()
    tables = ['customers', 'products', 'orders', 'order_items', 'payments', 'shipments']

    all_passed = True

    for table in tables:
        df = pd.read_sql(f'SELECT * FROM {table}', engine)

        if not check_row_count(df, table):
            all_passed = False

        nulls = df.isnull().sum()
        if nulls.any():
            print(f'FALHA: {table} possui valores nulos:\n{nulls[nulls > 0]}')
            all_passed = False

    if all_passed:
        print('Todas as validacoes passaram!')
    else:
        print('Algumas validacoes falharam.')
        exit(1)
