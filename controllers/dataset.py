from flask_restful import Resource, reqparse
from classes.tools import Tools
import json

class Dataset(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset', required=True)
        parser.add_argument('index', required=True, type=str)
        parser.add_argument('input', required=True, type=str)
        args = parser.parse_args()
        
        helper = Tools()

        data = helper.get_dataset(args.dataset, [args.index, args.input])
        response = []
        for i in range(len(data)):
            response += [{'date': str(data.index[i]), 'value': data[args.input][i]}]

        return {'data': response}

