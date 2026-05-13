import os
import pandas as pd
from sqlalchemy import create_engine

# Configuracao do banco
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)


def extrair_customers():
    # TODO: escrever query SELECT * FROM customers
    query = 'SELECT * FROM customers'

    # TODO: executar pd.read_sql com a query e o engine
    df = pd.read_sql(query, engine)

    return df


def main():
    print('Conectando ao banco e extraindo tabela customers...')

    # TODO: chamar funcao extrair_customers
    df = extrair_customers()

    # TODO: exibir as 5 primeiras linhas
    print('\nPrimeiras linhas do DataFrame:')
    print(df.head())

    # TODO: exibir informacoes do DataFrame
    print('\nInformacoes do DataFrame:')
    print(df.info())


if __name__ == '__main__':
    main()
