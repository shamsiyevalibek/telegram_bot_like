from telegram.ext import (
    Updater,
    MessageHandler,
    CallbackContext,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)

lst = []
g_dislike = 0
d_like = 0


def start(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id

    bot = context.bot

    keyboard1 = InlineKeyboardButton(
        f"dislike 👎 {g_dislike}", callback_data=f"1dislike"
    )
    keyboard2 = InlineKeyboardButton(f"like 👍 {d_like}", callback_data=f"1like")
    reply_markup = InlineKeyboardMarkup(
        [
            [keyboard1, keyboard2],
        ]
    )

    bot.send_message(
        chat_id=chat_id,
        text="Hello @" + update.message.chat.username,
        reply_markup=reply_markup,
    )


def query(update: Update, context: CallbackContext):
    if update.callback_query:
        global g_dislike
        global d_like
        chat_id = update.callback_query.message.chat_id

        button = update.callback_query.data

        # Example: answer the callback query to avoid Telegram client loading icon
        if chat_id not in lst:
            if "dislike" in button:
                g_dislike += 1
            else:
                d_like += 1

            keyboard1 = InlineKeyboardButton(
                f"dislike 👎 {g_dislike}",
                callback_data="1dislike",
            )
            keyboard2 = InlineKeyboardButton(
                f"like 👍 {d_like}", callback_data=f"1like"
            )
            reply_markup = InlineKeyboardMarkup(
                [
                    [keyboard1, keyboard2],
                ]
            )
            update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        lst.append(chat_id)


dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler(command="start", callback=start))
dispatcher.add_handler(CallbackQueryHandler(callback=query, pattern="1"))


updater.start_polling()
updater.idle()
