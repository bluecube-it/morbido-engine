from flask_restful import Resource
from flask_restful import reqparse
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
            - string (month) "todo"
    """
    def post(self):
        #params = request.form['data']
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        args = parser.parse_args()
        params = json.loads(args.data)
        forecasting = Sarima(params['seasonality'], params['precision'])
        
        return forecasting.get_prediction(params['filename'], [params['index'], params['input']], params['prediction'])
        """
        prova = Sarima(12, 'medium')
        return json.loads(prova.get_prediction('dataset_finale.csv', ['date', 'values'], 12))
        """
