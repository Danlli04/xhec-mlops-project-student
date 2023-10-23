# This module is the training flow: it reads the data, preprocesses it, trains a model and saves it.

import argparse
import pandas as pd
from pathlib import Path
from utils import save_pickle
from preprocessing import compute_target, extract_x_y
from training import train_model

# Define the relative path to the data folder
DATA_FOLDER = Path("../../data")
MODELS_DIRPATH = Path("../../src/web_service/local_objects")

# Construct the path to your CSV file
trainset_path = DATA_FOLDER / "abalone.csv"

def load_data(path: str):
    return pd.read_csv(path)

def main(trainset_path: Path) -> None:
    """Train a model using the data at the given path and save the model (pickle)."""
    # Read data
    df = load_data(path=trainset_path)
    # Preprocess data
    df = compute_target(df)
    x, y, dv = extract_x_y(df)

    # Train model
    model = train_model(x, y)

    # Pickle model --> The model should be saved in pkl format the `src/web_service/local_objects` folder
    modelpath = MODELS_DIRPATH / "model.pkl"
    dvpath = MODELS_DIRPATH / "dv.pkl"
    save_pickle(path=modelpath, obj=model)
    save_pickle(path=dvpath, obj=dv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model using the data at the given path.")
    parser.add_argument("-t", "--trainset_path", type=str, default=str(trainset_path), help="Path to the training set")
    args = parser.parse_args()
    main(Path(args.trainset_path))
