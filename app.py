from flask import Flask
from flask_restful import Api
from controllers.describe import Describe
from controllers.tried import Tried

app = Flask(__name__)
api = Api(app)

api.add_resource(Tried, '/example/<string:word>')
api.add_resource(Describe, '/api/describe/<string:filename>')

if __name__ == '__main__':
    app.run(debug=True)