from fastapi import FastAPI
from loguru import logger
from app.core.config import check_database_connection, settings

from app.users.views import router as users_router
from app.chat.views import router as chat_router

app = FastAPI(title="Messenger")


@app.on_event("startup")
async def startup_event():
    await check_database_connection(settings)
    logger.info("FastAPI startup completed.")


app.include_router(chat_router)
app.include_router(users_router)
