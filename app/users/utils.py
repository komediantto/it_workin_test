from sqlalchemy import and_, select
from fastapi import HTTPException

from app.users.schemas import UserSchema, UserSearch


from app.core.models import User
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import USERS_NOT_FOUND

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def check_username(session, username):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    receiver = result.scalars().first()
    if receiver is None:
        return True
    else:
        return False


async def create_user(session: AsyncSession, new_user: UserSchema):
    hashed_password = pwd_context.hash(new_user.password)
    user = User(
        username=new_user.username,
        hashed_password=hashed_password,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone_number=new_user.phone_number,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def get_user(session, username):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


async def get_all_users(session):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


async def get_all_usernames(session):
    usernames = []
    users = await get_all_users(session)
    for user in users:
        usernames.append(user.username)
    return usernames


async def get_user_list(session, conditions=None):
    if conditions:
        query = select(User).where(and_(*conditions))
        result = await session.execute(query)
        users = result.scalars().all()

        user_search_results = [
            UserSearch(
                username=user.username,
                last_name=user.last_name,
                id=user.id,
                first_name=user.first_name,
                phone_number=user.phone_number,
            )
            for user in users
        ]

        if len(user_search_results) != 0:
            return user_search_results

        raise HTTPException(status_code=404, detail=USERS_NOT_FOUND)

    return await get_all_users(session)
