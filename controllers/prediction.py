from flask_restful import Resource
from classes.sarima import Sarima
from flask import request, json

class Prediction(Resource):
    """
    data:
        filename: string
        seasonality: int
        precision: int
        index: string
        input: string
        prediction: int
    """
    def post(self):
        #params = request.form['data']
        #
        #forecasting = Sarima(params['seasonality'], params['precision'])
        #
        #return json.loads(forecasting.get_prediction(params['filename'], [params['index'], params['input']], params['prediction'])

        prova = Sarima(12, 'low')
        return json.loads(prova.get_prediction('dataset_finale.csv', ['date', 'values'], 12))