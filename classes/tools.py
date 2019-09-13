import numpy as np
import pandas as pd

class Tools:
    def describe(self, filename):
        return pd.read_csv(filename).describe().to_json()