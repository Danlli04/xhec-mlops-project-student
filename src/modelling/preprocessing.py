from sklearn.feature_extraction import DictVectorizer
import pandas as pd
from prefect import flow, task
from loguru import logger
import scipy.sparse
from typing import Tuple
import numpy as np
@task
def compute_target(
    df: pd.DataFrame,
    rings_column: str = "Rings",
) -> pd.DataFrame:
    df["Age"] = df[rings_column] + 1.5
    df.drop("Rings", axis=1, inplace=True) 
    return df

# Function to extract X and y using DictVectorizer
@task
def extract_x_y(
    df: pd.DataFrame,
    dv: DictVectorizer = None,
    with_target: bool = True,
) -> Tuple[scipy.sparse.csr_matrix, np.ndarray, DictVectorizer]:

    dicts = df.drop(columns=["Age"] if "Age" in df.columns else []).to_dict(orient="records")

    if dv is None:
        dv = DictVectorizer()
        dv.fit(dicts)

    x = dv.transform(dicts)

    y = None
    if with_target and "Age" in df.columns:
        y = df["Age"].values

    return x, y, dv

def load_data(path: str):
    return pd.read_csv(path)

@flow(name="Preprocess data")
def process_data(filepath: str, dv=None, with_target: bool = True) -> scipy.sparse.csr_matrix:
    """
    Load data from a csv file
    Turn features to sparce matrix
    :return The sparce matrix, the target' values and the
    dictvectorizer object if needed.
    """
    df = load_data(path=filepath)
    if with_target:
        logger.debug(f"{filepath} | Computing target...")
        df1 = compute_target(df)
        logger.debug(f"{filepath} | Extracting X and y...")
        return extract_x_y(df1, dv=dv)
    else:
        logger.debug(f"{filepath} | Extracting X and y...")
        return extract_x_y(df, dv=dv, with_target=with_target)