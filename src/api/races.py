from ..web import app, DEFAULT_PATH
from ..database.models import session, Race, Pilot, RaceLeaderboard, RaceLeaderboard
from fastapi import HTTPException
from pydantic import BaseModel, Field


class RaceRequest(BaseModel):
    name: str = Field(examples=["PistonCup"])
    laps: int = Field(examples=[15])


@app.get(f"{DEFAULT_PATH}/races", description="Get all races", tags=["Races"])
async def get_races():
    races = session.query(Race).all()
    return races


@app.get(
    f"{DEFAULT_PATH}/races/{{race_id}}", description="Get a race by ID", tags=["Races"]
)
async def get_race(race_id: int):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@app.get(
    f"{DEFAULT_PATH}/races/{{race_id}}/pilots",
    description="Get all pilots from a race",
    tags=["Races"],
)
async def get_race_pilots(race_id: int):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    pilots = (
        session.query(Pilot)
        .join(RaceLeaderboard)
        .filter(RaceLeaderboard.race_id == race_id)
        .all()
    )
    return pilots


@app.post(f"{DEFAULT_PATH}/races", description="Create a new race", tags=["Races"])
async def create_race(race_request: RaceRequest):
    if race_request.laps > 9223372036854775807:
        raise HTTPException(
            status_code=400,
            detail="Laps number is bigger than the maximum authorized : 9223372036854775807",
        )
    if race_request.laps < 1:
        raise HTTPException(
            status_code=400,
            detail="Laps number is lesser than the minimum authorized : 1",
        )

    race = Race(name=race_request.name, laps=race_request.laps)
    session.add(race)
    session.commit()
    return race


@app.put(
    f"{DEFAULT_PATH}/races/{{race_id}}",
    description="Update a race by ID",
    tags=["Races"],
)
async def update_race(race_id: int, race_request: RaceRequest):
    if race_request.laps > 9223372036854775807:
        raise HTTPException(
            status_code=400,
            detail="Laps number is bigger than the maximum authorized : 9223372036854775807",
        )
    if race_request.laps < 1:
        raise HTTPException(
            status_code=400,
            detail="Laps number is lesser than the minimum authorized : 1",
        )

    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")

    race.name = race_request.name
    race.laps = race_request.laps
    session.commit()
    return race


@app.delete(
    f"{DEFAULT_PATH}/races/{{race_id}}",
    description="Delete a race by ID",
    tags=["Races"],
)
async def delete_race(race_id: int):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    session.delete(race)
    session.commit()
    return race


@app.get(
    f"{DEFAULT_PATH}/races/{{race_id}}/leaderboard",
    description="Get the leaderboard of a race (sorted by position)",
    tags=["Races"],
)
async def get_leaderboard_from_race(race_id: int):
    race = session.query(Race).filter_by(id=race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    leaderboard = (
        session.query(RaceLeaderboard)
        .filter(RaceLeaderboard.race_id == race_id)
        .order_by(RaceLeaderboard.position)
        .all()
    )
    if not leaderboard:
        raise HTTPException(
            status_code=404, detail="Race not found or no leaderboard in the race"
        )
    return leaderboard
