# pipeline.py

import pandas as pd
from sqlalchemy import create_engine
import logging
import sys
from config import DATABASE_CONFIG, CSV_FILES, LOG_FILE

# Configuración de Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_db_engine(config):
    """
    Crea una conexión de motor a la base de datos MySQL.
    """
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}",
            echo=False
        )
        logging.info("Conexión a la base de datos establecida correctamente.")
        return engine
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        sys.exit(1)

def read_csv(file_path):
    """
    Lee un archivo CSV y devuelve un DataFrame de pandas.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Archivo {file_path} leído exitosamente.")
        return df
    except Exception as e:
        logging.error(f"Error al leer el archivo {file_path}: {e}")
        sys.exit(1)

def transform_customers(df):
    """
    Realiza transformaciones específicas en el DataFrame de customers.
    """
    # Ejemplo: Convertir correos electrónicos a minúsculas
    df['customer_email'] = df['customer_email'].str.lower()
    # Validar campos obligatorios
    if df[['customer_fname', 'customer_lname', 'customer_email']].isnull().any().any():
        logging.error("Datos faltantes en el DataFrame de customers.")
        sys.exit(1)
    return df

def transform_departments(df):
    """
    Realiza transformaciones específicas en el DataFrame de departments.
    """
    # Validar que department_name no tenga duplicados
    if df['department_name'].duplicated().any():
        logging.warning("Hay departamentos duplicados en el DataFrame de departments.")
    return df

def transform_categories(df, departments_df):
    """
    Realiza transformaciones específicas en el DataFrame de categories.
    """
    # Asegurar que category_department_id exista en departments
    valid_ids = set(departments_df['department_id'])
    if not df['category_department_id'].isin(valid_ids).all():
        logging.error("Hay category_department_id que no existen en departments.")
        sys.exit(1)
    return df

def transform_products(df, categories_df):
    """
    Realiza transformaciones específicas en el DataFrame de products.
    """
    # Asegurar que product_category_id exista en categories
    valid_ids = set(categories_df['category_id'])
    if not df['product_category_id'].isin(valid_ids).all():
        logging.error("Hay product_category_id que no existen en categories.")
        sys.exit(1)
    return df

def transform_orders(df, customers_df):
    """
    Realiza transformaciones específicas en el DataFrame de orders.
    """
    # Convertir order_date a datetime
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    if df['order_date'].isnull().any():
        logging.error("Hay valores inválidos en order_date.")
        sys.exit(1)
    # Asegurar que order_customer_id exista en customers
    valid_ids = set(customers_df['customer_id'])
    if not df['order_customer_id'].isin(valid_ids).all():
        logging.error("Hay order_customer_id que no existen en customers.")
        sys.exit(1)
    return df

def transform_order_items(df, orders_df, products_df):
    """
    Realiza transformaciones específicas en el DataFrame de order_items.
    """
    # Asegurar que order_item_order_id exista en orders
    valid_order_ids = set(orders_df['order_id'])
    if not df['order_item_order_id'].isin(valid_order_ids).all():
        logging.error("Hay order_item_order_id que no existen en orders.")
        sys.exit(1)
    # Asegurar que order_item_product_id exista en products
    valid_product_ids = set(products_df['product_id'])
    if not df['order_item_product_id'].isin(valid_product_ids).all():
        logging.error("Hay order_item_product_id que no existen en products.")
        sys.exit(1)
    # Calcular order_item_subtotal si no está presente o está incorrecto
    calculated_subtotal = df['order_item_quantity'] * df['order_item_product_price']
    if not (df['order_item_subtotal'] == calculated_subtotal).all():
        logging.info("Recalculando order_item_subtotal.")
        df['order_item_subtotal'] = calculated_subtotal
    return df

def load_data(engine, table_name, df, if_exists='append'):
    """
    Carga un DataFrame de pandas a una tabla de MySQL.
    """
    try:
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)
        logging.info(f"Datos cargados exitosamente en la tabla {table_name}.")
    except Exception as e:
        logging.error(f"Error al cargar datos en la tabla {table_name}: {e}")
        sys.exit(1)

def main():
    # Crear conexión a la base de datos
    engine = create_db_engine(DATABASE_CONFIG)
    
    # Orden de carga para respetar las dependencias de claves foráneas
    load_order = ['departments', 'categories', 'customers', 'products', 'orders', 'order_items']
    
    # Diccionario para almacenar DataFrames transformados
    dataframes = {}
    
    # Leer y transformar cada tabla
    # 1. Departments
    departments_df = read_csv(CSV_FILES['departments'])
    departments_df = transform_departments(departments_df)
    dataframes['departments'] = departments_df
    
    # 2. Categories
    categories_df = read_csv(CSV_FILES['categories'])
    categories_df = transform_categories(categories_df, departments_df)
    dataframes['categories'] = categories_df
    
    # 3. Customers
    customers_df = read_csv(CSV_FILES['customers'])
    customers_df = transform_customers(customers_df)
    dataframes['customers'] = customers_df
    
    # 4. Products
    products_df = read_csv(CSV_FILES['products'])
    products_df = transform_products(products_df, categories_df)
    dataframes['products'] = products_df
    
    # 5. Orders
    orders_df = read_csv(CSV_FILES['orders'])
    orders_df = transform_orders(orders_df, customers_df)
    dataframes['orders'] = orders_df
    
    # 6. Order Items
    order_items_df = read_csv(CSV_FILES['order_items'])
    order_items_df = transform_order_items(order_items_df, orders_df, products_df)
    dataframes['order_items'] = order_items_df
    
    # Cargar datos en MySQL en el orden correcto
    for table in load_order:
        load_data(engine, table, dataframes[table], if_exists='append')
    
    logging.info("Pipeline de datos ejecutado exitosamente.")

if __name__ == "__main__":
    main()
