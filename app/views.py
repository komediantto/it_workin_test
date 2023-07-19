from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants

from app.db import get_async_session
from app.manager import current_user
from app.models import Message, User
from app.schemas import MessageCreate, UserSearchResult
from app.utils import check_username

message_router = APIRouter(prefix="/messages", tags=["Сообщения"])
users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@message_router.post("/")
async def create_message(
    new_message: MessageCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.username == new_message.username)
    result = await session.execute(query)
    receiver = result.scalars().first()
    if receiver is not None:
        message = Message(
            text=new_message.text, author_id=user.id, receiver_id=receiver.id
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return {"message": f"Сообщение успешно отправлено юзеру {receiver.username}"}
    raise HTTPException(
        status_code=404,
        detail=constants.USER_NOT_FOUND.format(username=new_message.username),
    )


@message_router.get("/")
async def get_messages(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Message).where(Message.receiver_id == user.id)
    result = await session.execute(query)
    messages = result.scalars().all()
    logger.warning(len(messages))
    if len(messages) != 0:
        return messages
    raise HTTPException(status_code=404, detail=constants.NO_MESSAGES)


@message_router.get("/out")
async def get_sended_messages(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Message).where(Message.author_id == user.id)
    result = await session.execute(query)
    messages = result.scalars().all()
    if len(messages) != 0:
        return messages
    raise HTTPException(status_code=404, detail=constants.NO_SENDED_MESSAGES)


@users_router.get("/", response_model=List[UserSearchResult])
async def search_users(
    username: str = Query(default=None, description="По имени пользователя"),
    first_name: str = Query(default=None, description="По имени"),
    last_name: str = Query(default=None, description="По фамилии"),
    phone_number: str = Query(default=None, description="По номеру телефона"),
    session: AsyncSession = Depends(get_async_session),
):
    conditions = []

    if username:
        conditions.append(User.username == username)
    if first_name:
        conditions.append(User.first_name == first_name)
    if last_name:
        conditions.append(User.last_name == last_name)
    if phone_number:
        conditions.append(User.phone_number == phone_number)

    if conditions:
        query = select(User).where(and_(*conditions))
        result = await session.execute(query)
        users = result.scalars().all()

        user_search_results = [
            UserSearchResult(
                username=user.username,
                last_name=user.last_name,
                email=user.email,
                id=user.id,
                first_name=user.first_name,
                phone_number=user.phone_number,
            )
            for user in users
        ]

        if len(user_search_results) != 0:
            return user_search_results

        raise HTTPException(status_code=404, detail=constants.USERS_NOT_FOUND)

    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@users_router.patch("/me", response_model=UserSearchResult)
async def me_update(
    user: User = Depends(current_user),
    username: str = Query(default=None, description="Change username"),
    first_name: str = Query(default=None, description="Change first name"),
    last_name: str = Query(default=None, description="Change last name"),
    phone_number: str = Query(default=None, description="Change phone number"),
    session: AsyncSession = Depends(get_async_session),
):
    if username:
        if await check_username(username):
            user.username = username
        else:
            raise HTTPException(
                status_code=403,
                detail=constants.USERNAME_ALREADY_EXIST.format(username=username),
            )
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if phone_number:
        user.phone_number = phone_number
    await session.commit()
    return user
