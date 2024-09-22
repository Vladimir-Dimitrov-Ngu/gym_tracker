from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'),
         InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_gender_keyboard(messages, lang):
    keyboard = [
        [InlineKeyboardButton(messages[lang]['male'], callback_data='gender_male')],
        [InlineKeyboardButton(messages[lang]['female'], callback_data='gender_female')],
        [InlineKeyboardButton(messages[lang]['skip'], callback_data='gender_skip')]
    ]
    return InlineKeyboardMarkup(keyboard)
