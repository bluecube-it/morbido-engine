import numpy as np
import pandas as pd

class Tools:
    def describe(self, filename):
        return pd.read_csv(filename).describe().to_json()

    """
    MAPE: true, actual = float, int, np.array
    """
    def mean_absolute_percentage_error(self, true, actual):
        return np.mean(np.abs((true - actual) / true)) * 100