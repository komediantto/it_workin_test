from sqlalchemy import select

from app.db import User, async_session_maker


async def check_username(username):
    async with async_session_maker() as session:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        receiver = result.scalars().first()
        if receiver is None:
            return True
        else:
            return False
