import pickle 
from pathlib import Path

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent


with open(f"{BASE_DIR}/trained_momofraud_model-{__version__}.pkl", "rb") as f:
    model = pickle.load(f)


def predict_fraud(step, type, amount:float, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest:float, newbalanceDest:float):
    # I won't require nameOrig, nameDest
    errorbalanceOrg = newbalanceOrig + amount - oldbalanceOrg
    print(errorbalanceOrg)
    errorbalanceDest = oldbalanceDest + amount - newbalanceDest
    print( errorbalanceDest)
    HourOfDay = step % 24
    if type == "CASH_OUT":
        type_CASH_OUT = 1
        type_TRANSFER = 0
    elif type == "TRANSFER":
        type_TRANSFER = 1
        type_CASH_OUT = 0
    else :
        type_CASH_OUT = 0
        type_TRANSFER = 0
    X_test = [step,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        errorbalanceOrg,
        errorbalanceDest,
        HourOfDay,
        type_CASH_OUT,
        type_TRANSFER]
    [predicted_value] = model.predict([X_test])
    prediction_dict = {
        "value" : int(predicted_value),
        "Fraud status" : "Fraud" if int(predicted_value) else "Not Fraud"
    }
    return prediction_dict