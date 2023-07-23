from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.utils import (
    create_message,
    get_messages,
    get_or_create_room,
    get_username,
)

from app.core.db import get_async_session
from app.core.models import User
from app.chat.manager import manager
from app.users.utils import check_username
from app.users.auth import get_current_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/chat", tags=["Чат"])


@router.get("/{username}")
async def open_chat(
    request: Request,
    username: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not await check_username(session, username):
        room = await get_or_create_room(session, user.username, username)
        messages = await get_messages(session, room.id)
        return templates.TemplateResponse(
            "chat.html",
            {
                "request": request,
                "room": room,
                "username": username,
                "messages": messages,
                "user": user,
            },
        )


@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await create_message(text=data, room_id=room_id, author_id=user_id)
            username = await get_username(user_id)
            for connection in manager.room_connections[room_id]:
                await connection.send_text(f"{username}: {data}")

    except WebSocketDisconnect:
        logger.warning("WebSocket disconnected")
