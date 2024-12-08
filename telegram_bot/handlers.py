# telegram_bot/handlers.py
from telegram import Update
from telegram.ext import CallbackContext
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    args = context.args
    if args:
        link_code = args[0]
        try:
            profile = Profile.objects.get(link_code=link_code)
            profile.chat_id = chat_id
            profile.link_code = None
            profile.save()
            context.bot.send_message(chat_id=chat_id, text="Ваш аккаунт успешно привязан к Telegram!")
        except Profile.DoesNotExist:
            context.bot.send_message(chat_id=chat_id, text="Неверный или просроченный код.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Отправьте /start <код> для привязки к аккаунту.")
