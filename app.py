from flask import Flask
from flask_restful import Api
from controllers.shape import Shape
from controllers.tried import Tried
from controllers.prediction import Prediction

app = Flask(__name__)
api = Api(app)

api.add_resource(Tried, '/example/<string:word>')
api.add_resource(Shape, '/dataset/shape')
api.add_resource(Prediction, '/predict/sarima')

if __name__ == '__main__':
    app.run(debug=True)