from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove, InputMediaPhoto
from telebot.apihelper import ApiTelegramException
import time

from configs import *
from keyboards import *
from queries import *
from insert_data import insert_new_ctg_data, insert_products

bot = TeleBot(token=TOKEN, parse_mode='HTML')

users_data = {}
products_data = {}
categories_data = {}


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    users = get_all_users()
    if user_id == ADMIN_ID:
        ask_to_choose()
    elif user_id in users:
        main_menu(message)
    else:
        bot.send_message(user_id, f"""Assalamu alaykum Hurmatli foydalanuvchi <i>{full_name}</i> !!!""")
        bot.send_message(user_id, f"""Ushbu botdan to'liq foydalanish uchun iltimos ro'yxatdan o'ting 📝😊""",
                         reply_markup=generate_signin_button())


@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish 📝✅")
def ask_full_name(message: Message):
    global users_data
    user_id = message.from_user.id
    users_data[user_id] = {
        "user_id": user_id
    }
    msg = bot.send_message(user_id, "Ism va familyangizni kiriting: ",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_age)


def ask_age(message: Message):
    global users_data
    user_id = message.from_user.id
    full_name = message.text
    users_data[user_id].update({"full_name": full_name})
    msg = bot.send_message(user_id, "Yoshingizni kiriting: ")
    bot.register_next_step_handler(msg, ask_contact)


def ask_contact(message: Message):
    global users_data
    user_id = message.from_user.id
    age = message.text
    users_data[user_id].update({"age": age})
    print(users_data)
    msg = bot.send_message(user_id, "Telefon raqamingizni jo'nating !!!", reply_markup=generate_send_contact_btn())

    bot.register_next_step_handler(msg, show_data)


def show_data(message: Message):
    global users_data
    user_id = message.from_user.id
    if message.content_type == 'contact':
        contact = message.contact.phone_number
        users_data[user_id].update({'contact': contact})
        print(users_data)
    elif message.content_type == 'text':
        contact = message.text
        users_data[user_id].update({'contact': contact})
        print(users_data)
    msg = bot.send_message(user_id, f"""Ism va Familya: <i>{users_data[user_id]['full_name']}</i>
Yosh: <b>{users_data[user_id]['age']}</b>
Telefon raqam: <b>{users_data[user_id]['contact']}</b>""",
                           reply_markup=generate_submit_btn())
    bot.register_next_step_handler(msg, agree_disagree)


def agree_disagree(message: Message):
    global users_data
    user_id = message.from_user.id
    if message.text == "Ha✅":
        insert_user(telegram_id=user_id, full_name=users_data[user_id]['full_name'],
                    age=users_data[user_id]['age'], contact=users_data[user_id]['contact'])
        msg = bot.send_message(user_id, "Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi❗❗❗🥳🥳🥳",
                               reply_markup=ReplyKeyboardRemove())
        main_menu(message)

    elif message.text == "Yo'q❌":
        users_data.pop(user_id)
        command_start(message)


# -------------------------------------------------------------------------------------------------
# Main menu
def main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Quyidagilardan birini tanlang:", reply_markup=generate_main_menu())


# ----------------------------------------------------------------------------------------------------------
# Products
@bot.message_handler(func=lambda message: message.text == "Tovarlar 💍")
def show_categories_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Kategoriyalardan birini tanlang:",
                     reply_markup=generate_categories_menu())


CATEGORIES = get_all_categories()


@bot.message_handler(func=lambda message: message.text in CATEGORIES or message.text == 'Bosh Menyu⏫')
def show_category_products(message: Message):
    if message.text == 'Bosh Menyu⏫':
        main_menu(message)
    else:
        global categories_data
        chat_id = message.chat.id
        category_name = message.text
        category_image = get_category_image(category_name)
        bot.send_photo(chat_id,
                       photo=category_image,
                       caption=f"Siz <i>{category_name}</i> kategoriyasini tanladingiz !"
                               f"Quyidagilardan birini tanlang❗❗❗",
                       reply_markup=generate_category_products(category_name), parse_mode='HTML')


