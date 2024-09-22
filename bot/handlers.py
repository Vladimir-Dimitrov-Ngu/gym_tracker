from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ConversationHandler, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.keyboards import get_language_keyboard, get_gender_keyboard
from bot.messages import WELCOME_MESSAGE, START_MESSAGE, HELP_MESSAGE, PROFILE_MESSAGES, ANALYTICS_MESSAGES
from database.operations import get_user, create_or_update_user, get_latest_weight, get_weight_history
from services.progress_analyzer import analyze_weight_progress
import matplotlib.pyplot as plt
import io

# Добавьте эти константы в начало файла
GENDER, HEIGHT, WEIGHT = range(3)

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

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get('language', 'en')
    db_user = get_user(user.id)
    
    if db_user:
        await update.message.reply_text(PROFILE_MESSAGES[lang]['update_weight_prompt'])
        return WEIGHT
    else:
        reply_markup = get_gender_keyboard(PROFILE_MESSAGES, lang)
        await update.message.reply_text(PROFILE_MESSAGES[lang]['gender_prompt'], reply_markup=reply_markup)
        return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    gender = query.data.split('_')[1]
    
    if gender != 'skip':
        context.user_data['gender'] = gender
    
    await query.edit_message_text(PROFILE_MESSAGES[lang]['height_prompt'])
    return HEIGHT

async def height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'en')
    if update.message.text.lower() == PROFILE_MESSAGES[lang]['skip'].lower():
        context.user_data['height'] = None
    else:
        try:
            height = int(update.message.text)
            context.user_data['height'] = height
        except ValueError:
            await update.message.reply_text(PROFILE_MESSAGES[lang]['invalid_height'])
            return HEIGHT
    
    await update.message.reply_text(PROFILE_MESSAGES[lang]['weight_prompt'])
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'en')
    if update.message.text.lower() == PROFILE_MESSAGES[lang]['skip'].lower():
        await update.message.reply_text(PROFILE_MESSAGES[lang]['weight_skipped'])
        return ConversationHandler.END
    else:
        try:
            weight = float(update.message.text)
            user_id = update.effective_user.id
            db_user = get_user(user_id)
            if db_user:
                create_or_update_user(user_id, weight=weight)
            else:
                gender = context.user_data.get('gender')
                height = context.user_data.get('height')
                create_or_update_user(user_id, gender, height, weight)
            
            latest_weight = get_latest_weight(user_id)
            await update.message.reply_text(PROFILE_MESSAGES[lang]['weight_updated'].format(weight=latest_weight))
        except ValueError:
            await update.message.reply_text(PROFILE_MESSAGES[lang]['invalid_weight'])
            return WEIGHT
    
    return ConversationHandler.END

async def analytics_weights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get('language', 'en')
    db_user = get_user(user.id)
    
    if not db_user:
        await update.message.reply_text(ANALYTICS_MESSAGES[lang]['no_data'])
        return

    weight_history = get_weight_history(user.id)
    
    chart, analysis_text = analyze_weight_progress(weight_history, lang, ANALYTICS_MESSAGES)
    
    if not chart:
        await update.message.reply_text(analysis_text)
        return
    
    await update.message.reply_photo(chart)
    await update.message.reply_text(analysis_text)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(PROFILE_MESSAGES[lang]['cancelled'])
    return ConversationHandler.END


profile_handler = ConversationHandler(
    entry_points=[CommandHandler("profile", profile)],
    states={
        GENDER: [CallbackQueryHandler(gender, pattern='^gender_')],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height)],
        WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

def setup_handlers(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(profile_handler)
    application.add_handler(CommandHandler("analytics_weights", analytics_weights))
