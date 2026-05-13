import pandas as pd
from great_expectations.dataset import PandasDataset
from pipelines.utils.db import get_engine


def validate_customers(ds):
    # TODO: criar expectativas para customers
    ds.expect_column_values_to_not_be_null('customer_id')


def validate_orders(ds):
    # TODO: criar expectativas para orders
    ds.expect_column_values_to_not_be_null('order_id')
    ds.expect_column_values_to_not_be_null('status')
    ds.expect_column_values_to_be_in_set('status', ['paid', 'pending', 'cancelled'])


def validate_products(ds):
    # TODO: criar expectativas para products
    ds.expect_column_values_to_not_be_null('product_id')
    ds.expect_column_values_to_not_be_null('price')
    ds.expect_column_values_to_be_between('price', 0, 10000)


def generate_report(results):
    # TODO: gerar relatorio html com resultados
    html_parts = ['<html><body><h1>Relatorio de Validacao</h1>']
    for name, result in results.items():
        status = 'PASSOU' if result['success'] else 'FALHOU'
        html_parts.append(f'<h2>{name}: {status}</h2>')
        if not result['success']:
            html_parts.append('<ul>')
            for res in result['results']:
                if not res['success']:
                    html_parts.append(
                        f'<li>{res["expectation_config"]["expectation_type"]}: '
                        f'{res["result"]}</li>'
                    )
            html_parts.append('</ul>')
    html_parts.append('</body></html>')
    return '\n'.join(html_parts)


if __name__ == '__main__':
    engine = get_engine()

    customers = pd.read_sql('SELECT * FROM customers', engine)
    orders = pd.read_sql('SELECT * FROM orders', engine)
    products = pd.read_sql('SELECT * FROM products', engine)

    ds_customers = PandasDataset(customers)
    ds_orders = PandasDataset(orders)
    ds_products = PandasDataset(products)

    validate_customers(ds_customers)
    validate_orders(ds_orders)
    validate_products(ds_products)

    results = {
        'customers': ds_customers.validate(),
        'orders': ds_orders.validate(),
        'products': ds_products.validate(),
    }

    for name, result in results.items():
        status = 'PASSOU' if result['success'] else 'FALHOU'
        print(f'Validacao {name}: {status}')
        if not result['success']:
            for res in result['results']:
                if not res['success']:
                    expectation = res['expectation_config']['expectation_type']
                    print(f'  - {expectation}: {res["result"]}')

    html = generate_report(results)
    with open('validacao_report.html', 'w') as f:
        f.write(html)

    print('Relatorio HTML gerado: validacao_report.html')
