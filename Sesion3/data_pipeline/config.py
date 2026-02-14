# config.py

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3310,
    'user': 'root',
    'password': 'root',
    'database': 'retail_db'
}

CSV_FILES = {
    'customers': 'data/customers.csv',
    'departments': 'data/departments.csv',
    'categories': 'data/categories.csv',
    'products': 'data/products.csv',
    'orders': 'data/orders.csv',
    'order_items': 'data/order_items.csv'
}

LOG_FILE = 'logs/pipeline.log'
