from ..web import app, DEFAULT_PATH
from ..database.models import session, RaceLeaderboard, Race, Pilot

@app.get(f"{DEFAULT_PATH}/leaderboard", description="Get the race leaderboard", tags=["Leaderboard"])
async def get_leaderboard():
    leaderboard = session.query(RaceLeaderboard).all()
    return leaderboard

@app.get(f"{DEFAULT_PATH}/leaderboard/{{leaderboard_id}}", description="Get a leaderboard entry by ID", tags=["Leaderboard"])
async def get_leaderboard_entry(leaderboard_id: int):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    return leaderboard

@app.post(f"{DEFAULT_PATH}/leaderboard", description="Create a new leaderboard entry", tags=["Leaderboard"])
async def create_leaderboard_entry(race_id: int, pilot_id: int, position: int, achievedLaps: int, pitstops: bool):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        return {"error": "Race is not found"}, 404
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        return {"error": "Pilot is not found"}, 404
    leaderboard = RaceLeaderboard(race_id=race_id, pilot_id=pilot_id, position=position, achievedLaps=achievedLaps, pitstops=pitstops)
    session.add(leaderboard)
    session.commit()
    return leaderboard

@app.put(f"{DEFAULT_PATH}/leaderboard/{{leaderboard_id}}", description="Update a leaderboard entry by ID", tags=["Leaderboard"])
async def update_leaderboard_entry(leaderboard_id: int, position: int, achievedLaps: int, pitstops: bool):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    if leaderboard is None:
        return {"error": "Leaderboard entry not found"}, 404
    leaderboard.position = position
    leaderboard.achievedLaps = achievedLaps
    leaderboard.pitstops = pitstops
    session.commit()
    return leaderboard

@app.delete(f"{DEFAULT_PATH}/leaderboard/{{leaderboard_id}}", description="Delete a leaderboard entry by ID", tags=["Leaderboard"])
async def delete_leaderboard_entry(leaderboard_id: int):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    if leaderboard is None:
        return {"error": "Leaderboard entry not found"}, 404
    session.delete(leaderboard)
    session.commit()
    return leaderboard
