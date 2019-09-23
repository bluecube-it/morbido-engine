from flask_restful import Resource, reqparse
from classes.tools import Tools

class Columns(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset')
        args = parser.parse_args()
        tools = Tools()
        return {'columns': tools.get_columns(args.dataset)}
