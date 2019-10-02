import warnings
import numpy as np
import pandas as pd
from threading import Thread
from itertools import product
from .tools import Tools
from statsmodels.tsa.statespace.sarimax import SARIMAX
from flask import abort
import gc
#import joblib as jb

class Sarima:
    """
    __init__:
        seasonality: int
        precison: sting
    """

    def __init__(self, seasonality, precision):
        self.seasonality = seasonality
        self.precison = precision
        self.models = []
        gc.enable()
    
    def int_prediction(self, prediction):
        if prediction == 'gen' or prediction == 'mar' or prediction == 'mag' or prediction == 'lug' or prediction == 'ago' or prediction == 'ott' or prediction == 'dic':
            return 31
        elif prediction == 'feb':
            return 28
        elif prediction == 'apr' or prediction == 'giu' or prediction == 'set' or prediction == 'nov':
            return 30

    """
    get_prediction:
        filename: string
        columns: list
            columns[0]: string, index
            columns[1]: string, input
        prediction: int
    """

    def get_prediction(self, filename, columns, prediction):
        ##try:
        ##    prediction = int(prediction)
        ##except:
        ##    prediction = prediction
        tools = Tools()
        graph = tools.json_dataset(filename, columns)
        dataset = tools.get_dataset(filename, columns)
        string_seasonality = tools.seasonality_to_string(self.seasonality)
        if self.precison == "high":
            dataset = tools.convert_to_log(dataset, string_seasonality)
        if (string_seasonality == "D") and type(prediction) == type("string"):
            dataset = tools.montly_dataset(dataset, prediction)
            prediction = self.int_prediction(prediction)
        params_list = tools.get_params_list(dataset, self.seasonality, columns[1])
        index = pd.to_datetime(dataset.index[-1:]).date

        model = self.cross_validation(dataset[columns[1]], params_list)
        if self.precison == "low":
            predicted = model.forecast(prediction)[columns[1]]
        elif self.precison == "high":
            forecast = model.forecast(prediction)
            predicted = pd.DataFrame(tools.convert_to_exp(forecast)).to_json(orient='table')

        gc.collect()
        return {'data': tools.json_parse(index, predicted, string_seasonality), 'dataset': graph}

    """
    cross_validation:
        dataset: pandas DataFrame
        params_list: list 
    """

    def cross_validation(self, dataset, params_list):
        
        best_aic = float('inf')
        best_model = None
        iterable = 0
        while iterable < len(params_list):
            queue = []
            for i in range(5):
                #print(iterable, i)
                try:
                    t = Thread(target=self.seasonal_arima, args=(dataset, params_list[iterable + i] ))
                    queue.append(t)
                    t.start()
                except:
                    continue

            for q in queue:
                q.join()

            iterable += 5

        if len(self.models) == 0:
            abort(500, {'error': 'No forecasts available for this choice'})

        for model in self.models:
            try:
                aic = model.aic
                if aic < best_aic:
                    best_aic = model.aic
                    best_model = model
            except:
                continue
        #jb.dump(best_model, 'model.pkl')
        return best_model

    def period(self):
        if self.seasonality == 31 or self.seasonality == 30 or self.seasonality == 29 or self.seasonality == 28:
            return 1
        elif self.seasonality == 12:
            return 30
        else:
            return self.seasonality

    """
    seasonal_arima:
        dataset: pandas DataFrame
        params: tuple (p, d, q, P, D, Q)
    """
    def seasonal_arima(self, dataset, params):
        #if self.precison == "low" or self.precison == "medium":   
        if sum(params) < 7:
            try:
                warnings.filterwarnings('ignore')
                self.models.append(SARIMAX(dataset, order=(params[0], params[1], params[2]), trend='t', seasonal_order=(params[3], params[4], params[5], self.seasonality)).fit(disp=-1))
            except:
                pass

