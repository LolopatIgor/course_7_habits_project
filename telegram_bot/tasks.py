from celery import shared_task
from telegram_bot.telegram_bot_init import bot


@shared_task
def send_habit_reminder(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)
