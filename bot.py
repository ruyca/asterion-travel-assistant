import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv

from state_functions import start_lyfCare, lang, code, destination

from other_functions import data_agreement, start, about_the_creators

### STATES ###
# User Info Conf
LANG, CODE, LOCATION, DESTINATION = range(0, 4)
# Full solution States
PLANNING, MOVING, EXPLORING, EMERGENCY, END = range(4, 9)  


load_dotenv()
TEL_TOKEN = os.getenv("TELEGRAM_TOKEN")
TRIPADVISOR_TOKEN = os.getenv("TRIP_TOKEN") ##
USER_LANGUAGE = "English"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO, handlers=[logging.FileHandler("app.log"), 
                                                    logging.StreamHandler()])
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    
    application = ApplicationBuilder().token(TEL_TOKEN).build()

    # handlers for commands
    start_handler = CommandHandler('start', start)
    data_handler = CommandHandler('data_agreement', data_agreement)
    creators_handler = CommandHandler('about_the_creators', about_the_creators)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_lyfCare', start_lyfCare)],
        states = {
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang)],
            CODE: [CallbackQueryHandler(code)],
            DESTINATION: [MessageHandler(filters.LOCATION, destination)]
        },
        fallbacks=[]
    )


    application.add_handler(conv_handler)
    application.add_handler(start_handler)
    application.add_handler(data_handler)
    application.add_handler(creators_handler)
    
    application.run_polling()

