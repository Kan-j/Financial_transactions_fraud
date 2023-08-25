import pickle 
from pathlib import Path
import pandas as pd
import numpy as np
from feature_engine.encoding import OneHotEncoder
from feature_engine.encoding import MeanEncoder
from feature_engine.transformation import YeoJohnsonTransformer
import xgboost as xgb

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent


with open(f"{BASE_DIR}/trained_credit_card_fraud_model-{__version__}.pkl", "rb") as f:
    model = pickle.load(f)



def predict_creditcard_fraud(payload):
    # data = [payload.amt, payload.state, payload.city_pop, payload.trans_hour, payload.trans_month, payload.trans_dayofweek, payload.timedelta_last_trans, payload.cust_age, payload.lat_dist_cust_merch, payload.long_dist_cust_merch, payload.lat_dist_prev_merch, payload.long_dist_prev_merch, payload.category_misc_net, payload.category_gas_transport, payload.category_kids_pets, payload.category_home, payload.category_shopping_net, payload.category_food_dining, payload.category_personal_care, payload.category_grocery_pos, payload.category_entertainment, payload.category_shopping_pos, payload.category_misc_pos, payload.category_travel, payload.category_health_fitness, payload.gender_f]
    
    # return "Hello"
    data_input = {
        "amt": [payload.amt],
        "state": [payload.state],
        "city_pop": [payload.city_pop],
        "trans_hour": [payload.trans_hour],
        "trans_month": [payload.trans_month],
        "trans_dayofweek": [payload.trans_dayofweek],
        "timedelta_last_trans": [payload.timedelta_last_trans],
        "cust_age": [payload.cust_age],
        "lat_dist_cust_merch": [payload.lat_dist_cust_merch],
        "long_dist_cust_merch": [payload.long_dist_cust_merch],
        "lat_dist_prev_merch": [payload.lat_dist_prev_merch],
        "long_dist_prev_merch": [payload.long_dist_prev_merch],
        "category_misc_net": [payload.category_misc_net],
        "category_gas_transport":[payload.category_gas_transport],
        "category_kids_pets": [payload.category_kids_pets],
        "category_home": [payload.category_home],
        "category_shopping_net": [payload.category_shopping_net],
        "category_food_dining": [payload.category_food_dining],
        "category_personal_care": [payload.category_personal_care],
        "category_grocery_pos": [payload.category_grocery_pos],
        "category_entertainment": [payload.category_entertainment],
        "category_shopping_pos": [payload.category_shopping_pos],
        "category_misc_pos": [payload.category_misc_pos],
        "category_travel": [payload.category_travel],
        "category_health_fitness": [payload.category_health_fitness],
        "gender_f": [payload.gender_f]
    }

    data = pd.DataFrame(data_input)
    predicted_value= model.predict(data)
    prediction_dict = {
        "value" : int(predicted_value),
        "Fraud status" : "Fraud" if int(predicted_value) else "Not Fraud"
    }
    return prediction_dict
    