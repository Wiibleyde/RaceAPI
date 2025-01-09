import unittest
import requests

url = "http://localhost:8000/api/v1"

class TestApi(unittest.TestCase):
    def test_default_route(self):
        response = requests.get(url + "/", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test_get_stables(self):
        response = requests.get(url + "/stables", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test_get_pilots(self):
        response = requests.get(url + "/pilots", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test_get_races(self):
        response = requests.get(url + "/races", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test_get_raceLeaderboards(self):
        response = requests.get(url + "/leaderboards", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test_get_raceEvents(self):
        response = requests.get(url + "/events", timeout=2)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()