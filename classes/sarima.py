import warnings
import numpy as np
import pandas as pd
from threading import Thread
from itertools import product
from tools import Tools
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings('ignore')

class Sarima:
    def get_prediction(self, filename, columns, seasonality):
        tools = Tools()
        dataset = tools.get_dataset(filename, columns)
        
