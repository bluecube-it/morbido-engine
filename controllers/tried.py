from flask_restful import Resource
from classes.example import Example

class Tried(Resource):
    def get(self, word):
        ciao = Example()
        return {'hello': ciao.hello(word)}