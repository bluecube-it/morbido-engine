import numpy as np
import pandas as pd
from itertools import product

class Tools:

    """
    get_dataset:
        filename: string
        columns: [string, string]
            columns[0]: index
            columns[1]: input
    """

    def get_dataset(self, filename, column):
        dateparser = lambda x: pd.datetime.strptime(x,'%Y-%m-%d %H:00')
        return pd.read_csv(filename, usecols=[column[0],  column[1]], index_col=[column[0]], parse_dates=[column[0]],  date_parser=dateparser)

    def shape(self, filename):
        return pd.read_csv(filename).shape

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
        return np.log1p(dataset).groupby(pd.Grouper(freq=seasonality)).sum()
        
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