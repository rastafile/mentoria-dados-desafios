import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

# Configuracao do banco
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)

# Diretorio de saida
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, 'datasets', 'etl')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract(tabelas):
    print('Extracao: lendo tabelas do banco...')
    dados = {}

    # TODO: para cada tabela, executar pd.read_sql e armazenar
    for tabela in tabelas:
        query = f'SELECT * FROM {tabela}'
        df = pd.read_sql(query, engine)
        dados[tabela] = df
        print(f'  -> {tabela}: {len(df)} linhas extraidas')

    return dados


def transform(dados):
    print('Transformacao: aplicando limpeza...')

    # TODO: aplicar transformacoes em cada tabela
    for nome, df in dados.items():
        # Tratar nulos em colunas de texto
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('N/A' if col in ['phone', 'zip_code', 'tracking_number'] else 'desconhecido')

        # Padronizar status para minusculo se existir
        if 'status' in df.columns:
            df['status'] = df['status'].str.lower()

        # Converter colunas de data
        for col in df.columns:
            if col.endswith('_at') or col in ['order_date', 'shipment_date', 'delivery_date', 'payment_date']:
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

        dados[nome] = df
        print(f'  -> {nome}: {len(df)} linhas transformadas')

    return dados


def load(dados, formato):
    print(f'Carga: salvando no formato {formato}...')

    # TODO: salvar cada tabela no formato escolhido
    for nome, df in dados.items():
        if formato == 'csv':
            caminho = os.path.join(OUTPUT_DIR, f'{nome}.csv')
            df.to_csv(caminho, index=False)
        elif formato == 'json':
            caminho = os.path.join(OUTPUT_DIR, f'{nome}.json')
            df.to_json(caminho, orient='records', date_format='iso')
        elif formato == 'parquet':
            caminho = os.path.join(OUTPUT_DIR, f'{nome}.parquet')
            df.to_parquet(caminho, index=False)
        else:
            print(f'  -> Formato {formato} nao suportado')
            return

        print(f'  -> {nome} salvo em {caminho}')


def main():
    # TODO: configurar argparse com --tables e --format
    parser = argparse.ArgumentParser(description='Pipeline ETL completo')
    parser.add_argument('--tables', type=str,
                        default='customers,products,orders,order_items,payments,shipments',
                        help='Lista de tabelas separadas por virgula')
    parser.add_argument('--format', type=str, default='csv',
                        choices=['csv', 'json', 'parquet'],
                        help='Formato de saida dos arquivos')
    args = parser.parse_args()

    # Processar lista de tabelas
    tabelas = [t.strip() for t in args.tables.split(',')]

    print(f'Iniciando ETL completo para tabelas: {tabelas}')
    print(f'Formato de saida: {args.format}')

    # Pipeline ETL
    dados = extract(tabelas)
    dados = transform(dados)
    load(dados, args.format)

    print('ETL concluido com sucesso!')


if __name__ == '__main__':
    main()
