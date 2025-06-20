from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)
dispatcher = updater.dispatcher

g_dislike = 0
d_like = 0

dct = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    bot = context.bot

    keyboard1 = InlineKeyboardButton(
        f"dislike 👎 {g_dislike}", callback_data="1dislike"
    )
    keyboard2 = InlineKeyboardButton(
        f"like 👍 {d_like}", callback_data="1like"
    )
    reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

    bot.send_message(
        chat_id=chat_id,
        text="Hello @" + update.message.chat.username,
        reply_markup=reply_markup,
    )

def query(update: Update, context: CallbackContext):
    global g_dislike, d_like

    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        button = update.callback_query.data 

        if button == '1like':
            current_choice = 'like'
        elif button == '1dislike':
            current_choice = 'dislike'
        else:
            return

        previous_choice = dct.get(chat_id, None)

        if previous_choice == current_choice:
            return 

        if previous_choice == 'like':
            d_like -= 1
        elif previous_choice == 'dislike':
            g_dislike -= 1

        if current_choice == 'like':
            d_like += 1
        else:
            g_dislike += 1

        dct[chat_id] = current_choice

        keyboard1 = InlineKeyboardButton(
            f"dislike 👎 {g_dislike}", callback_data="1dislike"
        )
        keyboard2 = InlineKeyboardButton(
            f"like 👍 {d_like}", callback_data="1like"
        )
        reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(callback=query, pattern="1"))

updater.start_polling()
updater.idle()