PRODUCTS = get_all_products()


@bot.message_handler(func=lambda message: message.text in PRODUCTS)
def product_info(message: Message):
    chat_id = message.chat.id
    product_name = message.text
    product_image1 = get_product_image1(product_name)
    product_image2 = get_product_image2(product_name)
    photo_media = [InputMediaPhoto(product_image1, caption=get_desc(product_name)), InputMediaPhoto(product_image2)]
    bot.send_media_group(chat_id, photo_media)


# ---------------------------------------------------------------------------------------------------------
# Help
@bot.message_handler(func=lambda message: message.text == "Yordam 🆘")
def help(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"""Assalomu Alaykum hurmatli foydalanuvchi!!! Bizning <b>Silver Store</b>
telegram botimiz orqali siz turli xildagi bijuteriyalar haqida ma'lumotga ega bo'lishingiz mumkin✅Buning uchun esa
 Tovarlar 💍 tugmachasini bossangiz bo'ldi
Dasturchi bilan aloqaga chiqish uchun📲: https://t.me/Jaf_the_Coder""")
    time.sleep(10)
    msg = bot.send_message(chat_id, "Berilgan ma'lumot siz uchun foydali bo'ldimi ?",
                           reply_markup=generate_submit_btn())
    bot.register_next_step_handler(msg, choose_yes_no)


def choose_yes_no(message: Message):
    chat_id = message.chat.id
    if message.text == 'Ha✅':
        bot.send_message(chat_id, "Javob uchun katta rahmat😊😉")
        main_menu(message)
    elif message.text == "Yo'q❌":
        bot.send_message(chat_id, "Ok👌.Biz yana ham yaxshiroq harakat qilamiz)")
        main_menu(message)


# --------------------------------------------------------------------------------------------------
# Feedback
@bot.message_handler(func=lambda message: message.text == "Fikr bildirish ✍")
def ask_feedback(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Fikringizni yuboring: ",
                           reply_markup=generate_back_btn())
    bot.register_next_step_handler(msg, thanks_for_feedback)


def thanks_for_feedback(message: Message):
    chat_id = message.chat.id
    if message.text == '⬅Ortga':
        main_menu(message)
    else:
        feedback = message.text
        user_data = get_user_data(chat_id)
        bot.send_message(FEEDBACK_CHANNEL, f"""Ism, Familya: {user_data[2]}
Telefon raqami: {user_data[4]}
Feedback: {feedback}""")
        bot.send_message(chat_id, "Fikr-mulohazangiz uchun rahmat☺ !")
        main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Aloqaga chiqish 📞📲")
def callback(message: Message):
    chat_id = message.chat.id
    user_data = get_user_data(chat_id)
    print(user_data)
    bot.send_message(CALLBACK_CHANNEL, f"""Ism, Familya 👤: <i>{user_data[2]}</i>
Telefon raqami ☎: <b>{user_data[4]}</b>""", parse_mode='HTML')
    bot.send_message(chat_id, "Biz siz bilan tez orada aloqaga chiqamiz☺📲!")
    main_menu(message)


# ----------------------------------------------------------------------------------------------------------
# Admin part
def ask_to_choose():
    bot.send_message(ADMIN_ID, f"""Assalomu Alaykum hurmatli adminstrator❗❗❗
Quyidagilardan birini tanlang""", reply_markup=generate_ctg_admin())


@bot.message_handler(func=lambda message: message.text == "Yangi Kategoriya🆕" and message.from_user.id == ADMIN_ID)
def asc_ctg_name(message: Message):
    global categories_data
    user_id = message.from_user.id
    msg = bot.send_message(user_id, f"""<b>Yangi Kategoriya</b> nomini kiriting ❗""", parse_mode='HTML',
                           reply_markup=generate_back_btn())

    bot.register_next_step_handler(msg, ask_ctg_photo)


