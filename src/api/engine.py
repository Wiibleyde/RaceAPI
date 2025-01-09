from ..web import app, DEFAULT_PATH
from ..database.models import session, Race, Pilot, RaceLeaderboard, RaceLeaderboard
import json

@app.put(f"{DEFAULT_PATH}/swapPilots", description="Swap two pilots in the leaderboard", tags=["Race engine"])
async def swap_pilots(race_id: int, pilot1_id: int, pilot2_id: int):
    pilot1 = session.query(Pilot).filter_by(id=pilot1_id).first()
    if pilot1 is None:
        return {"error": "Pilot 1 is not found"}, 404
    pilot2 = session.query(Pilot).filter_by(id=pilot2_id).first()
    if pilot2 is None:
        return {"error": "Pilot 2 is not found"}, 404
    leaderboard = session.query(RaceLeaderboard).filter_by(race_id=race_id).all()
    leaderboard_pilot1 = None
    leaderboard_pilot2 = None
    for entry in leaderboard:
        if entry.pilot_id == pilot1_id:
            leaderboard_pilot1 = entry
        if entry.pilot_id == pilot2_id:
            leaderboard_pilot2 = entry
    if leaderboard_pilot1 is None:
        return {"error": "Pilot 1 is not in the leaderboard"}, 404
    if leaderboard_pilot2 is None:
        return {"error": "Pilot 2 is not in the leaderboard"}, 404
    leaderboard_pilot1.pilot_id = pilot2_id
    leaderboard_pilot2.pilot_id = pilot1_id
    session.commit()
    return leaderboard

@app.put(f"{DEFAULT_PATH}/updateLeaderboard", description="Update the leaderboard")
async def update_leaderboard(race_id: int, leaderboard: str):
    leaderboard_db = session.query(RaceLeaderboard).filter_by(race_id=race_id).all()
    leaderboard = json.loads(leaderboard)
    for entry in leaderboard:
        leaderboard_entry = None
        for entry_db in leaderboard_db:
            if entry_db.pilot_id == entry["pilot_id"]:
                leaderboard_entry = entry_db
        if leaderboard_entry is None:
            return {"error": "Pilot not found in the leaderboard"}, 404
        leaderboard_entry.position = entry["position"]
        leaderboard_entry.achievedLaps = entry["achievedLaps"]
        leaderboard_entry.pitstops = entry["pitstops"]
    session.commit()
    return leaderboard_db
