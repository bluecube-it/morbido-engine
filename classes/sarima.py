import warnings
import numpy as np
import pandas as pd
from threading import Thread
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX

class Sarima:
    def hello(self, word):
        return word