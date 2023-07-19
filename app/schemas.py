from fastapi_users import schemas
from pydantic import BaseModel, constr, validator


class UserSearchResult(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str
    phone_number: constr(min_length=11, max_length=11)

    @validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Номер телефона должен содержать только цифры")
        return phone_number


class UserUpdate(schemas.BaseUserUpdate):
    pass


class MessageCreate(BaseModel):
    text: str
    username: str
