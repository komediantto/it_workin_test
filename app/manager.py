from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, models, schemas
from loguru import logger

import app.config as cfg

from app.auth import auth_backend
from app.constants import USERNAME_ALREADY_EXIST
from app.db import User, get_user_db
from app.utils import check_username

SECRET = cfg.USER_SECRET_KEY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        if await check_username(user_create.username):
            user = await super().create(user_create, safe, request)
            return user
        else:
            raise HTTPException(
                status_code=403,
                detail=USERNAME_ALREADY_EXIST.format(username=user_create.username),
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
