import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.handlers import start, help, language_callback
from config import TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))

    application.run_polling()

if __name__ == '__main__':
    main()
