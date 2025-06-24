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
from tinydb import TinyDB,Query
load_dotenv()
token=os.getenv('token')
updater=Updater(token=token)
dispatcher=updater.dispatcher
def start(update:Update,context:CallbackContext):
    context=context.bot
    chat_id=update.message.chat_id
    user_name=update.message.from_user.first_name
    db=TinyDB('alibek.json')
    user=Query()
    if not db.search(user.chat_id==chat_id):
        db.insert({'chat_id':chat_id,'username':user_name})
    

    context.send_message(
        chat_id=chat_id,
        text="Hello @" + update.message.chat.username,)
    
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()