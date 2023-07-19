from fastapi import FastAPI

from app.auth import auth_backend
from app.manager import fastapi_users
from app.schemas import UserCreate, UserRead
from app.views import message_router, users_router

app = FastAPI(title="Messenger")

app.include_router(message_router)
app.include_router(users_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
