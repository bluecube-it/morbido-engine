from flask_restful import Resource
from classes.sarima import Sarima
from flask import request, json

class Prediction(Resource):
    """
    data:
        filename: string
        seasonality: int
        precision: sting
            - "low": only parsimonia
            - "medium": log and parsimonia
            - "high": TODO
        index: string
        input: string
        prediction:
            - int
            - string (month)
    """
    def post(self):
        params = request.form['data']
        
        forecasting = Sarima(params['seasonality'], params['precision'])
        
        return json.loads(forecasting.get_prediction(params['filename'], [params['index'], params['input']], params['prediction']))

        """
        usati per la prova
        prova = Sarima(12, 'low')
        return json.loads(prova.get_prediction('dataset_finale.csv', ['date', 'values'], 12))
        """
