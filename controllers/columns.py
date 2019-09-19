from flask_restful import Resource, reqparse
from classes.tools import Tools

class Columns(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filename')
        args = parser.parse_args()
        tools = Tools()
        return {'columns': tools.get_columns(args.filename)}
