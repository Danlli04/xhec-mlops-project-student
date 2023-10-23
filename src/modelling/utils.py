# Use this module to code a `pickle_object` function. This will be useful to pickle the model (and encoder if need be).
import pickle
from typing import Any

def save_pickle(path: str, obj: Any):
    with open(path, "wb") as f:
        pickle.dump(obj, f)