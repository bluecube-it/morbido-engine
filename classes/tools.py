import numpy as np
import pandas as pd
from itertools import product
from dateutil.relativedelta import relativedelta
#from dateutil.relativedelta import *
import json
import datetime

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

    def convert_to_exp(self, values):
        return np.array(np.expm1(values))

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
        print(seasonality)
        return np.log1p(dataset).groupby(pd.Grouper(freq=seasonality)).mean()

    """
    montly_dataset:
        dataset: pandas(DataFrame, TimeSeries)
        month: int
    """

    def montly_dataset(self, dataset, month):
        months = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
        index = months.index(month) + 1
        print(index)
        return dataset[dataset.index.month == index]
    
    """
    index_placeholder:
        dataset: pandas(DataFrame, TimeSeries)
        start_date: string timestamp
        
        Add made up index to predict specific periods
    """
    def add_index_placeholder(self, dataset, start_date = '2000-01-01 00:00:00'):
        index = pd.date_range(start = start_date, freq=frequency, periods=steps)
        dataset.insert(1, 'tmp_index', index)
        dataset.reset_index(inplace=True)
        dataset.set_index('tmp_index', append=True, inplace=True, drop=True)
        return dataset

    """
    restore_index:
        dataset: pandas(DataFrame, TimeSeries)
        index: string

        Restores original index - use after add_index_placeholder()
    """
    def restore_index(self, dataset, index = 'index'):
        dataset.reset_index(inplace=True)
        dataset.set_index(index, inplace=True)
        return dataset
   
    """
    get_params_list:
        return a list of tuple of Sarima Params
    """

    def get_params_list(self, dataset, seasonality, value_column = 'values'):
        p = range(0, 5)
        q = range(0, 5)
        ## seasonal
        Q = range(0, 5)
        P = range(0, 5)
        
        d,D = self.set_trend_params(dataset, seasonality, value_column)
        return list(product(p,d,q,P,D,Q))

    """
    set_trend_params:
        dataset: pandas DataFrame
        seasonality: int

        Extracts trend and seasonality information from the dataset to determine the best d and D values.
        Note: '0.1' and '0.001' are the default threshold values, change them if needed.
    """
    def set_trend_params(self, dataset, seasonality, value_column = 'values'):
        data = dataset[value_column]
        listed_df = pd.Series(data.tolist())
        result =  listed_df.squeeze().autocorr(lag=seasonality)
        if result < 0.1 and result > -0.1:
            D = [0]
        else:
            D = [1]
        for i in range(1, seasonality - 1):
            result += np.abs(listed_df.autocorr(lag=i))
        if result / seasonality  < 0.1:
            d = [0]
            return d, D
        index = [0]
        for i in range(1,len(list(data))):
            index.append(i)
        coeffs = np.polyfit(index, list(data), deg = 1)
        slope = float(coeffs[-2])
        if slope < 0.001 and slope > -0.001:
            d = [0]
        else:
            d = range(1,2)
        return d,D
    """
    json_parse:
        start: DateTimeIndex, Index
        string: str, str(json)

    return the final json of the prediction
    """
    def json_parse(self, start, string, seasonality):
        new_json = []
        
        for el in json.loads(string)['data']:
            if seasonality == "M":
                start = start + relativedelta(months=+1, day=1)
            elif seasonality == "D":
                start = start + relativedelta(days=+1)
            new_json += [{'date': str(list(start)[0]), 'value': el['0']}]
        return {'data': new_json}