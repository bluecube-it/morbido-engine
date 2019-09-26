import unittest
import app
import requests
import csv
import io

class TestShape(unittest.TestCase):
    def test_post_request(self):
        data = dict(
            dataset = io.open('dataset_finale.csv', 'r')
        )
        response = requests.post('http://localhost:5000/dataset/shape', data=data)
        self.assertEqual(response.json(), {'rows': 0, 'columns': 2})

    def test_post_missing_param_request(self):
        response = requests.post('http://localhost:5000/dataset/shape')
        self.assertEqual(response.json(), {'message': {'dataset': 'dataset required'}})
    
    def test_get_missing_param_request(self):
        response = requests.get('http://localhost:5000/dataset/shape')
        self.assertEqual(response.json(), {'message': 'The method is not allowed for the requested URL.'})

    