from sklearn.linear_model import LinearRegression
import scipy
from scipy.sparse import csr_matrix
import numpy as np
from prefect import task
from sklearn.metrics import mean_squared_error

@task(name="Train model")
def train_model(x_train: csr_matrix, y_train: np.ndarray):
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    return lr

@task(name="Make predictions")
def predict(X: scipy.sparse.csr_matrix, model: LinearRegression) -> np.ndarray:
    """Make predictions with a trained model"""
    return model.predict(X)


@task(name="Evaluate model")
def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate mean squared error for two arrays"""
    return mean_squared_error(y_true, y_pred, squared=False)