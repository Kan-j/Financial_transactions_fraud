from database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)



# from pydantic import BaseModel, Field, EmailStr


# class UserSchema(BaseModel):
#     fullname: str = Field(...)
#     email: EmailStr = Field(...)
#     password: str = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "fullname": "Joe Doe",
#                 "email": "joe@xyz.com",
#                 "password": "any"
#             }
#         }

# class UserLoginSchema(BaseModel):
#     email: EmailStr = Field(...)
#     password: str = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "email": "joe@xyz.com",
#                 "password": "any"
#             }
#         }
