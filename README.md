# LyfCare Travel Assistant 🌍✈️

## About the Project
LyfCare is a comprehensive travel assistant bot developed for Lyf during the HackAngel Hackathon Finals. This intelligent Telegram bot is designed to enhance the travel experience of Lyf's guests by providing crucial services and support throughout their journey.

### Key Features
- **Multi-language Support**: Communicate seamlessly in multiple languages including English, Spanish, Chinese, Hindi, Malay, and Arabic
- **Live Translation Service**: Real-time voice and text translation to facilitate communication between travelers and locals
- **Location Services**: Find the nearest Lyf properties and get navigation assistance
- **Travel Planning**: Get personalized recommendations and assistance for trip planning
- **Emergency Support**: Quick access to emergency services and Lyf staff
- **User Authentication**: Secure access through reservation code validation

## Prerequisites
- Python 3.8+
- Telegram Bot Token (from @BotFather)
- OpenAI API Key
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lyfcare-assistant.git
cd lyfcare-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install required packages:
```bash
# Core Telegram functionality
pip install python-telegram-bot

# OpenAI integration
pip install openai

# Database management
pip install tinydb

# Audio processing
pip install sounddevice
pip install wavio
pip install playsound

# Location services
pip install geopy

# Environment variables
pip install python-dotenv

# Additional utilities
pip install pathlib
```

4. Create a `.env` file in the project root:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## Project Structure
```
lyfcare-assistant/
│
├── bot.py                 # Main bot initialization and handlers
├── state_functions.py     # State management and core functionality
├── live_translation.py    # Translation service functions
├── query_chatgpt.py      # OpenAI integration for translations
├── nearest_lyf.py        # Location services
├── users_db.json         # User database
└── .env                  # Environment variables
```

## Features in Detail

### Live Translation
The bot provides real-time translation services:
1. Text-to-text translation between multiple languages
2. Voice message translation
3. Text-to-speech for easier communication
4. Support for natural conversations between users speaking different languages

### User Authentication
- Secure login using Lyf reservation codes
- User information and preferences storage
- Session management

### Location Services
- Finding nearest Lyf properties
- Distance calculation
- Navigation assistance
- Local area information

## Usage

1. Start the bot:
```bash
python bot.py
```

2. In Telegram, interact with the bot using these commands:
- `/start` - Initialize the bot
- `/start_lyfCare` - Begin the main assistance flow
- `/start_translation` - Access the translation service
- `/data_agreement` - View data usage policies
- `/about_the_creators` - Information about the developers
- `/cancel` - End current operation

## Development Notes
- The bot uses a state machine pattern for handling conversations
- Multi-language support is implemented using OpenAI's translation services
- User data is stored in a lightweight TinyDB database
- Audio processing is handled through sounddevice and wavio libraries

## About HackAngel Hackathon
This project was developed for the HackAngel Hackathon Finals, focusing on creating innovative solutions for the hospitality industry. The LyfCare Assistant demonstrates the potential of AI and automation in enhancing guest experiences at Lyf properties.

## Contributors
- [Your Name]
- [Team Member 2]
- [Team Member 3]

## Acknowledgments
- Lyf for the opportunity and support
- HackAngel Hackathon organizers
- OpenAI for API services
- Telegram Bot API

## License
MIT licencse