def ask_ctg_photo(message: Message):
    if message.text == "⬅Ortga":
        ask_to_choose()
    else:
        global categories_data
        category_name = message.text
        categories_data.update({'category_name': category_name})
        msg = bot.send_message(ADMIN_ID, f"""<b>Yangi kategoriya uchun RASM</b> jo'nating❗""", parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())

        bot.register_next_step_handler(msg, show_ctg_data)


def show_ctg_data(message: Message):
    global categories_data
    pic_id = message.photo[-1].file_id
    categories_data.update({'photo_id': pic_id})
    print(categories_data)
    msg = bot.send_message(ADMIN_ID, f"""Kategoriya nomi uzuk:{categories_data['category_name']}""",
                           parse_mode='HTML', reply_markup=generate_submit_btn())
    bot.register_next_step_handler(msg, agree_disagree_to_add)


def agree_disagree_to_add(message: Message):
    global categories_data

    if message.text == "Ha✅":
        insert_new_ctg_data(category_name=categories_data['category_name'],
                            category_image=categories_data['photo_id'])
        bot.send_message(ADMIN_ID, "🆕 Kategoriya qo'shish muvaffaqiyatli amalga oshirildi❗❗❗🥳🥳🥳",
                         reply_markup=ReplyKeyboardRemove())
        ask_to_choose()
    elif message.text == "Yo'q❌":
        ask_to_choose()


@bot.message_handler(func=lambda message: message.text == "Yangi Tovar💍🆕" and message.from_user.id == ADMIN_ID)
def ask_new_productname(message: Message):
    global products_data
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "Yangi Tovar nomini kiriting !!!", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_photo)


def ask_photo(message: Message):
    global products_data
    product_name = message.text
    products_data.update({"product_name": product_name})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, "Yangi tovar uchun 1chi rasmni jo'nating !!!")
    bot.register_next_step_handler(msg, send_product_photo1)


def send_product_photo1(message: Message):
    global products_data
    pic_id = message.photo[-1].file_id
    products_data.update({"pic_id1": pic_id})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, "Yangi tovar uchun 2chi rasmni jo'nating !!!")
    bot.register_next_step_handler(msg, send_product_photo2)


def send_product_photo2(message: Message):
    global products_data
    pic2_id = message.photo[-1].file_id
    products_data.update({'pic_id2': pic2_id})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, "Yangi tovar uchun video jo'nating !!!")
    bot.register_next_step_handler(msg, send_product_video)


def send_product_video(message: Message):
    global products_data
    vd_id = message.video.file_id
    products_data.update({"video_id": vd_id})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, "Yangi Tovar uchun tavsif jo'nating!!!")
    bot.register_next_step_handler(msg, send_product_desc)


def send_product_desc(message: Message):
    global products_data
    desc = message.text
    products_data.update({"description": desc})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, "Tovar qaysi kategoriyaga qo'shilsin ?", reply_markup=generate_categories_menu())
    bot.register_next_step_handler(msg, show_product_data)


def show_product_data(message: Message):
    global products_data
    ctg = message.text
    products_data.update({"category": ctg})
    print(products_data)
    msg = bot.send_message(ADMIN_ID, f"""Kategoriya nomi: {products_data['product_name']}
Tavsif: {products_data['description']}
Kategoriya: {products_data['category']}""", reply_markup=generate_submit_btn())
    bot.register_next_step_handler(msg, agree_disagree_to_add_product)


def agree_disagree_to_add_product(message: Message):
    global products_data
    category_id = get_category_id(products_data['category'])
    if message.text == "Ha✅":
        insert_products(product_name=products_data['product_name'],
                        product_image1=products_data['pic_id1'],
                        product_image2=products_data['pic_id2'],
                        product_video=products_data['video_id'],
                        product_description=products_data['description'],
                        category_id=category_id,
                        )
        bot.send_message(ADMIN_ID, "Yangi Tovar💍🆕 qo'shish muvaffaqiyatli amalga oshirildi❗❗❗🥳🥳🥳")
        ask_to_choose()

    elif message.text == "Yo'q❌":
        ask_to_choose()


