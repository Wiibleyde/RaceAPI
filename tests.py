import unittest
import requests

url = "http://localhost:8000/api/v1"

class TestApi(unittest.TestCase):
    def test_default_route(self):
        response = requests.get(url + "/")
        self.assertEqual(response.status_code, 200)

    def test_get_stables(self):
        response = requests.get(url + "/stables")
        self.assertEqual(response.status_code, 200)

    def test_get_pilots(self):
        response = requests.get(url + "/pilots")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()