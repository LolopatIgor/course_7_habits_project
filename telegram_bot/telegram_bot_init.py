import os
from telegram import Bot

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)
