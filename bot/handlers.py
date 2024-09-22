from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import get_language_keyboard
from bot.messages import WELCOME_MESSAGE, START_MESSAGE, HELP_MESSAGE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    reply_markup = get_language_keyboard()
    await update.message.reply_text(
        f"{WELCOME_MESSAGE['en']}\n{WELCOME_MESSAGE['ru']}",
        reply_markup=reply_markup
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['language'] = lang
    await query.edit_message_text(
        START_MESSAGE[lang].format(name=query.from_user.first_name)
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(HELP_MESSAGE[lang])
