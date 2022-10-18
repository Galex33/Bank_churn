from joblib import load
import os

def get_model(country):
    simp_path = f"\models\{country}.joblib"
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    abs_path = f'{ROOT_DIR}{simp_path}'
    model = load(abs_path)
    return model

def get_prediction(df,country):
    model = get_model(country)
    prediction = model.predict_proba(df)
    return prediction

