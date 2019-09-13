from flask_restful import Resource
from classes.tools import Tools
from flask import json

class Describe(Resource):
    def get(self, filename):
        tool = Tools()
        shape = tool.describe(filename)
        return {'rows': shape[0], 'columns': shape[1]}