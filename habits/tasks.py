# habits/tasks.py
from celery import shared_task
from telegram import Bot
import os
from django.contrib.auth import get_user_model

User = get_user_model()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)


@shared_task
def send_habit_reminder(user_id, message):
    user = User.objects.get(pk=user_id)
    chat_id = user.profile.chat_id
    if chat_id:
        bot.send_message(chat_id=chat_id, text=message)
