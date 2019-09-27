from flask_restful import Resource, reqparse
from classes.tools import Tools

class Columns(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset', required=True)
        args = parser.parse_args()
        tools = Tools()
        #dataset = 'dataset_finale.csv'
        return {'columns': tools.get_columns(args.dataset)}
