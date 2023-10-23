from typing import List
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.base import BaseEstimator
from sklearn.feature_extraction import DictVectorizer
from models import InputData

# Function to extract X and y using DictVectorizer
def extract_x_y(
    df: pd.DataFrame,
    dv: DictVectorizer = None,
    with_target: bool = True,
) -> dict:

    dicts = df.drop(columns=["Age"] if "Age" in df.columns else []).to_dict(orient="records")

    if dv is None:
        dv = DictVectorizer()
        dv.fit(dicts)

    x = dv.transform(dicts)

    y = None
    if with_target and "Age" in df.columns:
        y = df["Age"].values

    return x, y, dv

def run_inference(input_data: List[InputData], dv: DictVectorizer, model: BaseEstimator) -> np.ndarray:
    """Run inference on a list of input data.

    Args:
        payload (dict): the data point to run inference on.
        dv (DictVectorizer): the fitted DictVectorizer object.
        model (BaseEstimator): the fitted model object.

    Returns:
        np.ndarray: the predicted trip durations in minutes.

    """
    logger.info(f"Running inference on:\n{input_data}")
    df = pd.DataFrame([x.dict() for x in input_data])
    dicts = df.to_dict(orient="records")
    X = dv.transform(dicts)
    y = model.predict(X)
    logger.info(f"Predicted abalone age:\n{y}")
    return y