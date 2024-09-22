from telegram import Update
from telegram.ext import (
    Application, ConversationHandler, ContextTypes, CommandHandler, 
    CallbackQueryHandler, MessageHandler, filters
)
from bot.keyboards import (
    get_language_keyboard, get_gender_keyboard, get_muscle_group_keyboard, 
    get_equipment_keyboard
)
from bot.messages import (
    WELCOME_MESSAGE, START_MESSAGE, HELP_MESSAGE, PROFILE_MESSAGES, 
    ANALYTICS_MESSAGES, WORKOUT_MESSAGES, MUSCLE_GROUPS, EQUIPMENT_LIST
)
from database.operations import (
    get_user, create_or_update_user, get_latest_weight, get_weight_history, 
    add_workout, get_equipment_by_muscle_group, get_equipment_description, 
    add_custom_equipment
)
from services.progress_analyzer import analyze_weight_progress
import logging

# Константы для состояний разговора
GENDER, HEIGHT, WEIGHT = range(3)
MUSCLE_GROUP, EQUIPMENT, CUSTOM_EQUIPMENT, SETS, REPS = range(5)

# Фильтры для команд
start_filter = filters.Command("start") & filters.ChatType.PRIVATE
help_filter = filters.Command("help") & filters.ChatType.PRIVATE
profile_filter = filters.Command("profile") & filters.ChatType.PRIVATE
track_workout_filter = filters.Command("track_workout") & filters.ChatType.PRIVATE
analytics_weights_filter = filters.Command("analytics_weights") & filters.ChatType.PRIVATE
cancel_filter = filters.Command("cancel") & filters.ChatType.PRIVATE

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Start command received")
    user = update.effective_user
    reply_markup = get_language_keyboard()
    await update.message.reply_text(
        f"{WELCOME_MESSAGE['en']}\n{WELCOME_MESSAGE['ru']}",
        reply_markup=reply_markup
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Help command received")
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(HELP_MESSAGE[lang])

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Profile command received. Message text: {update.message.text}")
    user = update.effective_user
    lang = context.user_data.get('language', 'en')
    db_user = get_user(user.id)
    
    if db_user:
        logging.info(f"User {user.id} found in database")
        await update.message.reply_text(PROFILE_MESSAGES[lang]['update_weight_prompt'])
        return WEIGHT
    else:
        logging.info(f"User {user.id} not found in database")
        reply_markup = get_gender_keyboard(PROFILE_MESSAGES, lang)
        await update.message.reply_text(PROFILE_MESSAGES[lang]['gender_prompt'], reply_markup=reply_markup)
        return GENDER

async def track_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Track workout command received")
    lang = context.user_data.get('language', 'en')
    reply_markup = get_muscle_group_keyboard(MUSCLE_GROUPS, lang)
    await update.message.reply_text(WORKOUT_MESSAGES[lang]['select_muscle_group'], reply_markup=reply_markup)
    return MUSCLE_GROUP

async def analytics_weights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Analytics weights command received")
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
    logging.info("Cancel command received")
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(PROFILE_MESSAGES[lang]['cancelled'])
    return ConversationHandler.END

# Обр��ботчики колбэков
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Language callback received")
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['language'] = lang
    await query.edit_message_text(
        START_MESSAGE[lang].format(name=query.from_user.first_name)
    )

async def gender_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Gender callback received")
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    gender = query.data.split('_')[1]
    
    if gender != 'skip':
        context.user_data['gender'] = gender
    
    await query.edit_message_text(PROFILE_MESSAGES[lang]['height_prompt'])
    return HEIGHT

async def muscle_group_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Muscle group callback received")
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    muscle_group = query.data.split('_')[1]
    context.user_data['muscle_group'] = muscle_group
    print('/n/n/n')
    print(muscle_group)
    
    equipment_list = EQUIPMENT_LIST[lang][MUSCLE_GROUPS[lang].index(muscle_group)]
    reply_markup = get_equipment_keyboard(equipment_list, lang)
    
    await query.edit_message_text(WORKOUT_MESSAGES[lang]['select_equipment'], reply_markup=reply_markup)
    return EQUIPMENT

async def equipment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Equipment callback received")
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    equipment = query.data.split('_')[1]
    
    if equipment == 'custom':
        await query.edit_message_text(WORKOUT_MESSAGES[lang]['enter_custom_equipment'])
        return CUSTOM_EQUIPMENT
    
    context.user_data['equipment'] = equipment
    await query.edit_message_text(WORKOUT_MESSAGES[lang]['enter_sets'])
    return SETS

async def equipment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Equipment info callback received")
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    equipment = query.data.split('_')[1]
    
    description = get_equipment_description(equipment)
    if description:
        await query.edit_message_text(WORKOUT_MESSAGES[lang]['equipment_info'].format(equipment=equipment, description=description))
    else:
        await query.edit_message_text(WORKOUT_MESSAGES[lang]['equipment_info'].format(equipment=equipment, description="No information available."))

# Обработчики сообщений
async def height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Height message received")
    lang = context.user_data.get('language', 'en')
    if update.message.text.lower() == PROFILE_MESSAGES[lang]['skip'].lower():
        context.user_data['height'] = None
    else:
        try:
            height = int(update.message.text)
            context.user_data['height'] = height
        except ValueError:
            logging.warning("Invalid height input")
            await update.message.reply_text(PROFILE_MESSAGES[lang]['invalid_height'])
            return HEIGHT
    
    await update.message.reply_text(PROFILE_MESSAGES[lang]['weight_prompt'])
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Weight message received")
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
            logging.warning("Invalid weight input")
            await update.message.reply_text(PROFILE_MESSAGES[lang]['invalid_weight'])
            return WEIGHT
    
    return ConversationHandler.END

async def custom_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Custom equipment message received")
    lang = context.user_data.get('language', 'en')
    equipment = update.message.text
    context.user_data['equipment'] = equipment
    add_custom_equipment(equipment, context.user_data['muscle_group'], "Custom equipment")
    await update.message.reply_text(WORKOUT_MESSAGES[lang]['enter_sets'])
    return SETS

async def sets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Sets message received")
    lang = context.user_data.get('language', 'en')
    try:
        sets = int(update.message.text)
        context.user_data['sets'] = sets
        await update.message.reply_text(WORKOUT_MESSAGES[lang]['enter_reps'])
        return REPS
    except ValueError:
        logging.warning("Invalid sets input")
        await update.message.reply_text(WORKOUT_MESSAGES[lang]['invalid_input'])
        return SETS

async def reps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Reps message received")
    lang = context.user_data.get('language', 'en')
    try:
        reps = int(update.message.text)
        context.user_data['reps'] = reps
        
        user_id = update.effective_user.id
        muscle_group = context.user_data['muscle_group']
        equipment = context.user_data['equipment']
        sets = context.user_data['sets']
        
        add_workout(user_id, muscle_group, equipment, sets, reps)
        
        await update.message.reply_text(WORKOUT_MESSAGES[lang]['workout_saved'])
        return ConversationHandler.END
    except ValueError:
        logging.warning("Invalid reps input")
        await update.message.reply_text(WORKOUT_MESSAGES[lang]['invalid_input'])
        return REPS

# Обработчики разговоров
profile_handler = ConversationHandler(
    entry_points=[CommandHandler("profile", profile, filters=profile_filter)],
    states={
        GENDER: [CallbackQueryHandler(gender_callback, pattern='^gender_')],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height)],
        WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight)],
    },
    fallbacks=[CommandHandler("cancel", cancel, filters=cancel_filter)],
)

workout_handler = ConversationHandler(
    entry_points=[CommandHandler("track_workout", track_workout, filters=track_workout_filter)],
    states={
        MUSCLE_GROUP: [CallbackQueryHandler(muscle_group_callback, pattern='^muscle_')],
        EQUIPMENT: [CallbackQueryHandler(equipment_callback, pattern='^equip_')],
        CUSTOM_EQUIPMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_equipment)],
        SETS: [MessageHandler(filters.Regex(r'^\d+$'), sets)],
        REPS: [MessageHandler(filters.Regex(r'^\d+$'), reps)],
    },
    fallbacks=[CommandHandler("cancel", cancel, filters=cancel_filter)],
)

def setup_handlers(application: Application):
    application.add_handler(CommandHandler("start", start, filters=start_filter))
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    application.add_handler(CommandHandler("help", help, filters=help_filter))
    application.add_handler(profile_handler)
    application.add_handler(workout_handler)
    application.add_handler(CommandHandler("analytics_weights", analytics_weights, filters=analytics_weights_filter))
    application.add_handler(CallbackQueryHandler(equipment_info, pattern='^info_'))
    application.add_error_handler(error_handler)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f"Exception while handling an update: {context.error}")
