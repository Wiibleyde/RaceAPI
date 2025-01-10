from ..web import app, DEFAULT_PATH
from ..database.models import session, RaceEvent, Race
from fastapi import HTTPException
from pydantic import BaseModel, Field


class RaceEventPostRequest(BaseModel):
    race_id: int = Field(examples=[1])
    type: str = Field(examples=[2])
    sector: int = Field(examples=[1])


class RaceEventPutRequest(BaseModel):
    type: str = Field(examples=[2])
    sector: int = Field(examples=[1])


@app.get(
    f"{DEFAULT_PATH}/events", description="Get all race events", tags=["Race events"]
)
async def get_raceEvents():
    raceEvents = session.query(RaceEvent).all()
    return raceEvents


@app.get(
    f"{DEFAULT_PATH}/events/{{raceEvent_id}}",
    description="Get a race event by ID",
    tags=["Race events"],
)
async def get_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        raise HTTPException(status_code=404, detail="Race event entry not found")
    return raceEvent


@app.post(
    f"{DEFAULT_PATH}/events",
    description="Create a new race event",
    tags=["Race events"],
)
async def create_raceEvent(race_event_request: RaceEventPostRequest):
    print("race")
    race = session.query(Race).filter_by(id=race_event_request.race_id).first()
    print("race sql finished")
    if race is None:
        print("no race")
        raise HTTPException(status_code=404, detail="Race not found")
    raceEvent = RaceEvent(
        race_id=race_event_request.race_id,
        type=race_event_request.type,
        sector=race_event_request.sector,
    )
    print("raceEvent")
    session.add(raceEvent)
    print("session")
    session.commit()
    print("commit")
    return raceEvent


@app.put(
    f"{DEFAULT_PATH}/events/{{raceEvent_id}}",
    description="Update a race event by ID",
    tags=["Race events"],
)
async def update_raceEvent(raceEvent_id: int, race_event_request: RaceEventPutRequest):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        raise HTTPException(status_code=404, detail="Race event not found")
    raceEvent.type = race_event_request.type
    raceEvent.sector = race_event_request.sector
    session.commit()
    return raceEvent


@app.delete(
    f"{DEFAULT_PATH}/events/{{raceEvent_id}}",
    description="Delete a race event by ID",
    tags=["Race events"],
)
async def delete_raceEvent(raceEvent_id: int):
    raceEvent = session.query(RaceEvent).filter_by(id=raceEvent_id).first()
    if raceEvent is None:
        raise HTTPException(status_code=404, detail="Race event not found")
    session.delete(raceEvent)
    session.commit()
    return raceEvent
