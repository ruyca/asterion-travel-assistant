from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from query_chatgpt import translate
from nearest_lyf import calculate_distance, find_closest_locations


### STATES ###
# User Info Conf
LANG, CODE, LOCATION, DESTINATION = range(0, 4)
# Full solution States
PLANNING, MOVING, EXPLORING, EMERGENCY, END = range(4, 9)  

async def print_lyf_locations(update: Update, context: ContextTypes.DEFAULT_TYPE, locations: list,
                                language: str) -> None:
    """Prints the closets Lyf locations relative to the users location
        Locations = [(name, address, distance, photo), ...] -> len = 3
    """
    p = "<b>Here are the closest Lyf locations, reserved in any of them!</b>"
    t_p = translate(p, language)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = (t_p),
        parse_mode = "HTML"
    )

    for cont, location in enumerate(locations):

        loc_name = location[0]
        loc_adr = location[1]
        loc_dist = location[2]
        loc_photo = location[3]

        # Loc photo
        await context.bot.send_photo(chat_id=update.effective_chat.id,photo=loc_photo)
        p = f"<b>{cont + 1}.- {loc_name}</b>\n\n"

        adr_trans = translate("Address", language)
        p1 = f"• <b>{adr_trans}: <em>{loc_adr}</em></b>\n"
        dist_trans = translate("Distance", language)
        p2 = f"• <b>{dist_trans}: <em>{loc_dist}</em></b> km\n"
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                        text = (p+p1+p2),
                                        parse_mode = "HTML")


# ENTRY POINT
async def start_lyfCare(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Starts the conversation. Displays how to use the solution."""

    await update.message.reply_text(
        '<b>This is LyfCare: your all-around-safety solution by Lyf</b>\n\n'
        'Here is the general workflow of how the solution works:\n'
        '1.- Set the language you would like me to write in.\n'
        '2.- Provide your personalized LyfToken to enable this service (or get one!)\n'
        '3.- Answer some quick information that will help us provide better service.\n'
        '4.- With my help, plan your next trip! (I will be available in case of any trouble)\n'
        '5.- Explore freely the city! I will help you stay on safe zones and contact any emergency \
        authorities (LyfStaff) in need be.',
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup([["Lets go!"]], one_time_keyboard=True, resize_keyboard=True)
    )

    return LANG


# STATE 0
async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the language the bot will be conversing. Resets when exiting States"""
    
    # Define inline buttons for language selection
    keyboard = [
        [InlineKeyboardButton('Spanish', callback_data='Spanish')],
        [InlineKeyboardButton('English', callback_data='English')],
        [InlineKeyboardButton('Simplified Chinese', callback_data='Simplified Chinese')],
        [InlineKeyboardButton('Hindi', callback_data='Hindi')],
        [InlineKeyboardButton('Malay', callback_data='Malay')],
        [InlineKeyboardButton('Arabic', callback_data='Arabic')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('<b>Click the language you would like me to speak in 👇</b>', parse_mode='HTML', reply_markup=reply_markup)

    return CODE


# STATE 1
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authenticates the user reservation code. If incorrect or doesn't have one"""

    query = update.callback_query
    await query.answer()

    selected_lang = query.data
    context.user_data["language"] = selected_lang  # Saves the language 

    phrase = f"Perfect! From now on we will speak in <b>{selected_lang}</b>"
    # If the selected lang is different from English, we translate
    translated_phrase = translate(phrase, selected_lang) 

    await query.edit_message_text(
        text=translated_phrase,
        parse_mode="HTML"
    )

    # Ask for user location so we can recommend closests Lyf
    phrase = "Now, can you please <b>share your location</b>\
    so we can help you find your closest Lyf location."
    translated_phrase = translate(phrase, selected_lang)

    # Use query.message.reply_text when update.message is None
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=translated_phrase, parse_mode="HTML")

    return DESTINATION


# STATE 2
async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Brings the top 3 closests Lyf destinations and asks"""

    selected_lang = context.user_data.get("language")
    
    if update.message.location: 
        user_location = update.message.location

        user_coords = (user_location.latitude, user_location.longitude)
        closests_locs = find_closest_locations(user_coords, 50)
        await print_lyf_locations(update, context, closests_locs, selected_lang)
        
        

    return ConversationHandler.END


