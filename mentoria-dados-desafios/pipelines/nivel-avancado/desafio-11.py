import os
import pandas as pd
from pipelines.utils.db import get_engine


def extract_customers(engine):
    # TODO: extrair tabela customers do banco
    return pd.read_sql('SELECT * FROM customers', engine)


def extract_products(engine):
    # TODO: extrair tabela products do banco
    return pd.read_sql('SELECT * FROM products', engine)


def save_to_csv(df, filename, output_dir):
    # TODO: salvar dataframe como csv no diretorio de output
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f'Arquivo salvo: {path}')


if __name__ == '__main__':
    output_dir = '/output'
    os.makedirs(output_dir, exist_ok=True)

    engine = get_engine()

    customers = extract_customers(engine)
    products = extract_products(engine)

    save_to_csv(customers, 'customers.csv', output_dir)
    save_to_csv(products, 'products.csv', output_dir)

    print('Extracao concluida. Arquivos salvos em /output')
