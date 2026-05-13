import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# Configuracao do banco
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)

# Diretorio dos CSVs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')


def importar_csv(caminho_arquivo):
    # Extrai o nome da tabela a partir do nome do arquivo
    nome_tabela = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    print(f'Importando {caminho_arquivo} para tabela {nome_tabela}...')

    try:
        # TODO: ler CSV com pd.read_csv
        df = pd.read_csv(caminho_arquivo)

        # TODO: inserir no banco com df.to_sql
        df.to_sql(nome_tabela, engine, if_exists='replace', index=False)

        print(f'  -> {len(df)} linhas inseridas em {nome_tabela}')

    except Exception as e:
        print(f'  -> ERRO ao importar {nome_tabela}: {e}')


def main():
    print('Iniciando importacao de CSVs para o banco...')

    # TODO: listar arquivos CSV no diretorio datasets
    pattern = os.path.join(DATASETS_DIR, '*.csv')
    arquivos = glob.glob(pattern)

    # TODO: iterar sobre os arquivos e importar cada um
    for arquivo in arquivos:
        importar_csv(arquivo)

    print('Importacao concluida com sucesso!')


if __name__ == '__main__':
    main()
