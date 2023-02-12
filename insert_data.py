import sqlite3

def insert_new_ctg_data(category_name, category_image):
    database = sqlite3.connect("silverbot.db")
    cursor = database.cursor()
    cursor.execute('''
       INSERT INTO categories(category_name, category_image)
       VALUES(?, ?)
       ''', (category_name, category_image))
    database.commit()
    database.close()

def insert_products(product_name, product_image1, product_image2, product_video, product_description, category_id):
    database = sqlite3.connect('silverbot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(product_name, product_image1, product_image2, product_video, product_description, category_id)
    VALUES (?,?,?,?,?,?)
    ''', (product_name, product_image1, product_image2, product_video, product_description, category_id))
    database.commit()
    database.close()