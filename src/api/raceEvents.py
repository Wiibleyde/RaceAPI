from ..web import app, DEFAULT_PATH
from ..database.models import session, RaceEvent, Race

@app.get(f"{DEFAULT_PATH}/events", description="Get all race events", tags=["Race events"])
async def get_raceEvents():
    raceEvents = session.query(RaceEvent).all()
    return raceEvents

@app.get(f"{DEFAULT_PATH}/events/{{raceEvent_id}}", description="Get a race event by ID", tags=["Race events"])
async def get_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    return raceEvent

@app.post(f"{DEFAULT_PATH}/events", description="Create a new race event", tags=["Race events"])
async def create_raceEvent(race_id: int, type: int, sector: int):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        return {"error": "Race is not found"}, 404
    raceEvent = RaceEvent(race_id=race_id, type=type, sector=sector)
    session.add(raceEvent)
    session.commit()
    return raceEvent

@app.put(f"{DEFAULT_PATH}/events/{{raceEvent_id}}", description="Update a race event by ID", tags=["Race events"])
async def update_raceEvent(raceEvent_id: int, type: int, sector: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        return
    raceEvent.type = type
    raceEvent.sector = sector
    session.commit()
    return raceEvent

@app.delete(f"{DEFAULT_PATH}/events/{{raceEvent_id}}", description="Delete a race event by ID", tags=["Race events"])
async def delete_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        return
    session.delete(raceEvent)
    session.commit()
    return raceEvent