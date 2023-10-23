from models import InputData, PredictionOut
from utils import load_model, load_preprocessor
from pathlib import Path
from fastapi import FastAPI
from inference import run_inference
import sys
import os

# Add root directory to the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

MODEL_DIRPATH = Path("../web_service/local_objects/model.pkl")
DV_DIRPATH = Path("../web_service/local_objects/dv.pkl")

#PATH_TO_MODEL = f"web_service/local_objects/model.pkl"
#PATH_TO_DV = f"web_service/local_objects/dv.pkl"

app = FastAPI(title="Albano-age-prediction", description="TBD")
MODEL_VERSION = "0.0.1"
@app.get("/")
def home():
    return {"health_check": "OK", "model_version": MODEL_VERSION}

@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData) -> dict:
    dv = load_preprocessor(DV_DIRPATH)
    model = load_model(MODEL_DIRPATH)
    y = run_inference([payload], dv, model)
    return {"abalone_age_prediction": y[0]}
