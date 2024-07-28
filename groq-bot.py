import sys
import telebot
import requests
import os
import json
from collections import defaultdict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

# Load API keys from JSON file
def load_api_keys():
    try:
        with open('api-bot-groq.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        show_error("Error: api-bot-groq.json file not found. Please make sure it exists in the same directory as the script.")
        sys.exit(1)
    except json.JSONDecodeError:
        show_error("Error: api-bot-groq.json file is not valid JSON. Please check its contents.")
        sys.exit(1)
    except Exception as e:
        show_error(f"An unexpected error occurred while reading api-bot-groq.json: {str(e)}")
        sys.exit(1)

# Load API keys
api_keys = load_api_keys()

# Configuration
TELEGRAM_BOT_TOKEN = api_keys['TELEGRAM_BOT_TOKEN']
GROQ_API_KEY = api_keys['GROQ_API_KEY']
GROQ_API_URL = "https://api.groq.com/openai/v1"

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# User data
user_conversations = defaultdict(list)
user_models = defaultdict(lambda: "llama-3.1-8b-instant")
user_characters = defaultdict(lambda: "default")

# Load available models and characters
AVAILABLE_MODELS = [
    "llama-3.1-405b-reasoning", "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant", "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview", "llama3-70b-8192",
    "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it", "gemma2-9b-it"
]

# Load characters with error handling
try:
    with open('characters.json', 'r', encoding='utf-8') as f:
        AVAILABLE_CHARACTERS = json.load(f)
except FileNotFoundError:
    show_error("Error: characters.json file not found. Please make sure it exists in the same directory as the script.")
    AVAILABLE_CHARACTERS = {"default": {"name": "Default Character", "description": "A generic AI assistant."}}
except json.JSONDecodeError:
    show_error("Error: characters.json file is not valid JSON. Please check its contents.")
    AVAILABLE_CHARACTERS = {"default": {"name": "Default Character", "description": "A generic AI assistant."}}
except Exception as e:
    show_error(f"An unexpected error occurred while reading characters.json: {str(e)}")
    AVAILABLE_CHARACTERS = {"default": {"name": "Default Character", "description": "A generic AI assistant."}}

# Model emojis
MODEL_EMOJIS = {"llama": "🦙", "mixtral": "🌪️", "gemma": "💎"}

# Error handling function
def show_error(message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Icon.Critical)
    error_box.setText("Error")
    error_box.setInformativeText(message)
    error_box.setWindowTitle("Error")
    error_box.exec()

# Bot functionality
def format_model_info(model_name):
    prefix = model_name.split("-")[0]
    emoji = MODEL_EMOJIS.get(prefix, "🤖")
    return f"{emoji} Model: {model_name}"

def create_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    buttons = [
        InlineKeyboardButton("🔄 Reset", callback_data="reset"),
        InlineKeyboardButton("🔀 Model", callback_data="change_model"),
        InlineKeyboardButton("🎭 Karakter", callback_data="change_character"),
        InlineKeyboardButton("📊 Konteks", callback_data="context_count"),
        InlineKeyboardButton("💡 Ide Topik", callback_data="suggestions"),
        InlineKeyboardButton("❓ Bantuan", callback_data="help")
    ]
    markup.add(*buttons)
    return markup

def create_model_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    buttons = [
        InlineKeyboardButton(format_model_info(model),
                             callback_data=f"model_{model}")
        for model in AVAILABLE_MODELS
    ]
    markup.add(*buttons)
    return markup

def create_character_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    buttons = [
        InlineKeyboardButton(char_info['name'],
                             callback_data=f"character_{char_key}")
        for char_key, char_info in AVAILABLE_CHARACTERS.items()
    ]
    markup.add(*buttons)
    return markup

def create_suggestion_menu(suggestions):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for suggestion in suggestions:
        markup.add(KeyboardButton(suggestion))
    markup.add(KeyboardButton("🔄 Generate Saran Baru"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Halo! Saya adalah chatbot yang menggunakan Groq API.\n\n"
        "Silakan kirim pesan untuk memulai percakapan, atau ketik /menu untuk melihat opsi yang tersedia."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['menu'])
def show_menu(message):
    bot.send_message(message.chat.id, "Menu:", reply_markup=create_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    handlers = {
        "reset": reset_conversation,
        "change_model": show_model_options,
        "change_character": show_character_options,
        "context_count": show_context_count,
        "suggestions": show_suggestions,
        "help": send_help
    }

    if call.data in handlers:
        handlers[call.data](call.message)
    elif call.data.startswith("model_"):
        change_model(call.message, call.data.split("_", 1)[1])
    elif call.data.startswith("character_"):
        change_character(call.message, call.data.split("_", 1)[1])

    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)
    except ApiTelegramException as e:
        if "message is not modified" not in str(e):
            show_error(f"Telegram API error: {str(e)}")

def reset_conversation(message):
    user_id = message.chat.id
    user_conversations[user_id] = []
    bot.send_message(user_id, "🔄 Riwayat percakapan Anda telah direset.")
    show_menu(message)

def show_model_options(message):
    bot.send_message(message.chat.id,
                     "🔀 Pilih model AI:",
                     reply_markup=create_model_menu())

def show_character_options(message):
    bot.send_message(message.chat.id,
                     "🎭 Pilih karakter bot:",
                     reply_markup=create_character_menu())

def change_model(message, new_model):
    user_id = message.chat.id
    user_models[user_id] = new_model
    bot.send_message(user_id,
                     f"✅ Model AI diubah ke:\n{format_model_info(new_model)}")
    show_menu(message)

def change_character(message, new_character):
    user_id = message.chat.id
    user_characters[user_id] = new_character
    character_info = AVAILABLE_CHARACTERS[new_character]
    bot.send_message(user_id,
                     f"✅ Karakter diubah ke:\n{character_info['name']}")
    show_menu(message)

def show_context_count(message):
    user_id = message.chat.id
    context_count = len(user_conversations[user_id])
    bot.send_message(user_id, f"📊 Jumlah pesan dalam konteks: {context_count}")
    show_menu(message)

def show_suggestions(message):
    user_id = message.chat.id
    current_model = user_models[user_id]
    current_character = user_characters[user_id]
    character_info = AVAILABLE_CHARACTERS[current_character]

    system_message = f"""You are {character_info['name']}, {character_info['description']}. 
    A user wants to chat with you. Generate 6 diverse, creative, and engaging conversation starters or questions that the user can ask you.
    Each suggestion should:
    1. Reflect your unique character and personality as {character_info['name']}.
    2. Be relevant to your background, expertise, or the time period you're from (if applicable).
    3. Encourage interesting and in-depth conversations.
    4. Be concise, not exceeding 15 words.
    5. Start with an appropriate emoji that matches the topic or tone of the suggestion.
    6. Be presented on a new line.

    Mix up the types of suggestions:
    - Thought-provoking questions for you to answer
    - Intriguing scenarios or "what if" situations related to your expertise or background
    - Topics for discussion that align with your interests or knowledge
    - Requests for you to share a story or anecdote related to your background

    Remember, these are suggestions for what the user might ask YOU, so phrase them accordingly.
    Stay true to your character's personality, knowledge, and era throughout all suggestions. in bahasa indonesia"""

    try:
        response = requests.post(f"{GROQ_API_URL}/chat/completions",
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": f"Bearer {GROQ_API_KEY}"
                                 },
                                 json={
                                     "messages": [{
                                         "role": "system",
                                         "content": system_message
                                     }],
                                     "model": current_model,
                                     "temperature": 0.8,
                                     "max_tokens": 250,
                                     "top_p": 1,
                                     "stream": False,
                                     "stop": None
                                 })

        response.raise_for_status()
        suggestions = response.json()['choices'][0]['message']['content'].strip().split('\n')
        suggestions = [s.strip() for s in suggestions if s.strip()][:6]  # Ensure we have at most 6 suggestions
        bot.send_message(
            message.chat.id,
            f"💡 Berikut adalah beberapa pertanyaan yang bisa Anda ajukan kepada {character_info['name']}. Pilih salah satu, ketik pesan Anda sendiri, atau generate saran baru:",
            reply_markup=create_suggestion_menu(suggestions))
    except requests.exceptions.RequestException as e:
        error_message = f"Error generating suggestions: {str(e)}"
        show_error(error_message)
        bot.send_message(message.chat.id, "❌ Maaf, tidak dapat menghasilkan saran saat ini.")

def send_help(message):
    help_text = ("❓ Bantuan:\n\n"
                 "• 💬 Kirim pesan untuk memulai percakapan\n"
                 "• 🎤 Kirim pesan suara untuk transkripsi\n"
                 "• 🔄 'Reset' untuk memulai percakapan baru\n"
                 "• 🔀 'Model' untuk ganti model AI\n"
                 "• 🎭 'Karakter' untuk ganti karakter bot\n"
                 "• 📊 'Konteks' untuk cek jumlah pesan\n"
                 "• 💡 'Ide Topik' untuk mendapatkan ide percakapan\n"
                 "• 🔍 Ketik /menu untuk menu utama")
    bot.send_message(message.chat.id, help_text)
    show_menu(message)

def transcribe_audio(file_path):
    try:
        with open(file_path, 'rb') as audio_file:
            response = requests.post(
                f"{GROQ_API_URL}/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files={"file": audio_file},
                data={
                    "model": "whisper-large-v3",
                    "response_format": "verbose_json"
                })

        response.raise_for_status()
        return response.json()['text']
    except requests.exceptions.RequestException as e:
        error_message = f"Error transcribing audio: {str(e)}"
        show_error(error_message)
        return None

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("voice_message.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)

        transcription = transcribe_audio("voice_message.ogg")

        if transcription:
            bot.reply_to(message, f"🎤 Transkripsi:\n\n{transcription}")
            handle_message(message, transcription)
        else:
            bot.reply_to(
                message,
                "❌ Maaf, terjadi kesalahan saat mentranskripsikan pesan suara."
            )

    except Exception as e:
        error_message = f"Error handling voice message: {str(e)}"
        show_error(error_message)
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")

    finally:
        if os.path.exists("voice_message.ogg"):
            os.remove("voice_message.ogg")

def handle_message(message, user_message=None):
    user_id = message.from_user.id
    user_message = user_message or message.text

    current_character = user_characters[user_id]
    character_info = AVAILABLE_CHARACTERS[current_character]

    system_message = f"You are {character_info['name']}, {character_info['description']}. Respond accordingly."

    user_conversations[user_id].append({
        "role": "system",
        "content": system_message
    })
    user_conversations[user_id].append({
        "role": "user",
        "content": user_message
    })

    conversation_history = user_conversations[user_id][-6:]  # Include system message + 5 latest messages
    current_model = user_models[user_id]

    try:
        response = requests.post(f"{GROQ_API_URL}/chat/completions",
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": f"Bearer {GROQ_API_KEY}"
                                 },
                                 json={
                                     "messages": conversation_history,
                                     "model": current_model,
                                     "temperature": 0.7,
                                     "max_tokens": 1024,
                                     "top_p": 1,
                                     "stream": False,
                                     "stop": None
                                 })

        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        user_conversations[user_id].append({
            "role": "assistant",
            "content": bot_response
        })
    except requests.exceptions.RequestException as e:
        error_message = f"Error processing request: {str(e)}"
        show_error(error_message)
        bot_response = "❌ Maaf, terjadi kesalahan saat memproses permintaan Anda."

    model_info = f"\n\n{format_model_info(current_model)}"
    character_info_text = f"\n{character_info['name']}"

    bot.reply_to(message, bot_response + model_info + character_info_text)

@bot.message_handler(func=lambda message: message.text == "🔄 Generate Saran Baru")
def regenerate_suggestions(message):
    show_suggestions(message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text != "🔄 Generate Saran Baru":
        handle_message(message)
    bot.send_message(message.chat.id, "Ketik /menu untuk melihat opsi yang tersedia.")

# Optimized PyQt6 GUI implementation
class BotThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        self.is_running = True
        self.update_signal.emit("Bot started...")
        while self.is_running:
            try:
                bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as e:
                error_message = f"Error during bot polling: {str(e)}"
                self.update_signal.emit(error_message)
                show_error(error_message)
                self.update_signal.emit("Restarting bot...")

    def stop(self):
        self.is_running = False
        bot.stop_polling()
        self.update_signal.emit("Bot stopped.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telegram Bot Controller")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.start_button = QPushButton("Start Bot")
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Bot")
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.bot_thread = None
        self.stop_timer = QTimer(self)
        self.stop_timer.timeout.connect(self.check_bot_stopped)

    def start_bot(self):
        self.log_text.append("Starting bot...")
        self.bot_thread = BotThread()
        self.bot_thread.update_signal.connect(self.update_log)
        self.bot_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_bot(self):
        if self.bot_thread and self.bot_thread.is_running:
            self.log_text.append("Stopping bot...")
            self.bot_thread.stop()
            self.stop_timer.start(100)  # Check every 100ms

    def check_bot_stopped(self):
        if not self.bot_thread.is_running:
            self.stop_timer.stop()
            self.bot_thread = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.log_text.append("Bot stopped.")

    def update_log(self, message):
        self.log_text.append(message)

    def closeEvent(self, event):
        if self.bot_thread and self.bot_thread.is_running:
            self.stop_bot()
            self.bot_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())