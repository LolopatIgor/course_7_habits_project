import pytest
from django.contrib.auth import get_user_model
from habits.models import Habit
from users.models import Profile
from telegram import Update, Chat, User as TelegramUser
from telegram.ext import CallbackContext
from unittest.mock import patch
from telegram_bot.handlers import start
from habits.tasks import send_habit_reminder
from rest_framework.test import APITestCase
from habits.serializers import HabitSerializer

User = get_user_model()


@pytest.mark.django_db
class TestFullFunctionality:
    @pytest.fixture
    def create_user(self):
        """Создаёт пользователя и его профиль."""
        user = User.objects.create_user(username="testuser", password="testpassword")
        Profile.objects.create(user=user, link_code="1234abcd")
        return user

    def test_user_creation_and_profile(self, create_user):
        """Тест создания пользователя и профиля."""
        user = create_user
        profile = user.profile
        assert user.username == "testuser"
        assert profile.link_code == "1234abcd"
        assert profile.chat_id is None

    def test_link_chat_id(self, create_user, mocker):
        """Тест присвоения chat_id пользователю через команду /start."""
        user = create_user
        profile = user.profile

        # Mock Update и CallbackContext
        mock_chat = Chat(id=987654321, type="private")
        mock_telegram_user = TelegramUser(id=111222333, is_bot=False, first_name="TestUser")
        mock_update = mocker.Mock(spec=Update)
        mock_update.effective_chat = mock_chat
        mock_update.effective_user = mock_telegram_user
        mock_update.message.text = "/start 1234abcd"

        mock_context = mocker.Mock(spec=CallbackContext)
        mock_context.args = ["1234abcd"]  # Добавляем аргументы для команды /start

        # Вызываем обработчик команды /start
        start(mock_update, mock_context)

        # Проверяем, что chat_id присвоен
        profile.refresh_from_db()
        assert profile.chat_id == 987654321

        # Проверяем отправленное сообщение
        mock_context.bot.send_message.assert_called_once_with(
            chat_id=987654321,
            text="Ваш аккаунт успешно привязан к Telegram!"
        )

    def test_create_habit(self, create_user):
        """Тест создания привычки пользователем."""
        user = create_user

        # Создаём привычку
        habit = Habit.objects.create(
            user=user,
            place="дом",
            time="12:00:00",
            action="пробежка",
            is_pleasant=False,
            period_days=1,
            duration_seconds=120,
            is_public=True
        )

        # Проверяем, что привычка создана
        assert Habit.objects.count() == 1
        assert habit.user == user
        assert habit.action == "пробежка"

    @patch('habits.tasks.send_habit_reminder.delay')
    def test_send_reminder(self, mock_send, create_user):
        """Тест отправки напоминания через Celery."""
        user = create_user
        profile = user.profile
        profile.chat_id = 987654321
        profile.save()

        # Создаём привычку
        habit = Habit.objects.create(
            user=user,
            place="дом",
            time="12:00:00",
            action="пробежка",
            is_pleasant=False,
            period_days=1,
            duration_seconds=120,
            is_public=True
        )

        # Запускаем задачу отправки напоминания
        send_habit_reminder.delay(user_id=user.id, message="Не забудь о привычке!")

        # Проверяем, что задача Celery вызвана
        mock_send.assert_called_once_with(
            user_id=user.id,
            message="Не забудь о привычке!"
        )


class TestHabitSerializer(APITestCase):
    def test_valid_data(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {
            "place": "дом",
            "time": "12:00:00",
            "action": "пробежка",
            "is_pleasant": False,
            "period_days": 1,
            "duration_seconds": 120,
            "is_public": True,
            "user": user.id
        }
        serializer = HabitSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['action'] == "пробежка"

    def test_invalid_data(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {
            "place": "дом",
            "time": "12:00:00",
            "action": "пробежка",
            "is_pleasant": False,
            "period_days": 14,  # Не больше 7 - невалидно
            "duration_seconds": 100,  # Сделаем валидным
            "is_public": True,
            "user": user.id
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        # Проверяем, что ошибка содержится в period_days
        assert 'period_days' in serializer.errors
        assert serializer.errors['period_days'][0] == "Периодичность не может быть больше 7 дней."

    def test_duration_seconds_validation(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {
            "place": "офис",
            "time": "10:00:00",
            "action": "йога",
            "is_pleasant": False,
            "period_days": 5,
            "duration_seconds": 130,  # Невалидное значение
            "is_public": False,
            "user": user.id
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        assert "duration_seconds" in serializer.errors
        assert serializer.errors["duration_seconds"][0] == "Время выполнения не может превышать 120 секунд."

    def test_period_days_validation(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {
            "place": "офис",
            "time": "10:00:00",
            "action": "йога",
            "is_pleasant": False,
            "period_days": 10,  # Невалидное значение
            "duration_seconds": 100,
            "is_public": False,
            "user": user.id
        }
        serializer = HabitSerializer(data=data)
        assert not serializer.is_valid()
        assert "period_days" in serializer.errors
        assert serializer.errors["period_days"][0] == "Периодичность не может быть больше 7 дней."
