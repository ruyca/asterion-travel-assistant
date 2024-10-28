
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
import os
import sounddevice as sd
import wavio
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from query_chatgpt import translate
from playsound import playsound
from query_chatgpt import translate


load_dotenv()
client = OpenAI(api_key=os.getenv("CHATGPT_API"))

# Assuming `translate` is a function you've defined
# which takes (text, target_language) as parameters
def text_audio_request(text, path="output"):
    os.makedirs(path, exist_ok=True)
    speech_file_path = os.path.join(path, "output_audio.mp3")

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    print(f"Audio generated at: {speech_file_path}")
    return speech_file_path

def record_audio(duration=5, sample_rate=44100, path="input_audio.wav"):
    print("Recording started...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    wavio.write(path, audio_data, sample_rate, sampwidth=2)
    print(f"Recording saved as {path}")
    return path

def transcribe_audio(audio_path, language="en"):
    # Check if the file exists
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return None

    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
        print("Transcription complete:", transcript.text)  # Adjusted to access `text` attribute
        return transcript.text  # Return transcript text correctly
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def live_conversation(user_a_message, user_b_language="es", user_a_language="en"):
    while True:        
        # Step 1: User A sends a message and we get an audio response
        print(f"User A's message received: {user_a_message}")
        # Step 1.25: Translate User A's message into User B's language
        translated_message = translate(user_a_message, user_b_language)
        print(f"User A's message translated to {user_b_language}: {translated_message}")
        # Step 1.5: Generate audio response for User B in their language
        audio_path = text_audio_request(translated_message)
        print(f"User A's message audio ready for User B in {user_b_language}")
        # Step 1.75: Play the generated audio message for User B
        print("Playing User A's translated message audio...")
        playsound(audio_path)
        # Step 2: User B listens, then responds by recording
        input("Press Enter to record User B's response...")  # Trigger to start recording
        response_audio_path = record_audio()
                # Step 3: Transcribe User B's audio response
        print("Transcribing User B's response...")
        user_b_text = transcribe_audio(response_audio_path, )
        # Check if transcription was successful
        if user_b_text is None:
            print("Transcription failed, retrying...")
            continue  # Restart the loop to allow User B to record again
        user_b_text = translate(user_b_text, user_a_language, forced=True)
        print(f"User B's transcribed message: {user_b_text}")
        # Break condition
        end_conversation = input("Type 'yes' to end the conversation or press Enter to continue: ")
        if end_conversation.lower() == "yes":
            print("Ending conversation.")
            break