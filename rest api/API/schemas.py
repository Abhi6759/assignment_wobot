from pydantic import BaseModel, EmailStr, validator


# this is the base class for the accepting the token data
class Tokendata(BaseModel):
    token: str


class UserModel(Tokendata):
    name: str
    age: int
    city: str


class admindata(BaseModel):
    email: EmailStr
    password: str


class userData(BaseModel):
    name: str
    age: int
    city: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str


class NewAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('password')
    def password_validate(cls, password):
        if len(password) < 6:
            raise ValueError('Please Input atleast password of 6 characters')
        return password
