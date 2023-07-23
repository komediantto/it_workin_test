from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fuzzywuzzy import process
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import constants
from app.core.db import get_async_session
from app.core.models import User
from app.users.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.users.schemas import Token, UserSchema, UserSearch
from app.users.utils import (
    check_username,
    create_user,
    get_all_usernames,
    get_user_list,
)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/register")
async def register(
    new_user: UserSchema, session: AsyncSession = Depends(get_async_session)
):
    if await check_username(session, new_user.username):
        await create_user(session, new_user)
        return {"message": constants.USER_CREATED.format(username=new_user.username)}
    else:
        raise HTTPException(
            status_code=400,
            detail=constants.USERNAME_ALREADY_EXIST.format(username=new_user.username),
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[UserSearch])
async def search_users(
    username: str = Query(default=None, description="По имени пользователя"),
    first_name: str = Query(default=None, description="По имени"),
    last_name: str = Query(default=None, description="По фамилии"),
    phone_number: str = Query(default=None, description="По номеру телефона"),
    session: AsyncSession = Depends(get_async_session),
):
    conditions = []

    if username:
        fuzzy_usernames = process.extractBests(
            username, await get_all_usernames(session), score_cutoff=80
        )
        usernames = [username[0] for username in fuzzy_usernames]
        conditions.append(User.username.in_(usernames))
    if first_name:
        conditions.append(User.first_name == first_name)
    if last_name:
        conditions.append(User.last_name == last_name)
    if phone_number:
        conditions.append(User.phone_number == phone_number)

    users = await get_user_list(session=session, conditions=conditions)
    return users


@router.patch("/me", response_model=UserSearch)
async def me_update(
    user: User = Depends(get_current_user),
    username: str = Query(default=None, description="Change username"),
    first_name: str = Query(default=None, description="Change first name"),
    last_name: str = Query(default=None, description="Change last name"),
    phone_number: str = Query(default=None, description="Change phone number"),
    session: AsyncSession = Depends(get_async_session),
):
    if username:
        if await check_username(session, username):
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
