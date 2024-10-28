# translation.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("CHATGPT_API"))

languages_iso = {
    "Simplified Chinese": "zh_HANS",
    "Spanish": "es",
    "English": "en",
    "Hindi": "hi",
    "Arabic": "ar",
    "Bengali": "bn",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Punjabi": "pa",
    "German": "de",
    "Javanese": "jv",
    "Wu Chinese": "wuu",
    "French": "fr",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Korean": "ko",
    "Telugu": "te",
    "Italian": "it",
    "Malay": "ms",  # Added Malay
    "Thai": "th"
}


def translate(message, target, forced=False):

    if not forced:
        if target == "English":
            return message


    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "Translate English text to a user-specified language while preserving any HTML tags present in the text. The translation should maintain the HTML structure intact, altering only the English text.\n\n# Steps\n\n1. Identify and preserve any HTML tags present in the given text.\n2. Translate the English phrases only, ensuring that the HTML tags remain unchanged.\n3. Combine the translated text with the original HTML tags to form a coherent translated output.\n\n# Output Format\n\n- The output should be a string that contains the translated text with the original HTML tags in place. \n- Ensure the response is plain text, without any additional formatting or code blocks.\n\n# Notes\n\n- Pay attention to complex HTML structures and nested tags to ensure correct translation without altering the HTML.\n- Handle any edge cases where HTML attributes might contain translatable text separately."
            }
        ],
        "role": "user",
        "content":[
            {
            "type": "text",
            "text": f"Translate this message {message}\n\nTo this language: {target}\n\nOnly translate the text. Don't add any more text like 'Sure, I help you with that'"
            }
        ]
        }
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
    )
    
    return response.choices[0].message.content


