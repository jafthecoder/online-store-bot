from telebot.types import ReplyKeyboardMarkup, KeyboardButton


from queries import *

def generate_signin_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = KeyboardButton(text="Ro'yxatdan o'tish 📝✅")
    markup.add(btn)
    return markup



def generate_send_contact_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_send_btn = KeyboardButton(text="Telefon raqamini jo'natish 📲", request_contact=True)
    markup.row(btn_send_btn)
    return markup


def generate_submit_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_yes = KeyboardButton(text="Ha✅")
    btn_no = KeyboardButton(text="Yo'q❌")
    markup.row(btn_yes, btn_no)
    return markup

def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_menu = KeyboardButton(text="Tovarlar 💍")
    btn_help = KeyboardButton(text="Yordam 🆘")
    btn_feedback = KeyboardButton(text="Fikr bildirish ✍")
    btn_call = KeyboardButton(text='Aloqaga chiqish 📞📲')
    markup.row(btn_menu)
    markup.row(btn_help, btn_call)
    markup.row(btn_feedback)
    return markup

def generate_back_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_back = KeyboardButton(text="⬅Ortga")
    markup.add(btn_back)
    return markup

def generate_categories_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = get_all_categories()
    btn_back = KeyboardButton(text='Bosh Menyu⏫')
    markup.add(*categories)
    markup.add(btn_back)
    return markup

def generate_ctg_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_add_ctg = KeyboardButton(text="Yangi Kategoriya🆕")
    btn_add_product = KeyboardButton(text="Yangi Tovar💍🆕")
    btn_rassilka = KeyboardButton(text="Xabarnoma jo'natish ✉")
    markup.add(btn_add_ctg, btn_add_product, btn_rassilka)
    return markup

def generate_category_products(category_name):
    markup = ReplyKeyboardMarkup(row_width=3)
    products = get_all_products()
    markup.add(*products)
    return markup

def generate_rassilka():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    text_btn = KeyboardButton(text="Text 📄")
    image_btn = KeyboardButton(text='Picture 🖼')
    video_btn = KeyboardButton(text='Video 🎥')
    video_text = KeyboardButton(text='Video🎥 + text📄')
    picture_text = KeyboardButton(text='Picture🖼 + text📄')
    markup.add(text_btn, image_btn, video_btn, picture_text, video_text )
    return markup