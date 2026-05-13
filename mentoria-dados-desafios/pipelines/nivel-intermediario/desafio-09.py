import os
import pandas as pd
from sqlalchemy import text
from pipelines.utils.db import get_engine

TABELAS = ['customers', 'products', 'orders', 'order_items', 'payments', 'shipments']

COLUNAS_OBRIGATORIAS = {
    'customers': ['customer_id', 'email'],
    'products': ['product_id', 'price'],
    'orders': ['order_id', 'customer_id', 'total_amount'],
    'order_items': ['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price'],
    'payments': ['payment_id', 'order_id', 'amount'],
    'shipments': ['shipment_id', 'order_id'],
}

COLUNAS_UNIQUE = {
    'customers': ['email'],
}

VALORES_ESPERADOS = {
    'customers': {'status': ['active', 'inactive']},
    'orders': {'status': ['pending', 'paid', 'cancelled', 'refunded']},
    'payments': {'status': ['pending', 'completed', 'failed', 'refunded']},
    'shipments': {'status': ['pending', 'shipped', 'delivered', 'returned']},
}

RELACOES_FK = [
    ('orders', 'customer_id', 'customers', 'customer_id'),
    ('order_items', 'order_id', 'orders', 'order_id'),
    ('order_items', 'product_id', 'products', 'product_id'),
    ('payments', 'order_id', 'orders', 'order_id'),
    ('shipments', 'order_id', 'orders', 'order_id'),
]


def validar_nulos(engine):
    # TODO: checar nulos em colunas obrigatorias
    resultados = []
    for tabela, colunas in COLUNAS_OBRIGATORIAS.items():
        for coluna in colunas:
            query = text(f'SELECT COUNT(*) as total FROM {tabela} WHERE {coluna} IS NULL')
            df = pd.read_sql(query, engine)
            total_nulos = df['total'].iloc[0]
            if total_nulos > 0:
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'nulo_em_{coluna}',
                    'status': 'FALHOU',
                    'detalhes': f'{total_nulos} registros com {coluna} nulo'
                })
            else:
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'nulo_em_{coluna}',
                    'status': 'PASSOU',
                    'detalhes': 'Nenhum registro nulo'
                })
    return resultados


def validar_duplicatas(engine):
    # TODO: checar duplicatas em colunas unique
    resultados = []
    for tabela, colunas in COLUNAS_UNIQUE.items():
        for coluna in colunas:
            query = text(f"""
                SELECT {coluna}, COUNT(*) as qtd
                FROM {tabela}
                GROUP BY {coluna}
                HAVING COUNT(*) > 1
                LIMIT 10
            """)
            df = pd.read_sql(query, engine)
            if not df.empty:
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'duplicata_em_{coluna}',
                    'status': 'FALHOU',
                    'detalhes': f'{len(df)} valores duplicados (ex: {df.iloc[0][coluna]})'
                })
            else:
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'duplicata_em_{coluna}',
                    'status': 'PASSOU',
                    'detalhes': 'Nenhuma duplicata encontrada'
                })
    return resultados


def validar_fks(engine):
    # TODO: checar consistencia de chaves estrangeiras
    resultados = []
    for tabela_filha, coluna_filha, tabela_pai, coluna_pai in RELACOES_FK:
        query = text(f"""
            SELECT COUNT(*) as total
            FROM {tabela_filha} f
            LEFT JOIN {tabela_pai} p ON f.{coluna_filha} = p.{coluna_pai}
            WHERE p.{coluna_pai} IS NULL
        """)
        df = pd.read_sql(query, engine)
        total_orfas = df['total'].iloc[0]
        if total_orfas > 0:
            resultados.append({
                'tabela': tabela_filha,
                'validacao': f'fk_{coluna_filha}_para_{tabela_pai}',
                'status': 'FALHOU',
                'detalhes': f'{total_orfas} registros orfaos em {tabela_filha}.{coluna_filha}'
            })
        else:
            resultados.append({
                'tabela': tabela_filha,
                'validacao': f'fk_{coluna_filha}_para_{tabela_pai}',
                'status': 'PASSOU',
                'detalhes': 'Todas as FKs sao validas'
            })
    return resultados


def validar_valores(engine):
    # TODO: checar valores inesperados em colunas de status
    resultados = []
    for tabela, colunas in VALORES_ESPERADOS.items():
        for coluna, esperados in colunas.items():
            placeholders = ', '.join(f"'{v}'" for v in esperados)
            query = text(f"""
                SELECT DISTINCT {coluna} as valor
                FROM {tabela}
                WHERE {coluna} NOT IN ({placeholders})
                AND {coluna} IS NOT NULL
            """)
            df = pd.read_sql(query, engine)
            if not df.empty:
                valores = df['valor'].tolist()
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'valores_{coluna}',
                    'status': 'FALHOU',
                    'detalhes': f'Valores inesperados: {valores}'
                })
            else:
                resultados.append({
                    'tabela': tabela,
                    'validacao': f'valores_{coluna}',
                    'status': 'PASSOU',
                    'detalhes': 'Todos os valores estao dentro do esperado'
                })
    return resultados


def gerar_relatorio(resultados):
    # TODO: consolidar e exportar relatorio
    df_relatorio = pd.DataFrame(resultados)
    print(df_relatorio.to_string(index=False))

    aprovado = df_relatorio[df_relatorio['status'] == 'PASSOU'].shape[0]
    falhou = df_relatorio[df_relatorio['status'] == 'FALHOU'].shape[0]
    print(f'\nTotal: {len(df_relatorio)} | PASSOU: {aprovado} | FALHOU: {falhou}')

    saida = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'datasets', 'relatorio_qualidade.csv'
    )
    df_relatorio.to_csv(saida, index=False)
    print(f'Relatorio salvo em: {saida}')
    return df_relatorio


def main():
    print('Iniciando validacao manual de qualidade de dados...')
    engine = get_engine()

    resultados = []
    resultados.extend(validar_nulos(engine))
    resultados.extend(validar_duplicatas(engine))
    resultados.extend(validar_fks(engine))
    resultados.extend(validar_valores(engine))

    df_relatorio = gerar_relatorio(resultados)
    return df_relatorio


if __name__ == '__main__':
    main()
