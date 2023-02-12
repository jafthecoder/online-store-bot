import sqlite3


def insert_user(telegram_id, full_name, age, contact):
    database = sqlite3.connect('silverbot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name, age, contact)
    VALUES (?,?,?,?)
    ''', (telegram_id, full_name, age, contact))
    database.commit()
    database.close()


def get_all_users():
    database = sqlite3.connect('silverbot.db')
    cursor = database.cursor()
    cursor.execute('''
         SELECT telegram_id FROM users;

       ''')
    users = cursor.fetchall()
    users_tg_id = []

    for user in users:
        users_tg_id.append(user[0])

    database.close()

    return users_tg_id


def get_user_data(telegram_id):
    database = sqlite3.connect('silverbot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users
    WHERE telegram_id = ?
    ''', (telegram_id,))

    user_data = cursor.fetchone()
    database.close()
    return user_data

def get_all_categories():
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT category_name FROM categories;
    ''')
    categories = cursor.fetchall()
    ctg_list = []
    for c in categories:
        ctg_list.append(c[0])
    database.close()
    return ctg_list

def get_category_id(category_name):
    database = sqlite3.connect('silverbot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT category_id FROM categories 
    WHERE category_name = ?
    ''', (category_name,))

    category_id_from_name = cursor.fetchone()[0]
    database.close()
    return category_id_from_name


def get_all_products():
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name FROM products;
    ''')
    products = cursor.fetchall()
    prd_list = []
    for c in products:
        prd_list.append(c[0])
    database.close()
    return prd_list

def get_category_image(category_name):
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT category_image FROM categories
    WHERE category_name = ?
    ''', (category_name,))
    category_image = cursor.fetchone()[0]
    database.close()
    return category_image


def get_product_image1(product_name):
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_image1 FROM products
    WHERE category_name = ?
    ''', (product_name,))
    product_image = cursor.fetchone()[0]
    database.close()
    return product_image

def get_product_image2(product_name):
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_image2 FROM products
    WHERE category_name = ?
    ''', (product_name,))
    product_image = cursor.fetchone()[0]
    database.close()
    return product_image

def get_desc(product_name):
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_description FROM products
    WHERE product_name = ?
    ''', (product_name))

