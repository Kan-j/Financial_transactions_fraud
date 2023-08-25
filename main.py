from fastapi import FastAPI, Body, Depends, status, HTTPException
import models.user.user_model as models
from database import engine, SessionLocal
from typing_extensions import Annotated
from sqlalchemy.orm import Session
import auth.auth
from auth.auth import get_current_user,router

from pydantic import BaseModel
from models.mobile_money.mobilemoney_model import predict_fraud
from models.credit_card.creditcard_model import predict_creditcard_fraud
from models.mobile_money.mobilemoney_model import __version__ as model_version


# from models.user.user_model import UserSchema, UserLoginSchema
# from auth.auth_bearer import JWTBearer
# from auth.auth_handler import signJWT

users = []

# def check_user(data: UserLoginSchema):
#     for user in users:
#         if user.email == data.email and user.password == data.password:
#             return True
#     return False


app = FastAPI()
app.include_router(router)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DataIn(BaseModel):
    step: int
    type : str
    amount: float
    nameOrig: str
    oldBalanceOrg: float
    newBalanceOrig : float
    nameDest : str
    oldbalanceDest : float
    newbalanceDest: float


class CreditCardDataIn(BaseModel):
    amt : float
    state : float
    city_pop : float
    trans_hour :  int
    trans_month : int
    trans_dayofweek: float
    timedelta_last_trans: float
    cust_age : float
    lat_dist_cust_merch : float
    long_dist_cust_merch : float
    lat_dist_prev_merch : float
    long_dist_prev_merch : float
    category_misc_net :   int
    category_gas_transport :  int
    category_kids_pets : int
    category_home :int
    category_shopping_net :int
    category_food_dining :int
    category_personal_care :int
    category_grocery_pos :int
    category_entertainment :int
    category_shopping_pos :int
    category_misc_pos :int
    category_travel :int
    category_health_fitness :int
    gender_f :int


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# @app.post("/user/signup", tags=["user"])
# def create_user(user: UserSchema = Body(...)):
#     users.append(user) # replace with db call, making sure to hash the password first
#     return signJWT(user.email)


# @app.post("/user/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         return signJWT(user.email)
#     return {
#         "error": "Wrong login details!"
#     }

@app.get("/",status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication False')
    return {"User": user}

@app.post("/momo_fraud/predict",  tags= ['Momo Fraud'])
def predict(payload: DataIn, user: user_dependency, db: db_dependency):
    return predict_fraud(payload.step, payload.type,payload.amount, payload.nameOrig, payload.oldBalanceOrg, payload.newBalanceOrig,payload.nameDest,payload.oldbalanceDest,payload.newbalanceDest)



@app.post("/credit_card_fraud/predict", tags= ['Credit Card Fraud'])
def predict(payload: CreditCardDataIn, user: user_dependency, db: db_dependency):
    return predict_creditcard_fraud(payload)
