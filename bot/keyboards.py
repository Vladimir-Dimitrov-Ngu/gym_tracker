from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'),
         InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')]
    ]
    return InlineKeyboardMarkup(keyboard)