@bot.message_handler(func=lambda message: message.text == "Xabarnoma jo'natish ✉")
def admin(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Rassilka turini tanlang!", reply_markup=generate_rassilka())


@bot.message_handler(func=lambda message: message.text == "Text 📄" and message.from_user.id == ADMIN_ID)
def ask_text_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Text 📄' rassilka uchun TEXT jo'nating")

    bot.register_next_step_handler(msg, send_text_rassilka)


def send_text_rassilka(message: Message):
    users = get_all_users()
    text = message.text
    for user_id in users:
        try:
            bot.send_message(user_id, text)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "SMS xabarnoma barchaga jo'natildi✅")
    admin(message)


@bot.message_handler(func=lambda message: message.text == "Picture 🖼" and message.from_user.id == ADMIN_ID)
def ask_text_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Picture 🖼' rassilka uchun Rasm jo'nating")

    bot.register_next_step_handler(msg, send_image_rassilka)


def send_image_rassilka(message: Message):
    users = get_all_users()
    pic_id = message.photo[-1].file_id
    for user_id in users:
        try:
            bot.send_photo(user_id, pic_id)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "Rasm barchaga jo'natildi✅")
    admin(message)


@bot.message_handler(func=lambda message: message.text == "Video 🎥" and message.from_user.id == ADMIN_ID)
def ask_vd_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Video 🎥' rassilka uchun Video jo'nating!")
    bot.register_next_step_handler(msg, send_vd_rassilka)


def send_vd_rassilka(message: Message):
    users = get_all_users()

    video_id = message.video.file_id
    for user_id in users:
        try:
            bot.send_video(user_id, video_id)
        except ApiTelegramException:
            continue
    bot.send_message(ADMIN_ID, "Video barchaga jo'natildi✅")
    admin(message)


@bot.message_handler(func=lambda message: message.text == "Picture🖼 + text📄" and message.from_user.id == ADMIN_ID)
def ask_img_text_rassilka(message: Message):
    msg = bot.send_message(ADMIN_ID, "'Picture🖼 + text📄' rassilkasi uchun 'PHOTO' jo'nating")
    bot.register_next_step_handler(msg, ask_text_img_rassilka)


def ask_text_img_rassilka(message: Message):
    user_id = message.from_user.id
    pic_id = message.photo[-1].file_id
    msg = bot.send_message(user_id, "'Picture🖼 + text📄' rassilkasi uchun 'TEXT' jo'nating")
    bot.register_next_step_handler(msg, send_image_text_rassilka, pic_id)


def send_image_text_rassilka(message: Message, pic_id):
    users = get_all_users()
    text = message.text
    try:
        for user_id in users:
            try:
                bot.send_photo(user_id, pic_id, caption=text)
            except ApiTelegramException:
                continue
        bot.send_message(ADMIN_ID, "RASM VA TEXT barchaga yuborildi✅")
        admin(message)
    except:
        bot.send_message(ADMIN_ID, "Xatolik yuz berdi!!!Qaytadan urinib ko'ring!!!")


@bot.message_handler(func=lambda message: message.text == "Video🎥 + text📄" and message.from_user.id == ADMIN_ID)
def ask_vd_text_rassilka(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, "'Video🎥 + text📄' rassilkasi uchun 'VIDEO' jo'nating",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_text_vd_rassilka)


def ask_text_vd_rassilka(message: Message):
    user_id = message.from_user.id
    video_id = message.video.file_id
    msg = bot.send_message(user_id, "'Video🎥 + text📄' rassilkasi uchun 'TEXT' jo'nating")
    bot.register_next_step_handler(msg, send_vd_text_rassilka, video_id)


def send_vd_text_rassilka(message: Message, video_id):
    users = get_all_users()
    text = message.text
    try:
        for user_id in users:
            try:
                bot.send_photo(user_id, video_id, caption=text)
            except ApiTelegramException:
                continue
        bot.send_message(ADMIN_ID, "VIDEO VA TEXT barchaga yuborildi✅")
        admin(message)
    except:
        bot.send_message(ADMIN_ID, "Xatolik yuz berdi!!!Qaytadan urinib ko'ring!!!")


bot.polling(none_stop=True)
