# Описание

API для мессенджера.

## Технологии

FastAPI, PostgreSQL, SQLAlchemy, fastapi_users, alembic

## Как запустить

Создать .env файл в корне проекта вида:

```env
DB_USER=postgres
DB_PASS=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=<имя вашей базы>
TOKEN_SECRET_KEY=<секретный ключ для токена(любой)>
```

Из корневой директории запустить docker-compose

```bash
docker-compose up
```

Документация Swagger будет доступна по адресу <http://0.0.0.0:8000/docs>.
