from datetime import timedelta, datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models.user.user_model import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'b1c311d94122dd28055acaaf3aabb6c4fd06e76e06c9fcf2'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        hashed_password = bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()
    return {'user status': 'user created'}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.email, user.id, timedelta(minutes=28))
    return {'access_token': token, 'token_type':'bearer'}

def authenticate_user(email: str, password:str, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id:int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         email :str = payload.get('sub')
         user_id:int = payload.get('id')
         if email is None or user_id is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
         return {'email': email, 'id': user_id}
     except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')