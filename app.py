from flask import Flask
from flask_restful import Resource, Api
from helpers.sarima import Sarima

app = Flask(__name__)
api = Api(app)

class Describe(Resource):
    def get(self, word):
        ciao = Sarima()
        return {'hello': ciao.hello(word)}

api.add_resource(Describe, '/<string:word>')

if __name__ == '__main__':
    app.run(debug=True)