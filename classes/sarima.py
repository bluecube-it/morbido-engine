import warnings
import numpy as np
import pandas as pd
from threading import Thread
from itertools import product
from .tools import Tools
from statsmodels.tsa.statespace.sarimax import SARIMAX

#

class Sarima:
    """
    __init__:
        seasonality: int
        precison: sting
    """

    def __init__(self, seasonality, precision):
        self.seasonality = seasonality
        self.precison = precision

    def seasonality_to_string(self, seasonality):
        if seasonality == 30:
            return "D"
        elif seasonality == 7:
            return "W"
        elif seasonality == 12:
            return "M"
        else:
            return "NONE"

    """
    get_prediction:
        filename: string
        columns: list
            columns[0]: string, index
            columns[1]: string, input
        prediction: int
    """

    def get_prediction(self, filename, columns, prediction):
        tools = Tools()
        dataset = tools.get_dataset(filename, columns)
        string_seasonality = self.seasonality_to_string(self.seasonality)
        if self.precison == "high" or self.precison == "medium":
            dataset = tools.convert_to_log(dataset, string_seasonality)
        params_list = tools.get_params_list()
        model = self.cross_validation(dataset, params_list)
        
        return pd.DataFrame(model.forecast(prediction)).to_json(orient='table')

    """
    cross_validation:
        dataset: pandas DataFrame
        params_list: list 
    """

    def cross_validation(self, dataset, params_list):
        
        best_aic = float('inf')
        best_model = None
        for params in params_list:
            if self.precison == "low":
                if sum(params) < 7:
                    model = self.seasonal_arima(dataset, params)
            else:
               model = self.seasonal_arima(dataset, params)

            try:
                aic = model.aic
                if aic < best_aic:
                    best_aic = model.aic
                    best_model = model
            except:
                continue
        return best_model



    """
    seasonal_arima:
        dataset: pandas DataFrame
        params: tuple (p, d, q, P, D, Q)
    """
    def seasonal_arima(self, dataset, params):
        try:
            warnings.filterwarnings('ignore')
            return SARIMAX(dataset, order=(params[0], params[1], params[2]), trend='t', seasonal_order=(params[3], params[4], params[5], self.seasonality)).fit(disp=-1)
        except:
            return SARIMAX(dataset, order=(0,0,0), trend='t', seasonal_order=(0,0,0, self.seasonality)).fit(disp=-1)

