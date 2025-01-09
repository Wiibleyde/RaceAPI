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
        stable_id = 4
        name = "Alpine"
        response = requests.post(url + "/stables", json={"name": name}, timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.json(), {"id": stable_id, "name": name})

    def test08_update_stable(self):
        stable_id = 4
        name = "Cars"
        response = requests.put(
            f"{url}/stables/{stable_id}", json={"name": name}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.json(), {"id": stable_id, "name": name})

    def test09_delete_stable(self):
        stable_id = 4
        response = requests.delete(f"{url}/stables/{stable_id}", timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.status_code, 404)
        
    def test10_create_pilot(self):
        pilot_id = 5
        firstname = "Max"
        lastname = "Verstappen"
        stable_id = 3
        nationality = "Dutch"
        response = requests.post(
            url + "/pilots", json={"firstname": firstname, "lastname": lastname, "stable_id": stable_id, "nationality": nationality}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/pilots/{pilot_id}")
        self.assertEqual(response.json(), {"id": pilot_id, "firstname": firstname, "lastname": lastname, "stable_id": stable_id, "nationality": nationality})

    def test11_update_pilot(self):
        pilot_id = 5
        stable_id = 1
        firstname = "Jean"
        lastname = "Jeannot"
        stable_id = 2
        nationality = "Français"
        response = requests.put(
            f"{url}/pilots/{pilot_id}", json={"firstname": firstname, "lastname": lastname, "stable_id": stable_id, "nationality": nationality}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/pilots/{pilot_id}")
        self.assertEqual(response.json(), {"id": pilot_id, "firstname": firstname, "lastname": lastname, "stable_id": stable_id, "nationality": nationality})
        
    def test12_delete_pilot(self):
        pilot_id = 5
        response = requests.delete(
            f"{url}/pilots/{pilot_id}", timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/pilots/{pilot_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
