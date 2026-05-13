import os
import pandas as pd
from sqlalchemy import create_engine

# Configuracao do banco
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)

# Diretorio de saida
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

# Lista de tabelas para exportar
TABELAS = ['customers', 'products', 'orders', 'order_items', 'payments', 'shipments']


def exportar_tabela(nome_tabela):
    print(f'Exportando tabela {nome_tabela}...')

    # TODO: escrever query SELECT * FROM {nome_tabela}
    query = f'SELECT * FROM {nome_tabela}'

    # TODO: executar pd.read_sql
    df = pd.read_sql(query, engine)

    # TODO: salvar como CSV
    caminho_csv = os.path.join(DATASETS_DIR, f'{nome_tabela}.csv')
    df.to_csv(caminho_csv, index=False)

    print(f'  -> {len(df)} linhas exportadas para {caminho_csv}')


def main():
    print('Iniciando exportacao de todas as tabelas para CSV...')

    # TODO: iterar sobre a lista de tabelas e chamar exportar_tabela
    for tabela in TABELAS:
        exportar_tabela(tabela)

    print('Exportacao concluida com sucesso!')


if __name__ == '__main__':
    main()
