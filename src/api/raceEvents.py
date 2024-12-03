from ..web import app, DEFAULT_PATH
from ..database.models import session, RaceEvent

@app.get(f"{DEFAULT_PATH}/raceEvents", description="Get all race events")
async def get_raceEvents():
    raceEvents = session.query(RaceEvent).all()
    return raceEvents

@app.get(f"{DEFAULT_PATH}/raceEvents/{{raceEvent_id}}", description="Get a race event by ID")
async def get_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    return raceEvent

@app.post(f"{DEFAULT_PATH}/raceEvents", description="Create a new race event")
async def create_raceEvent(race_id: int, type: int, sector: int):
    raceEvent = RaceEvent(race_id=race_id, type=type, sector=sector)
    session.add(raceEvent)
    session.commit()
    return raceEvent

@app.put(f"{DEFAULT_PATH}/raceEvents/{{raceEvent_id}}", description="Update a race event by ID")
async def update_raceEvent(raceEvent_id: int, type: int, sector: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        return
    raceEvent.type = type
    raceEvent.sector = sector
    session.commit()
    return raceEvent

@app.delete(f"{DEFAULT_PATH}/raceEvents/{{raceEvent_id}}", description="Delete a race event by ID")
async def delete_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        return
    session.delete(raceEvent)
    session.commit()
    return raceEvent