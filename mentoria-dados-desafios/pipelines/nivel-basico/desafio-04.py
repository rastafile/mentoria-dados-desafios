import os
import pandas as pd
from sqlalchemy import create_engine

# Configuracao do banco
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)

# Diretorio de saida
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')


def extrair_dados():
    print('Extraindo dados do banco...')

    # TODO: executar SELECT * FROM customers
    query = 'SELECT * FROM customers'
    df = pd.read_sql(query, engine)

    print(f'  -> {len(df)} registros extraidos')
    return df


def tratar_nulos(df):
    print('Tratando valores nulos...')

    # TODO: preencher phone com 'N/A'
    df['phone'] = df['phone'].fillna('N/A')

    # TODO: preencher zip_code com '00000-000'
    df['zip_code'] = df['zip_code'].fillna('00000-000')

    return df


def padronizar_status(df):
    print('Padronizando status para minusculo...')

    # TODO: converter coluna status para minusculo
    df['status'] = df['status'].str.lower()

    return df


def converter_datas(df):
    print('Convertendo colunas de data para datetime...')

    # TODO: converter created_at e updated_at para datetime
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    return df


def remover_duplicatas(df):
    print('Removendo duplicatas baseadas em email...')

    # TODO: remover linhas duplicadas pela coluna email
    df = df.drop_duplicates(subset=['email'])

    print(f'  -> {len(df)} registros apos limpeza')
    return df


def main():
    print('Iniciando pipeline de limpeza e transformacao...')

    # Pipeline de etapas
    dados = extrair_dados()
    dados = tratar_nulos(dados)
    dados = padronizar_status(dados)
    dados = converter_datas(dados)
    dados = remover_duplicatas(dados)

    # TODO: exibir DataFrame final
    print('\nDataFrame apos limpeza:')
    print(dados.head())
    print(dados.info())

    # TODO: salvar como CSV limpo
    caminho_csv = os.path.join(DATASETS_DIR, 'customers_clean.csv')
    dados.to_csv(caminho_csv, index=False)
    print(f'\nDados limpos salvos em {caminho_csv}')


if __name__ == '__main__':
    main()
