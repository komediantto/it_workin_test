# Описание

API для мессенджера.

## Технологии

FastAPI, PostgreSQL, SQLAlchemy, fastapi_users, alembic

## Как запустить

Создать .env файл в корне проекта вида:

```env
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<имя вашей базы>
TOKEN_SECRET_KEY=<секретный ключ для токена(любой)>
USER_SECRET_KEY=<секретный ключ для юзеров(любой)
```

Из корневой директории запустить следующие команды

```bash
poetry install
poetry shell
alembic upgrade head
uvicorn app.main:app --reload
```

Документация Swagger будет доступна по адресу <http://127.0.0.1:8000/docs>.
