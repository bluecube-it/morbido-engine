from flask import Flask
from flask import json
from flask_restful import Resource, Api
from classes.example import Example
from classes.tools import Tools

app = Flask(__name__)
api = Api(app)

class Tried(Resource):
    def get(self, word):
        ciao = Example()
        return {'hello': ciao.hello(word)}

class Describe(Resource):
    def get(self, filename):
        tool = Tools()
        return json.loads(tool.describe(filename))

api.add_resource(Tried, '/example/<string:word>')
api.add_resource(Describe, '/api/describe/<string:filename>')

if __name__ == '__main__':
    app.run(debug=True)