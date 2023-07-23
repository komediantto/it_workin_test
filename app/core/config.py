import sys
from typing import Any, Dict, Optional
import asyncpg
from loguru import logger
from pydantic import ValidationError, PostgresDsn, validator
from pydantic_settings import BaseSettings

from app.core import constants


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    TOKEN_SECRET_KEY: str

    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI")
    def assemble_sync_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v

        required_variables = [
            "DB_USER",
            "DB_PASS",
            "DB_HOST",
            "DB_PORT",
            "DB_NAME",
            "TOKEN_SECRET_KEY",
        ]
        for var_name in required_variables:
            if var_name not in values:
                raise ValueError(constants.VAR_MISSING.format(var_name=var_name))

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("DB_USER"),
            password=values.get("DB_PASS"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"{values.get('DB_NAME') or ''}",
        )

    class Config:
        env_file = ".env"


async def check_database_connection(settings: Settings):
    try:
        connection_uri = str(settings.DATABASE_URI).replace("+asyncpg", "")
        if connection_uri is None:
            raise ValueError(constants.FAIL_URI)
        conn = await asyncpg.connect(dsn=connection_uri)
        await conn.execute("SELECT 1")
        await conn.close()

        logger.info(constants.DATABASE_OK)
    except Exception as e:
        logger.error(constants.DATABASE_FAIL.format(e=e))


try:
    settings = Settings()
except ValidationError as e:
    error = [error["msg"] for error in e.errors()]
    error_message = "\n".join(error)
    logger.error(constants.VALIDATION_ERROR.format(error_message=error_message))
    sys.exit(1)
