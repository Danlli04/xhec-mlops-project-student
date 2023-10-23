# This module is the training flow: it reads the data, preprocesses it, trains a model and saves it.

import argparse
import pandas as pd
from pathlib import Path
from typing import Optional
from utils import save_pickle
from training import train_model, predict, evaluate_model
from prefect import flow, serve
from loguru import logger
from preprocessing import process_data
from sklearn.model_selection import train_test_split

# Define the relative path to the data folder
DATA_FOLDER = Path("../../data")
MODELS_DIRPATH = Path("../../src/web_service/local_objects")

# Construct the path to your CSV file
trainset_path = DATA_FOLDER / "abalone.csv"

def load_data(path: str):
    return pd.read_csv(path)

@flow(name="Train model")
def train_model_workflow(
    train_filepath: str,
    artifacts_filepath: Optional[str] = None,
) -> dict:
    logger.info("Processing training data...")
    X, y, dv = process_data(filepath=train_filepath, with_target=True)
    logger.info("Training model...")
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # using 20% of data for testing

    # Train model
    model = train_model(X_train, y_train)

    # evaluate the model
    logger.info("Making predictions and evaluating...")
    y_pred = predict(X_test, model)
    rmse = evaluate_model(y_test, y_pred)

    # Pickle model --> The model should be saved in pkl format the `src/web_service/local_objects` folder
    modelpath = MODELS_DIRPATH / "model.pkl"
    dvpath = MODELS_DIRPATH / "dv.pkl"
    if artifacts_filepath is not None:
        logger.info(f"Saving artifacts to {artifacts_filepath}...")
        save_pickle(path=modelpath, obj=model)
        save_pickle(path=dvpath, obj=dv)

    return {"model": model, "dv": dv, "rmse": rmse}

if __name__ == "__main__":
    train_model_deployment = train_model_workflow.to_deployment(
        name="Model training Deployment",
        version="0.1.0",
        tags=["training", "model"],
        cron="0 0 * * 0",
        parameters={
            "train_filepath": trainset_path,
            "artifacts_filepath": MODELS_DIRPATH,
        },
    )
    serve(train_model_deployment)