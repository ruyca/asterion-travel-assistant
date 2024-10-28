# bot.py

import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    ApplicationBuilder, 
    CallbackQueryHandler, 
    CommandHandler, 
    CallbackContext,
    ContextTypes, 
    ConversationHandler, 
    MessageHandler, 
    filters
)
from dotenv import load_dotenv
from state_functions import start_lyfCare, lang, code, destination, cancel, user_conf
from other_functions import data_agreement, start, about_the_creators
from query_chatgpt import translate

from state_functions import start_translation, handle_a_to_b, handle_record_button
from state_functions import handle_voice_message, handle_continue


### STATES ###
# User Info Conf
LANG, CODE, LOCATION, DESTINATION, USER_CONF = range(0, 5)
# Full solution States
PLANNING, MOVING, EXPLORING, EMERGENCY, END = range(5, 10)  

# Translation States
A_TO_B = 50  # User A sends message
PLAY_AND_RECORD = 51  # Bot plays translation and records B's response
SHOW_TRANSLATION = 52  # Show translation to User A and ask to continue

load_dotenv()
TEL_TOKEN = os.getenv("TELEGRAM_TOKEN")
TRIPADVISOR_TOKEN = os.getenv("TRIP_TOKEN") 
USER_LANGUAGE = "English"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO, 
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Update your conversation handler
translation_handler = ConversationHandler(
    entry_points=[CommandHandler('start_translation', start_translation)],
    states={
        A_TO_B: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_a_to_b)
        ],
        PLAY_AND_RECORD: [
            CallbackQueryHandler(handle_record_button, pattern='^record$'),
            MessageHandler(filters.VOICE, handle_voice_message)
        ],
        SHOW_TRANSLATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_continue)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TEL_TOKEN).build()
    print("HERE")
    
    # handlers for commands
    start_handler = CommandHandler('start', start)
    data_handler = CommandHandler('data_agreement', data_agreement)
    creators_handler = CommandHandler('about_the_creators', about_the_creators)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_lyfCare', start_lyfCare)],
        states = {
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang)],
            CODE: [CallbackQueryHandler(code)],
            DESTINATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, destination)],
            USER_CONF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, user_conf),
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers in the correct order
    application.add_handler(translation_handler)
    application.add_handler(conv_handler)
    application.add_handler(start_handler)
    application.add_handler(data_handler)
    application.add_handler(creators_handler)
    
    application.run_polling()