import sqlite3

database = sqlite3.connect('silverbot.db')
cursor = database.cursor()

def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT UNIQUE,
        full_name TEXT,
        age TEXT,
        contact TEXT
    )
    ''')

create_users_table()

def create_categories_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE,
        category_image TEXT
    )
    ''')

create_categories_table()

def create_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_image1 TEXT,
        product_image2 TEXT,
        product_video TEXT,
        product_description TEXT,
        product_price DECIMAL(10, 2),
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    )
    ''')

create_products_table()



database.commit()
database.close()


