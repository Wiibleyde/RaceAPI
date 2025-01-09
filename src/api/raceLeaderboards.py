from ..web import app, DEFAULT_PATH
from ..database.models import session, RaceLeaderboard, Race, Pilot
from fastapi import HTTPException
from pydantic import BaseModel, Field


class RaceLeaderboardPostRequest(BaseModel):
    race_id: int = Field(examples=[1])
    pilot_id: int = Field(examples=[6])
    position: int = Field(examples=[3])
    achievedLaps: int = Field(examples=[1])
    pitstops: int = Field(examples=[False])


class RaceLeaderboardPutRequest(BaseModel):
    position: int = Field(examples=[3])
    achievedLaps: int = Field(examples=[1])
    pitstops: int = Field(examples=[False])


@app.get(
    f"{DEFAULT_PATH}/leaderboards",
    description="Get the race leaderboard",
    tags=["Leaderboard"],
)
async def get_leaderboards():
    leaderboard = session.query(RaceLeaderboard).all()
    return leaderboard


@app.get(
    f"{DEFAULT_PATH}/leaderboards/{{leaderboard_id}}",
    description="Get a race leaderboard entry by ID",
    tags=["Leaderboard"],
)
async def get_leaderboard(leaderboard_id: int):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    if leaderboard is None:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
    return leaderboard


@app.post(
    f"{DEFAULT_PATH}/leaderboards",
    description="Create a new race leaderboard entry",
    tags=["Leaderboard"],
)
async def create_leaderboard_entry(race_leaderboard_request: RaceLeaderboardPostRequest):
    race = session.query(Race).filter_by(id=race_leaderboard_request.race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race is not found")
    pilot = session.query(Pilot).filter_by(id=race_leaderboard_request.pilot_id).first()
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot is not found")
    leaderboard = RaceLeaderboard(
        race_id=race_leaderboard_request.race_id,
        pilot_id=race_leaderboard_request.pilot_id,
        position=race_leaderboard_request.position,
        achievedLaps=race_leaderboard_request.achievedLaps,
        pitstops=race_leaderboard_request.pitstops,
    )
    session.add(leaderboard)
    session.commit()
    return leaderboard


@app.put(
    f"{DEFAULT_PATH}/leaderboards/{{leaderboard_id}}",
    description="Update a race leaderboard entry by ID",
    tags=["Leaderboard"],
)
async def update_leaderboard_entry(
    leaderboard_id: int, race_leaderboard_request: RaceLeaderboardPutRequest
):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    if leaderboard is None:
        raise HTTPException(status_code=404, detail="Leaderboard entry not found")
    leaderboard.position = race_leaderboard_request.position
    leaderboard.achievedLaps = race_leaderboard_request.achievedLaps
    leaderboard.pitstops = race_leaderboard_request.pitstops
    session.commit()
    return leaderboard


@app.delete(
    f"{DEFAULT_PATH}/leaderboards/{{leaderboard_id}}",
    description="Delete a race leaderboard entry by ID",
    tags=["Leaderboard"],
)
async def delete_leaderboard_entry(leaderboard_id: int):
    leaderboard = session.query(RaceLeaderboard).filter_by(id=leaderboard_id).first()
    if leaderboard is None:
        raise HTTPException(status_code=404, detail="Leaderboard entry not found")
    session.delete(leaderboard)
    session.commit()
    return leaderboard
