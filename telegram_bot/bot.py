import os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from .handlers import start

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Регистрируем хэндлер на команду /start
dispatcher.add_handler(CommandHandler('start', start))


# Запуск бота
def run_bot():
    updater.start_polling()
    updater.idle()
