import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Inicializa Faker
fake = Faker('pt_BR')

# Configurações
NUM_CUSTOMERS = 150
NUM_PRODUCTS = 120
NUM_ORDERS = 500
START_DATE = datetime.now() - timedelta(days=365)
END_DATE = datetime.now()

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
DML_DIR = os.path.join(BASE_DIR, 'scripts', 'dml')

os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(DML_DIR, exist_ok=True)

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

print("Gerando Customers...")
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    status = np.random.choice(['active', 'inactive'], p=[0.8, 0.2])
    customers.append({
        'customer_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'phone': fake.phone_number(),
        'country': np.random.choice(['Brasil', 'Argentina', 'Chile', 'Colombia'], p=[0.8, 0.1, 0.05, 0.05]),
        'state': fake.state_abbr(),
        'city': fake.city(),
        'zip_code': fake.postcode(),
        'status': status,
        'created_at': random_date(START_DATE, END_DATE).strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
df_customers = pd.DataFrame(customers)

print("Gerando Products...")
categories = ['Eletrônicos', 'Móveis', 'Vestuário', 'Alimentos', 'Livros']
products = []
for i in range(1, NUM_PRODUCTS + 1):
    price = round(random.uniform(10.0, 5000.0), 2)
    cost = round(price * random.uniform(0.4, 0.8), 2)
    products.append({
        'product_id': i,
        'name': fake.catch_phrase(),
        'description': fake.text(max_nb_chars=200),
        'category': random.choice(categories),
        'price': price,
        'cost': cost,
        'stock_quantity': random.randint(0, 500), # 0 para simular sem estoque
        'created_at': START_DATE.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': START_DATE.strftime('%Y-%m-%d %H:%M:%S')
    })
df_products = pd.DataFrame(products)

print("Gerando Orders e Order Items...")
orders = []
order_items = []
item_id = 1

for i in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    
    # Simular queda de vendas nos últimos 2 meses reduzindo a probabilidade
    if random.random() < 0.2:
        o_date = random_date(END_DATE - timedelta(days=60), END_DATE)
    else:
        o_date = random_date(START_DATE, END_DATE - timedelta(days=60))
        
    status = np.random.choice(['paid', 'pending', 'cancelled', 'refunded'], p=[0.60, 0.15, 0.15, 0.10])
    
    # Gerar itens
    num_items = random.randint(1, 5)
    total_amount = 0
    for _ in range(num_items):
        product = df_products.iloc[random.randint(0, NUM_PRODUCTS - 1)]
        qty = random.randint(1, 3)
        unit_price = product['price']
        t_price = qty * unit_price
        total_amount += t_price
        
        order_items.append({
            'order_item_id': item_id,
            'order_id': i,
            'product_id': product['product_id'],
            'quantity': qty,
            'unit_price': unit_price,
            'total_price': t_price,
            'created_at': o_date.strftime('%Y-%m-%d %H:%M:%S')
        })
        item_id += 1

    orders.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': o_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'total_amount': total_amount,
        'created_at': o_date.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': o_date.strftime('%Y-%m-%d %H:%M:%S')
    })
df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)

print("Gerando Payments...")
payments = []
payment_methods = ['credit_card', 'pix', 'boleto', 'paypal']

for index, order in df_orders.iterrows():
    p_method = random.choice(payment_methods)
    p_status = 'pending'
    
    if order['status'] == 'paid':
        p_status = 'completed'
    elif order['status'] == 'refunded':
        p_status = 'refunded'
    elif order['status'] == 'cancelled':
        p_status = 'failed'
        
    # Fraude simulada: credit_card + failed mas com dados estranhos (deixaremos sutil)
    
    payments.append({
        'payment_id': order['order_id'], # 1 pra 1
        'order_id': order['order_id'],
        'payment_method': p_method,
        'payment_date': (datetime.strptime(order['order_date'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S') if p_status in ['completed', 'refunded'] else None,
        'amount': order['total_amount'],
        'status': p_status,
        'created_at': order['order_date']
    })
df_payments = pd.DataFrame(payments)

print("Gerando Shipments...")
shipments = []
shipment_id = 1
for index, order in df_orders.iterrows():
    if order['status'] in ['paid', 'refunded']:
        s_status = 'pending'
        s_date = None
        d_date = None
        
        if order['status'] == 'paid':
            s_status = np.random.choice(['shipped', 'delivered', 'pending'], p=[0.2, 0.7, 0.1])
        elif order['status'] == 'refunded':
            s_status = 'returned'
            
        o_date_obj = datetime.strptime(order['order_date'], '%Y-%m-%d %H:%M:%S')
        
        if s_status in ['shipped', 'delivered', 'returned']:
            s_date = (o_date_obj + timedelta(days=random.randint(1, 3))).strftime('%Y-%m-%d %H:%M:%S')
        if s_status in ['delivered', 'returned']:
            d_date = (o_date_obj + timedelta(days=random.randint(4, 15))).strftime('%Y-%m-%d %H:%M:%S')
            
        shipments.append({
            'shipment_id': shipment_id,
            'order_id': order['order_id'],
            'tracking_number': fake.ean13(),
            'shipment_date': s_date,
            'delivery_date': d_date,
            'status': s_status,
            'created_at': order['order_date']
        })
        shipment_id += 1
df_shipments = pd.DataFrame(shipments)

# Função para exportar CSV e DML
def export_data(df, table_name):
    print(f"Exportando {table_name}...")
    # CSV
    csv_path = os.path.join(DATASETS_DIR, f'{table_name}.csv')
    df.to_csv(csv_path, index=False)
    
    # DML SQL
    dml_path = os.path.join(DML_DIR, f'insert_{table_name}.sql')
    with open(dml_path, 'w') as f:
        f.write(f"-- Inserts for {table_name}\n")
        f.write(f"-- Generated automatically\n\n")
        
        # Split in batches to avoid huge lines
        batch_size = 100
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            columns = ', '.join(batch.columns)
            
            values_list = []
            for _, row in batch.iterrows():
                # Formata os valores para SQL
                row_vals = []
                for val in row:
                    if pd.isna(val):
                        row_vals.append("NULL")
                    elif isinstance(val, (int, float)):
                        row_vals.append(str(val))
                    else:
                        # Escape single quotes
                        val_str = str(val).replace("'", "''")
                        row_vals.append(f"'{val_str}'")
                values_list.append(f"({', '.join(row_vals)})")
                
            f.write(f"INSERT INTO {table_name} ({columns}) VALUES\n")
            f.write(",\n".join(values_list) + ";\n\n")

# Export all
export_data(df_customers, 'customers')
export_data(df_products, 'products')
export_data(df_orders, 'orders')
export_data(df_order_items, 'order_items')
export_data(df_payments, 'payments')
export_data(df_shipments, 'shipments')

print("Dados gerados com sucesso!")
