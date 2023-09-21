# aiogram_template_by_marsickat

## Описание

Шаблон для Telegram-ботов на основе aiogram с поддержкой postgresql, redis и docker.

Основан на другом шаблоне от [@MassonNN](https://github.com/MassonNN) - [masson-aiogram-template](https://github.com/MassonNN/masson-aiogram-template)

## Локальные зависимости

Для запуска проекта локально, убедитесь, что у вас установлены следующие зависимости:

1. [poetry](https://python-poetry.org/docs/#installation)
2. [redis](https://redis.io/docs/getting-started/installation/)


## Настройка

1. Файл .env.dist переименовать в .env
2. В файле .env в параметры <b>BOT_TOKEN</b>, <b>MAIN_ADMIN</b>, <b>ADMINS</b> записать Ваши данные
3. В файле .env в параметре <b>REDIS_PASSWORD</b> и в файле /database/redis/redis.conf в параметры <b>requirepass</b> и <b>masterauth</b> записать ваш пароль
4. Остальные параметры в файле .env можете изменять по Вашему желанию, если точно знаете что делаете

## Запуск бота

Для запуска бота локально выполните следующую команду из корневой папки проекта:

```bash
poetry run python -m bot
```

Для запуска с помощью docker для инициализации выполните следующую команду:

```bash
docker-compose run bot bash -c "poetry run alembic revision -m=init --autogenerate && poetry run alembic upgrade head"
```

## Docker

В docker используются образы

1. [python:3.10-slim](https://hub.docker.com/layers/library/python/3.10-slim/images/sha256-d364435d339ad318ac4c533b9fbe709739f9ba006b0721fd25e8592d0bb857cb?context=explore) - Python
2. [redis:latest](https://hub.docker.com/layers/library/redis/latest/images/sha256-b8d3a1a9e372ee2a64d6b647eb63ed87918876b5a0622f49e00289f04d481f97?context=explore) - Redis
3. [postgres:15-alpine](https://hub.docker.com/layers/library/postgres/15-alpine/images/sha256-f36c528a2dc8747ea40b4cb8578da69fa75c5063fd6a71dcea3e3b2a6404ff7b?context=explore) - Postgres
4. [dbeaver/cloudbeaver](https://hub.docker.com/layers/dbeaver/cloudbeaver/latest/images/sha256-c5e94d57994e187882d701b930ee2821c8fffc6c3e0fa4a9e04a9abd31a5cdef?context=explore) - Cloudbeaver

## Прочее

В будущем будет доработан [Makefile](https://github.com/Marsickat/my_aio_template_2/blob/master/Makefile) для более удобной работы