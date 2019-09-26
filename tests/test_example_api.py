import unittest
import app
import requests

class TestExample(unittest.TestCase):
    def test_example_api(self):
        response = requests.get('http://localhost:5000/example/world')
        self.assertEqual(response.json(), {'hello': 'world'})

    def test_example_variable_api(self):
        word = 'word'
        response = requests.get('http://localhost:5000/example/%s' % word)
        self.assertEqual(response.json(), {'hello': word})