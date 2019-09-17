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
        self.models = []

    def seasonality_to_string(self, seasonality):
        if seasonality == 30:
            return "D"
        elif seasonality == 7:
            return "W"
        elif seasonality == 12:
            return "M"
        else:
            return "NONE"

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
        tools = Tools()
        dataset = tools.get_dataset(filename, columns)
        string_seasonality = self.seasonality_to_string(self.seasonality)
        if self.precison == "high" or self.precison == "medium":
            dataset = tools.convert_to_log(dataset, string_seasonality)
        if (self.seasonality == 31 or self.seasonality == 30) and type(prediction) == "string":
            dataset = tools.montly_dataset(dataset, prediction)
            prediction = self.int_prediction(prediction)
        params_list = tools.get_params_list(dataset, self.seasonality, columns[1])
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
        iterable = 0
        while iterable < len(params_list):
            queue = []
            for i in range(5):
                #try:
                t = Thread(target=self.seasonal_arima, args=(dataset, params_list[iterable + i] ))
                queue.append(t)
                #except:
                    #continue

            for q in queue:
                q.start()

            for q in queue:
                q.join()

            iterable += 5
        #for params in params_list:
        #    if self.precison == "low" or self.precison =="medium":
        #        if sum(params) < 7:
        #            model = self.seasonal_arima(dataset, params)
        #    elif self.precison == "high":
        #       model = self.seasonal_arima(dataset, params)

        for model in self.models:
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
         if self.precison == "low" or self.precison == "medium":   
            if sum(params) < 7:
                try:
                    warnings.filterwarnings('ignore')
                    self.models.append(SARIMAX(dataset, order=(params[0], params[1], params[2]), trend='t', seasonal_order=(params[3], params[4], params[5], self.seasonality)).fit(disp=-1))
                except:
                    print('Errore parametri')
                    pass

