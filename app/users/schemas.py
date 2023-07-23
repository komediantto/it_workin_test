from pydantic import BaseModel, constr, validator


class UserSearch(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str


class UserSchema(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: constr(min_length=11, max_length=11)

    @validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Номер телефона должен содержать только цифры")
        return phone_number


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
