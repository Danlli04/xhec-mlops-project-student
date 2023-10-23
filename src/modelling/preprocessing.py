from sklearn.feature_extraction import DictVectorizer
import pandas as pd

def compute_target(
    df: pd.DataFrame,
    rings_column: str = "Rings",
) -> pd.DataFrame:
    df["Age"] = df[rings_column] + 1.5
    df.drop("Rings", axis=1, inplace=True) 
    return df

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