import logging
from telegram.ext import Application
from bot.handlers import setup_handlers
from config import TOKEN
from utils.helpers import add_initial_equipment

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    logging.info("Starting bot")
    add_initial_equipment()
    application = Application.builder().token(TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()
