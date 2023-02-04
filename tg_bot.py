import os
import logging
import redis
import moltin
from database import get_database_connection
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from pprint import pprint

# cd C:\Users\Public\Documents\Python_Programming\Chat_bots\tg_fish_shop
def start(update, context):
    products = moltin.fetch_products()
    keyboard = []
    print(products)
    for name, product_id in products:
        product_button = [InlineKeyboardButton(name, callback_data=product_id)]
        keyboard.append(product_button)
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return 'HANDLE_MENU'


def handle_menu(update, context):
    query = bot.callback_query
    pritn(update)
    product_info = f"{product_name} \n {sellary}\n{weight}\n{description}"
    print(query.data)
    print(11)
    print(query.message.message_id)

    update.message.reply_text(product_info, reply_markup=reply_markup)
    # context.bot.send_message(query.message.chat_id, text="Send")
    # context.bot.delete_message(query.message.chat_id, query.message.message_id)
    redis_db.hset(str(update.message.chat_id), 'current_product', query.data)
    


def echo(update, context):
    """
    Хэндлер для состояния ECHO.
    
    Бот отвечает пользователю тем же, что пользователь ему написал.
    Оставляет пользователя в состоянии ECHO.
    """
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(update, context):
    """
    Функция, которая запускается при любом сообщении от пользователя и решает как его обработать.
    Эта функция запускается в ответ на эти действия пользователя:
        * Нажатие на inline-кнопку в боте
        * Отправка сообщения боту
        * Отправка команды боту
    Она получает стейт пользователя из базы данных и запускает соответствующую функцию-обработчик (хэндлер).
    Функция-обработчик возвращает следующее состояние, которое записывается в базу данных.
    Если пользователь только начал пользоваться ботом, Telegram форсит его написать "/start",
    поэтому по этой фразе выставляется стартовое состояние.
    Если пользователь захочет начать общение с ботом заново, он также может воспользоваться этой командой.
    """
    #db = get_database_connection()
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = 'HANDLE_MENU'
        user_state = redis_db.hget(str(chat_id), 'next_state', user_state).decode("utf-8")
    states_functions = {
        'START': start,
        'HANDLE_MENU': handle_menu,
        'STOP':stop,
    }
    state_handler = states_functions[user_state]
    # Если вы вдруг не заметите, что python-telegram-bot перехватывает ошибки.
    # Оставляю этот try...except, чтобы код не падал молча.
    # Этот фрагмент можно переписать.
    try:
        next_state = state_handler(update, context)
        print(next_state)
        redis_db.hset(str(chat_id), 'next_state', next_state)
    except Exception as err:
        print(err)


def stop(update, context):
    update.message.reply_text("Викторина завершена.")
    return ConversationHandler.END


if __name__ == '__main__':
    load_dotenv()
    redis_db = get_database_connection()
    updater = Updater(os.environ["TG_TOKEN"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dp.add_error_handler(error_handler)
    updater.start_polling()

    updater.idle()