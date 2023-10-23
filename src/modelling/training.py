from sklearn.linear_model import LinearRegression
from scipy.sparse import csr_matrix
import numpy as np

def train_model(x_train: csr_matrix, y_train: np.ndarray):
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    return lr