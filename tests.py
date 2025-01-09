import unittest
import requests


url = "http://localhost:8000/api/v1"


class TestApi(unittest.TestCase):
    def test01_default_route(self):
        response = requests.get(url + "/", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test02_get_stables(self):
        response = requests.get(url + "/stables", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test03_get_pilots(self):
        response = requests.get(url + "/pilots", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test04_get_races(self):
        response = requests.get(url + "/races", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test05_get_raceLeaderboards(self):
        response = requests.get(url + "/leaderboards", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test06_get_raceEvents(self):
        response = requests.get(url + "/events", timeout=2)
        self.assertEqual(response.status_code, 200)

    def test07_create_stable(self):
        name = "Alpine"
        response = requests.post(
            url + "/stables", json={"name": name}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(url + "/stables/3")
        self.assertEqual(response.json(), {"id": 3, "name": name})

    def test08_update_stable(self):
        stable_id = 3
        name = "Red Bull"
        response = requests.put(
            f"{url}/stables/{stable_id}", json={"name": name}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.json(), {"id": stable_id, "name": name})
        
    def test09_delete_stable(self):
        stable_id = 3
        response = requests.delete(
            f"{url}/stables/{stable_id}", timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.status_code, 404)
        

if __name__ == "__main__":
    unittest.main(verbosity=2)
