from flask_restful import Resource, reqparse
from classes.tools import Tools

parser = reqparse.RequestParser()

class Shape(Resource):
    def post(self):
        # Params
        parser.add_argument('dataset', required=True, help='dataset required')
        args = parser.parse_args()
        # Init tools
        tool = Tools()
        shape = tool.shape(args.dataset)

        return {'rows': shape[0], 'columns': shape[1]}