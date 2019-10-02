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
        
        parser = reqparse.RequestParser()
        parser.add_argument('seasonality', type=str, required=True, help='missing seasonality')        
        parser.add_argument('precision', type=str, required=True, help='missing precision')
        parser.add_argument('filename', required=True, help='missing filename')
        parser.add_argument('index', type=str, required=True, help='missing index')
        parser.add_argument('input', type=str, required=True, help='missing input')
        parser.add_argument('prediction', type=int, required=True, help='missing precision')
        args = parser.parse_args()
        
        if args.seasonality == "yearly":
            args.prediction = args.prediction*12

        args.seasonality = 12
        
        forecasting = Sarima(args.seasonality, args.precision)
        
        return forecasting.get_prediction(args.filename, [args.index, args.input], args.prediction)
        """
        prova = Sarima(12, 'high')
        return prova.get_prediction('bitcoin_csv.csv', ['date', 'price(USD)'], 12)
        """
