from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.models import Room, Message, User
from app.core.db import async_session_maker


async def create_message(text: str, room_id: int, author_id: int):
    async with async_session_maker() as session:
        message = Message(text=text, room_id=room_id, author_id=author_id)
        session.add(message)
        await session.commit()
        await session.refresh(message)


async def get_messages(session, room_id):
    query = (
        select(Message)
        .filter(Message.room_id == room_id)
        .options(selectinload(Message.author))
    )
    result = await session.execute(query)
    messages = result.scalars().all()
    return messages


async def get_or_create_room(session, user1, user2):
    sorted_names = "_".join(sorted([user1, user2]))
    query = select(Room).where(Room.name == sorted_names)
    result = await session.execute(query)
    room = result.scalars().first()
    if room is not None:
        return room
    room = Room(name=sorted_names)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def get_username(user_id):
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user.username
