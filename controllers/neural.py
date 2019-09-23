from flask_restful import Resource
from flask_restful import reqparse
from classes.lnn import LNN
from flask import request, json

class Neural(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('seasonality', type=str, required=True, help='missing seasonality')
        parser.add_argument('filename', required=True, help='missing filename')
        parser.add_argument('index', type=str, required=True, help='missing index')
        parser.add_argument('input', type=str, required=True, help='missing input')
        args = parser.parse_args()
        neural = LNN(args.seasonality)
        prediction = neural.predict(arg.filename, [arg.index, args.input])
        return {'prediction': prediction.tolist()}