from flask import Flask
from flask_restful import Api
from controllers.shape import Shape
from controllers.tried import Tried
from controllers.columns import Columns
from controllers.prediction import Prediction
# from controllers.neural import Neural

app = Flask(__name__)
api = Api(app)

api.add_resource(Tried, '/example/<string:word>')
api.add_resource(Shape, '/dataset/shape')
api.add_resource(Columns, '/dataset/columns')
api.add_resource(Prediction, '/forecasts/sarima')
#api.add_resource(Neural, '/forecasts/neural')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')#, port=int("80"))
