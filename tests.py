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

    # Stable

    def test07_create_stable(self):
        stable_id = 3
        name = "Alpine"
        response = requests.post(url + "/stables", json={"name": name}, timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.json(), {"id": stable_id, "name": name})

    def test08_update_stable(self):
        stable_id = 3
        name = "Cars"
        response = requests.put(
            f"{url}/stables/{stable_id}", json={"name": name}, timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.json(), {"id": stable_id, "name": name})

    def test09_delete_stable(self):
        stable_id = 3
        response = requests.delete(f"{url}/stables/{stable_id}", timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/stables/{stable_id}")
        self.assertEqual(response.status_code, 404)

    # Pilots

    def test10_create_pilot(self):
        pilot_id = 5
        firstname = "Max"
        lastname = "Verstappen"
        stable_id = 2
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

    # Races

    def test13_create_race(self):
        race_id = 2
        name = "Zandvoort"
        laps = 79
        response = requests.post(
            f"{url}/races", json={"name": name, "laps": laps}, timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/races/{race_id}")
        self.assertEqual(response.json(), {"id": race_id, "name": name, "laps": laps})

    def test14_update_race(self):
        race_id = 2
        name = "Monza"
        laps = 53
        response = requests.put(
            f"{url}/races/{race_id}", json={"name": name, "laps": laps}, timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/races/{race_id}")
        self.assertEqual(response.json(), {"id": race_id, "name": name, "laps": laps})

    def test15_delete_race(self):
        race_id = 2
        response = requests.delete(
            f"{url}/races/{race_id}", timeout=2)
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/races/{race_id}")
        self.assertEqual(response.status_code, 404)

    # Leaderboards

    def test16_create_leaderboard(self):
        leaderboard_id = 4
        response = requests.post(
            f"{url}/leaderboards",
            json={
                "race_id": 1,
                "pilot_id": 1,
                "position": 1,
                "achievedLaps": 53,
                "pitstops": 1,
            },
            timeout=2,
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/leaderboards/{leaderboard_id}")
        self.assertEqual(
            response.json(),
            {
                "id": leaderboard_id,
                "race_id": 1,
                "pilot_id": 1,
                "position": 1,
                "achievedLaps": 53,
                "pitstops": 1,
            },
        )

    def test17_update_leaderboard(self):
        leaderboard_id = 4
        response = requests.put(
            f"{url}/leaderboards/{leaderboard_id}",
            json={"position": 2, "achievedLaps": 53, "pitstops": 1},
            timeout=2,
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/leaderboards/{leaderboard_id}")
        self.assertEqual(
            response.json(),
            {
                "id": leaderboard_id,
                "race_id": 1,
                "pilot_id": 1,
                "position": 2,
                "achievedLaps": 53,
                "pitstops": 1,
            },
        )

    def test18_delete_leaderboard(self):
        leaderboard_id = 4
        response = requests.delete(
            f"{url}/leaderboards/{leaderboard_id}", timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/leaderboards/{leaderboard_id}")
        self.assertEqual(response.status_code, 404)

    # Events

    def test19_create_event(self):
        event_id = 2
        race_id = 1
        type = "GREEN_FLAG"
        sector = 1
        response = requests.post(
            f"{url}/events",
            json={"race_id":race_id, "type": type, "sector": sector},
            timeout=2,
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/events/{event_id}")
        self.assertEqual(
            response.json(),
            {
                "id": event_id,
                "race_id": race_id,
                "type": 1,
                "sector": sector,
            },
        )

    def test20_update_event(self):
        event_id = 2
        race_id = 1
        type = "BLACK_FLAG"
        sector = 2
        response = requests.put(
            f"{url}/events/{event_id}",
            json={"type": type, "sector": sector},
            timeout=2,
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/events/{event_id}")
        self.assertEqual(
            response.json(),
            {
                "id": event_id,
                "race_id": race_id,
                "type": 5,
                "sector": sector,
            },
        )

    def test21_delete_event(self):
        event_id = 2
        response = requests.delete(
            f"{url}/events/{event_id}", timeout=2
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(f"{url}/events/{event_id}")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main(verbosity=2)
