from flask_restful import Resource
from classes.tools import Tools
from flask import json

class Describe(Resource):
    def get(self, filename):
        tool = Tools()
        return json.loads(tool.describe(filename))