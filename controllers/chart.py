from flask_restful import Resource
from flask_restful import reqparse
from classes.tools import Tools

class Chart(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset', required=True)
        parser.add_argument('input', required=True, type=str)
        parser.add_argument('index', required=True, type=str)
        args = parser.parse_args()
        tools = Tools()

        return {'data': tools.json_dataset(args.dataset, [args.index, args.input]), 'name': 'Dataset'}