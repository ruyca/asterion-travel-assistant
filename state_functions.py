#state_functions.py

from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    ReplyKeyboardRemove
)

from telegram.ext import ContextTypes, ConversationHandler
from query_chatgpt import translate
from nearest_lyf import calculate_distance, find_closest_locations
from tinydb import TinyDB, Query
from live_translation import text_audio_request, transcribe_audio

import os

# Initialize the database
db = TinyDB('users_db.json')

### STATES ###
# User Info Conf
LANG, CODE, LOCATION, DESTINATION, USER_CONF = range(0, 5)
# Full solution States
PLANNING, MOVING, EXPLORING, EMERGENCY, END = range(5, 10)  
# Translation States
A_TO_B, PLAY_AND_RECORD, SHOW_TRANSLATION = range(50, 53)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user_lang = context.user_data.get("language", "English")
    message = translate("Bye! Hope to talk to you again soon.", user_lang)
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


### Live Translation States ###

async def start_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the translation conversation and set up initial language."""
    user_lang = context.user_data.get("language", "English")
    
    message = translate(
        "This is the live translation service. Please enter the message you want to translate to English:",
        user_lang
    )
    
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return A_TO_B

async def handle_a_to_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle User A's message and create English translation."""
    user_lang = context.user_data.get("language", "English")
    message = update.message.text
    
    try:
        # Translate message to English
        translated_message = translate(message, target="English", forced=True)
        
        # Generate audio from translated message
        audio_path = text_audio_request(translated_message)
        
        # Prepare response messages in user's language
        audio_caption = translate(
            f"Play this audio for the English speaker. The translation is:\n\n{translated_message}\n\n"
            "After playing, press the 'Record Audio' button to record their response.",
            user_lang
        )
        
        # Send the audio to User A
        with open(audio_path, 'rb') as audio:
            await update.message.reply_voice(
                audio,
                caption=audio_caption
            )
        
        # Create a keyboard for recording
        record_button_text = translate("Record Audio", user_lang)
        keyboard = [[InlineKeyboardButton(record_button_text, callback_data='record')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        record_prompt = translate(
            "Press 'Record Audio' when you're ready to record their response:",
            user_lang
        )
        await update.message.reply_text(record_prompt, reply_markup=reply_markup)
        
        # Clean up
        os.remove(audio_path)
        return PLAY_AND_RECORD
        
    except Exception as e:
        error_message = translate(f"Error processing message: {str(e)}", user_lang)
        await update.message.reply_text(error_message)
        return ConversationHandler.END

async def handle_record_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the record button press."""
    user_lang = context.user_data.get("language", "English")
    query = update.callback_query
    await query.answer()
    
    message = translate(
        "Send a voice message with their response (record it within Telegram).",
        user_lang
    )
    await query.message.reply_text(message)
    return PLAY_AND_RECORD

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the recorded voice message."""
    user_lang = context.user_data.get("language", "English")
    
    if not update.message.voice:
        message = translate("Please send a voice message.", user_lang)
        await update.message.reply_text(message)
        return PLAY_AND_RECORD
    
    try:
        # Download voice message
        voice = await update.message.voice.get_file()
        voice_path = "temp_voice.ogg"
        await voice.download_to_drive(voice_path)
        
        # Transcribe audio
        transcribed_text = transcribe_audio(voice_path)
        if transcribed_text is None:
            message = translate("Failed to transcribe audio. Please try again.", user_lang)
            await update.message.reply_text(message)
            return PLAY_AND_RECORD
        
        # Translate from English to user's language
        translated_response = translate(transcribed_text, target=user_lang)
        
        # Send translation to user
        continue_prompt = translate(
            f"Their response: {translated_response}\n\nWould you like to continue the conversation? (Yes/No)",
            user_lang
        )
        await update.message.reply_text(continue_prompt)
        
        # Clean up
        os.remove(voice_path)
        return SHOW_TRANSLATION
        
    except Exception as e:
        error_message = translate(f"Error processing voice message: {str(e)}", user_lang)
        await update.message.reply_text(error_message)
        return ConversationHandler.END

async def handle_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle whether the user wants to continue the conversation."""
    user_lang = context.user_data.get("language", "English")
    response = update.message.text.lower()
    
    yes_translations = {
        'yes': True, 'y': True,
        'sí': True, 'si': True,
        '是的': True,
        'हाँ': True,
        'ya': True,
        'نعم': True
    }
    
    if yes_translations.get(response, False):
        message = translate("Please enter your next message:", user_lang)
        await update.message.reply_text(message)
        return A_TO_B
    else:
        message = translate(
            "Ending conversation. Thank you for using the translation service!",
            user_lang
        )
        await update.message.reply_text(message)
        return ConversationHandler.END

def validate_registration(code):
    reservation_codes = [user['reservation_code'] for user in db.all()]
    if code in reservation_codes:
        return True
    else: return False

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
        '2.- Provide your reservation code previously booked in Lyf Website.\n'
        '3.- Get our personalized, high availability help from the moment you land.\n'
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

    # Ask for the database so we can get the user info. 
    phrase = "Please provide your <b>reservation code</b> from your Lyf registration."
    translated_phrase = translate(phrase, selected_lang)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=translated_phrase, parse_mode="HTML")

    # Ask for user location so we can recommend closests Lyf
    #phrase = "Now, can you please <b>share your location</b>\
    #so we can help you find your closest Lyf location."
    #translated_phrase = translate(phrase, selected_lang)

    # Use query.message.reply_text when update.message is None
    #await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text=translated_phrase, parse_mode="HTML")

    return DESTINATION


# STATE 2
async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Brings the top 3 closests Lyf destinations and asks"""

    selected_lang = context.user_data.get("language")
    registration_code = update.message.text
    context.user_data["registration_code"] = registration_code # KEYYYYY 'AB294' for Ruy Cabello

    if validate_registration(registration_code):
        # Registation code successful
        print("THE CORRECT IS CORRECT")
        # Code is correct, continue with travel logic
        t1 = "Yes, the information is correct"
        t2 = "No, there is an error"

        t1_t = translate(t1, selected_lang)
        t2_t = translate(t2, selected_lang)

        keyboard = [[t1_t], [t2_t]]
        User = Query()
        user_entry = db.get(User.reservation_code == registration_code)
        user_name = user_entry['user_name']
        user_country = user_entry['country_origin']
        user_reservation_date = user_entry['reservation_date']
        user_flight_code = user_entry['flight_code']

        txt = f'Welcome back <b>{user_name}</b>\n\n'
        'Here is your information:\n'
        f'-> Country of origin: <b>{user_country}</b>\n'
        f'-> Reservation date <b>{user_reservation_date}</b>\n'
        f'-> Flight code: <b>{user_flight_code}</b>'
    
        txt_t = translate(txt, selected_lang) 

        await update.message.reply_text(
            txt_t,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

        return USER_CONF
    else:
        # Registration code unsuccesful 
        phrase = "Registration code incorrect. Please consider registering."
        translated_phrase = translate(phrase, selected_lang)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=translated_phrase, parse_mode="HTML")
        return ConversationHandler.END




async def user_conf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the selected language from the user data
    selected_lang = context.user_data.get("language")
    t = translate("Thank you, consider using", selected_lang)
    # Send confirmation message to the user
    await update.message.reply_text(f"{t} \\start_translation")

    return ConversationHandler.END