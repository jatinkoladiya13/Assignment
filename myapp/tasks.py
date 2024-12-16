import threading
from myapp.models import User, Order, Product
import sqlite3

users_data = [
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com'),
    (3, 'Charlie', 'charlie@example.com'),
    (4, 'David', 'david@example.com'),
    (5, 'Eve', 'eve@example.com'),
    (6, 'Frank', 'frank@example.com'),
    (7, 'Grace', 'grace@example.com'),
    (8, 'Alice', 'alice@example.com'),
    (9, 'Henry', 'henry@example.com'),
    (10, 'Jane', 'jane@example.com')
]

products_data = [
    (1, 1, 2),  
    (2, 2, 1),
    (3, 3, 5),
    (4, 4, 1),
    (5, 5, 3),
    (6, 6, 4),
    (7, 7, 2),
    (8, 8, 0),
    (9, 9, -1),
    (10, 10, 2)
]

orders_data = [
    (1, 1, 2),  
    (2, 2, 1),
    (3, 3, 5),
    (4, 4, 1),
    (5, 5, 3),
    (6, 6, 4),
    (7, 7, 2),
    (8, 8, 0),
    (9, 9, -1),
    (10, 10, 2)
]

def insert_into_db(db_name, table_name, data):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        if table_name == 'users':
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                email TEXT)''')
        elif table_name == 'products':
            cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                price REAL)''')
        elif table_name == 'orders':
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                product_id INTEGER,
                                quantity INTEGER)''')

        insert_query = f"INSERT OR IGNORE INTO {table_name} VALUES (?,?,?)"
        if table_name == 'orders':
            # For orders, omit the `id` column, as it is auto-incremented
            insert_query = "INSERT OR IGNORE INTO orders (user_id, product_id, quantity) VALUES (?,?,?)"
            cursor.executemany(insert_query, data)
        else:
            cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Successfully inserted into {db_name}/{table_name}") 

    except Exception as e:
        print(f"Error inserting into {db_name}/{table_name}: {e}")
    finally:
        conn.close()     

def run_insertions():
    threads = []

    threads.append(threading.Thread(target=insert_into_db, args=('users.db', 'users', users_data)))

    threads.append(threading.Thread(target=insert_into_db, args=('products.db', 'products', products_data)))
    
    threads.append(threading.Thread(target=insert_into_db, args=('orders.db', 'orders', orders_data)))

    for thread in threads:
        thread.start()
    
    
    for thread in threads:
        thread.join()

run_insertions()    