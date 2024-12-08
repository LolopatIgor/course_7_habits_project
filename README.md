# Habits Tracker Project

## Описание

Данный проект — бэкенд-часть для веб-приложения по отслеживанию привычек. Он реализован на Django и Django REST Framework, с поддержкой CORS, интеграцией с Telegram, асинхронными задачами через Celery, пагинацией, проверками качества кода и тестированием.

## Основной функционал

- Создание и управление привычками.
- Публичные привычки, доступные всем для просмотра.
- Авторизация и регистрация пользователей.
- Интеграция с Telegram-ботом для отправки напоминаний.
- Периодическое выполнение задач через Celery.
- Валидация и права доступа для CRUD-операций над привычками.
- Пагинация списка привычек.
- Переменные окружения для конфиденциальных данных.

## Требования

- Python 3.10+
- PostgreSQL (при желании можно начать с SQLite)
- Redis 
- Git

## Установка и настройка

1. **Клонировать репозиторий**:
   ```bash
   git clone https://github.com/your_username/habits_project.git
   cd habits_project


   Создать и активировать виртуальное окружение:

python3 -m venv venv
source venv/bin/activate

Установка зависимостей:

pip install --upgrade pip
pip install -r requirements.txt

Настройка переменных окружения: В проекте находится файл .env.sample нужно переименовать его и наполнить актуальными данными

Применить миграции:

python manage.py migrate

Запуск сервера разработки:

    python manage.py runserver

    Приложение будет доступно по адресу: http://127.0.0.1:8000.

Запуск Celery и Redis

    Убедитесь, что Redis запущен:

redis-server

Запустите Celery worker:

    celery -A habits_project worker -l INFO

При необходимости запустите celery beat для периодических задач:

celery -A habits_project beat -l INFO

Интеграция с Telegram

    Укажите TELEGRAM_BOT_TOKEN в .env.    
    При наличии запланированных задач Celery будет отправлять уведомления через бота.

Тестирование и покрытие

Запуск тестов:

pytest

pytest --cov=habits --cov=users --cov-report=term-missing

Цель: покрытие >= 80%.
CORS

Настройки CORS включены:

INSTALLED_APPS = [
    ...,
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True

При необходимости указать конкретные домены в settings.py.
Проверка кода с flake8

Запуск flake8:

flake8

Исключения и настройки прописаны в setup.cfg (или tox.ini), чтобы исключить миграции и внешние пакеты.
Документация API

Если настроен drf-spectacular или drf-yasg, схемы и документацию можно посмотреть по адресам:

    http://127.0.0.1:8000/api/docs/
    http://127.0.0.1:8000/api/redoc/
    http://127.0.0.1:8000/api/schema/

Список зависимостей

Все зависимости указаны в requirements.txt. Используйте его для разворачивания окружения и поддержания единой версии библиотек.
Дополнительно

    При возникновении проблем с миграциями или версиями пакетов — обновите зависимости или выполните makemigrations повторно.
    Рекомендуется использовать Postgres для продакшена, SQLite — для начальной разработки.
    Для реального деплоя настройте DEBUG=False, установите ALLOWED_HOSTS и используйте HTTPS.

