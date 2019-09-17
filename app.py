from flask import Flask
from flask_restful import Api
from controllers.describe import Describe
from controllers.tried import Tried
from controllers.prediction import Prediction

app = Flask(__name__)
api = Api(app)

api.add_resource(Tried, '/example/<string:word>')
api.add_resource(Describe, '/api/describe/<string:filename>')
api.add_resource(Prediction, '/api/predict')

if __name__ == '__main__':
    app.run(debug=True)
