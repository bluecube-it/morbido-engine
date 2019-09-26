import unittest
import pandas as pd
from dateutil.parser import parse
from classes.tools import Tools

class TestTools(unittest.TestCase):

    def test_seasonality_generate(self):
        helper = Tools()
        dataset = pd.read_csv('dataset_finale.csv', usecols=['date', 'values'])
        seasonality = 12
        result = helper.seasonality_generate(dataset['values'], seasonality)
        for i in range(len(result)):
            self.assertEqual(len(result[i]), seasonality)

    def test_seasonality_to_string(self):
        helper = Tools()
        seasonalities = [
            {'string': 'W', 'int': 7},
            {'string': 'M', 'int': 12},
            {'string': 'D', 'int': 28},
            {'string': 'D', 'int': 29},
            {'string': 'D', 'int': 30},
            {'string': 'D', 'int': 31},
            #{'string': {'error': 'invalid seasonlaity'} , 'int': 40},
        ]
        for el in seasonalities:
            string = helper.seasonality_to_string(el['int'])
            self.assertEqual(string, el['string'])
            
    def test_montly_dataset(self):
        helper = Tools()
        dateparser = lambda x: parse(x)
        dataset = pd.read_csv('dataset_finale.csv', usecols=['date', 'values'], index_col=['date'], parse_dates=['date'], date_parser=dateparser)
        month = [
            {'str': 'gen', 'int': 1},
            {'str': 'feb', 'int': 2},
            {'str': 'mar', 'int': 3},
            {'str': 'apr', 'int': 4},
            {'str': 'mag', 'int': 5},
            {'str': 'giu', 'int': 6},
            {'str': 'lug', 'int': 7},
            {'str': 'ago', 'int': 8},
            {'str': 'set', 'int': 9},
            {'str': 'ott', 'int': 10},
            {'str': 'nov', 'int': 11},
            {'str': 'dic', 'int': 12},
        ]
        for m in month:
            parsed = helper.montly_dataset(dataset['values'], m['str'])
            for el in parsed.index.month:
                self.assertEqual(el, m['int'])

    def test_dataset_prepare_yearly(self):
        helper = Tools()
        dateparser = lambda x: parse(x)
        dataset = pd.read_csv('dataset_finale.csv', usecols=['date', 'values'], index_col=['date'], parse_dates=['date'], date_parser=dateparser)
        seasonality = 12
        string = helper.seasonality_to_string(seasonality)
        data = helper.convert_to_log(dataset['values'], string)
        self.assertEqual(len(data) % seasonality, 0)
        ## XXX con le altre fallisce riflettere
    
    
if __name__ == "__main__":
    unittest.main()
