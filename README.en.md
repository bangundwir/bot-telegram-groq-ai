# English

## 📜 Introduction

This Telegram Bot is an advanced chatbot that integrates with the Groq API to provide AI-powered conversations. It features multiple AI models, character selection, and a graphical user interface (GUI) for easy management.

## 🛠️ Prerequisites

- Python 3.7+
- `telebot` library
- `requests` library
- `PyQt6` library
- Telegram Bot Token
- Groq API Key

## ⚙️ Setup

1. Clone the repository or download the script.

2. Install the required libraries:

   ```sh
   pip install pyTelegramBotAPI requests PyQt6
   ```

3. Create a `api-bot-groq.json` file in the same directory as the script with the following content:

   ```json
   {
       "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token_here",
       "GROQ_API_KEY": "your_groq_api_key_here"
   }
   ```

4. Create a `characters.json` file in the same directory with character definitions (example provided in the [Configuration](#configuration) section).

## 🛠️ Configuration

### 🔑 API Keys

Store your API keys in the `api-bot-groq.json` file:

```json
{
    "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token_here",
    "GROQ_API_KEY": "your_groq_api_key_here"
}
```

### 🎭 Characters

Define characters in the `characters.json` file:

```json
{
    "default": {
        "name": "Default Assistant",
        "description": "A helpful AI assistant."
    },
    "historian": {
        "name": "History Expert",
        "description": "An AI specializing in historical facts and events."
    }
}
```

## 🚀 Usage

1. Run the script:

   ```sh
   python your_script_name.py
   ```

2. Use the GUI to start and stop the bot.

3. Interact with the bot on Telegram using the following commands:

   - `/start`: Begin a conversation
   - `/menu`: Display the main menu
   - Use the inline buttons to change models, characters, or access other features

## 🔍 Key Components

### 💬 Bot Functionality

- Multiple AI models support
- Character selection
- Conversation context management
- Voice message transcription
- Suggestion generation for conversation topics

### 📜 Message Handlers

- `/start`: Sends a welcome message
- `/menu`: Displays the main menu
- Callback query handler for inline buttons
- Voice message handler for transcription
- General message handler for conversations

## 🖥️ GUI Interface

The graphical user interface provides the following features:

- Start Bot: Begins the bot's operation
- Stop Bot: Gracefully stops the bot
- Log Display: Shows bot activity and errors

## 🔧 Customization

### 🔄 Adding New Models

Add new model names to the `AVAILABLE_MODELS` list in the script.

### 🎭 Adding New Characters

Add new character definitions to the `characters.json` file.

### ⚙️ Modifying Bot Behavior

Adjust the `handle_message` function to change how the bot processes and responds to messages.

## 🚑 Troubleshooting

- **Bot Not Responding**: Check your internet connection and verify the Telegram Bot Token.
- **API Errors**: Ensure your Groq API key is correct and has sufficient permissions.
- **GUI Not Starting**: Verify that PyQt6 is installed correctly.
- **Character/Model Issues**: Check the `characters.json` file and `AVAILABLE_MODELS` list for correct formatting.

For any other issues, check the console output for error messages and refer to the respective library documentation for `telebot`, `requests`, and `PyQt6`.
