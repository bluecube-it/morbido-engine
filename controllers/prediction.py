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
        #params = request.form['data
        parser = reqparse.RequestParser()
        #parser.add_argument('data')
        parser.add_argument('seasonality', type=int)        
        parser.add_argument('precision', type=str)
        parser.add_argument('filename')
        parser.add_argument('index', type=str)
        parser.add_argument('input', type=str)
        parser.add_argument('prediction')
        args = parser.parse_args()
        #params = json.loads(args.data)
        
        forecasting = Sarima(args.seasonality, args.precision)
        
        return forecasting.get_prediction(args.filename, [args.index, args.input], args.prediction)
        """
        prova = Sarima(12, 'medium')
        return json.loads(prova.get_prediction('dataset_finale.csv', ['date', 'values, 12))
        """
