import numpy as np
import pandas as pd
from itertools import product

class Tools:
    def describe(self, filename):
        return pd.read_csv(filename).describe().to_json()

    """
    MAPE: 
        true, actual = float, int, np.array
    """
    def mean_absolute_percentage_error(self, true, actual):
        return np.mean(np.abs((true - actual) / true)) * 100

    """
    convert_to_exp:
        values: pandas(columns), np.array
        seasonality: int
    """

    def convert_to_exp(self, values, seasonality):
        for el in values:
            el = np.expm1(el / seasonality) * seasonality
        return values

    """
    convert_to_log:
        dataset: pandas(DataFrame, TimeSeries)
        seasonlity: string
            - "Y" annual
            - "M" mensile
            - "W" weekly
            - "D" daily
    """

    def convert_to_log(self, dataset, seasonality):
        return np.log1p(dataset).groupby(pd.Grouper(freq=seasonlity)).sum()
        
    """
    get_params_list:
        return a list of tuple of Sarima Params
    """

    def get_params_list(self):
        p = range(0, 5)
        q = range(0, 5)
        d = range(0, 2)
        ## seasonal
        Q = range(0, 5)
        P = range(0, 5)
        D = range(0, 1)
        return list(product(p, d, q, P, D ,Q))