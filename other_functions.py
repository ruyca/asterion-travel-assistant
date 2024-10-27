from telegram import Update
from telegram.ext import ContextTypes


# DATA AGREEMENT
async def data_agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays our data agreement policies."""

    document_path = 'Data Disclosure Agreement for LyfCare.pdf'

    await update.message.reply_text("Please read the following DataAgreement:\n")
    await update.message.reply_document(
        document=open(document_path, 'rb'),  # Opening the document in read-binary mode
        caption="LyfCare Data Agreement",  # Optional caption
    )
    

# GREETING MSSG
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initial command. Displays a list of available commands and starts conversation"""

    photo_path = "images/lyf_care.png"
    await update.message.reply_photo(photo_path)
    await update.message.reply_text(
        '<b>Welcome to LyfCare!</b>\n'
        'We are delighted to have you here. LyfCare is your trusted companion for safe travel and recommendations.\n\n'
        'Here are some functions you can run:\n'
        '• /start - Show this menu again \n'
        '• /start_lyfCare - Use our full solution (travel guardian, translator, place reccomendation)\n'       
        '• /about_the_creators - Learn about the team behind LyfCare\n'
        '• /get_recommendations - Get safe and popular travel destinations\n'
        '• /data_agreement - Read our data agreement\n\n'
        'Feel free to explore and let us know how we can assist you!',
        parse_mode='HTML',
    )

async def about_the_creators(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays information about the creators"""
    
    animation_path = "images/introduction.gif"
    
    # Send the GIF first
    with open(animation_path, 'rb') as animation:
        await context.bot.send_animation(chat_id=update.effective_chat.id, animation=animation)

    # Then send the text with information about the creators
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Meet the talented minds behind our project!\n\n"
            "Together, they bring a wealth of expertise and passion for innovation, technology, and problem-solving.\n"

            "Ruy Cabello Cuahutle\n"
            "💼 <em>Systems Reliability Engineer</em>\n"
            "<code>I started with competitive programming, and since then, I’ve become addicted to hackathons. "
            "In my free time, I enjoy exploring new technologies and staying up to date with the latest innovations.</code>\n"
            "🔗 <a href='https://www.linkedin.com/in/ruy-cabello-683630200/'>LinkedIn</a>\n\n"

            "Alejandro Grimaldo Gutiérrez\n"
            "📱 <em>Computer Engineering Student</em>\n"
            "<code>Passionate about web and mobile programming, I love tackling new technological challenges. "
            "I’m motivated to work on projects that promote innovation and develop impactful technological solutions.</code>\n"
            "🔗 <a href='https://www.linkedin.com/in/alejandrogrimaldo/'>LinkedIn</a>\n\n"

            "Sergio Bruno Ramírez Gutiérrez\n"
            "💻 <em>Computer Engineering Student</em>\n"
            "<code>My passion for challenges, innovation, and continuous learning led me to the fascinating world of computing. "
            "Hackathons have become an essential part of my daily life!</code>\n"
            "🔗 <a href='https://www.linkedin.com/in/sergiobrunoramirez/'>LinkedIn</a>\n\n"

            "Daniel Mendez Carrasco\n"
            "🔌 <em>Mechatronic and Electrical Engineering Student</em>\n"
            "<code>Aspiring entrepreneur at Asterion Energy, with a great passion for sustainable technology, AI/ML, and finance. "
            "Additionally, music is my escape!</code>\n"
            "<blockquote>Have an amazing present and conquer the world.</blockquote>\n"
            "🔗 <a href='https://www.linkedin.com/in/daniel-m%C3%A9ndez-carrasco-426564172/'>LinkedIn</a>\n"
        ),
        parse_mode='HTML'
    )
