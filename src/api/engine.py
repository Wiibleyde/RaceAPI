from ..web import app, DEFAULT_PATH
from ..database.models import session, Race, Pilot, RaceLeaderboard, RaceLeaderboard
import json
from fastapi import HTTPException
from pydantic import BaseModel, Field


class PilotSwap(BaseModel):
    race_id: int = Field(examples=[2])
    pilot1_id: int = Field(examples=[1])
    pilot2_id: int = Field(examples=[3])


class LeaderboardUpdate(BaseModel):
    race_id: int = Field(examples=[2])
    leaderboard: str = Field(examples=["Leaderboard on json format"])


@app.put(
    f"{DEFAULT_PATH}/swapPilots",
    description="Swap two pilots in the leaderboard",
    tags=["Race engine"],
)
async def swap_pilots(race_id: int, pilot_swap: PilotSwap):
    pilot1 = session.query(Pilot).filter_by(id=pilot_swap.pilot1_id).first()
    if pilot1 is None:
        raise HTTPException(status_code=404, detail="Pilot 1 not found")
    pilot2 = session.query(Pilot).filter_by(id=pilot_swap.pilot2_id).first()
    if pilot2 is None:
        raise HTTPException(status_code=404, detail="Pilot 2 not found")
    leaderboard = session.query(RaceLeaderboard).filter_by(race_id=race_id).all()
    leaderboard_pilot1 = None
    leaderboard_pilot2 = None
    for entry in leaderboard:
        if entry.pilot_id == pilot_swap.pilot1_id:
            leaderboard_pilot1 = entry
        if entry.pilot_id == pilot_swap.pilot2_id:
            leaderboard_pilot2 = entry
    if leaderboard_pilot1 is None:
        raise HTTPException(status_code=404, detail="Pilot 1 is not in the leaderboard")
    if leaderboard_pilot2 is None:
        raise HTTPException(status_code=404, detail="Pilot 2 is not in the leaderboard")
    leaderboard_pilot1.pilot_id = pilot_swap.pilot2_id
    leaderboard_pilot2.pilot_id = pilot_swap.pilot1_id
    session.commit()
    return leaderboard


@app.put(
    f"{DEFAULT_PATH}/updateLeaderboard",
    description="Update the leaderboard",
    tags=["Race engine"],
)
async def update_leaderboard(leaderboard_update: LeaderboardUpdate):
    leaderboard_db = (
        session.query(RaceLeaderboard)
        .filter_by(race_id=leaderboard_update.race_id)
        .all()
    )
    leaderboard = json.loads(leaderboard_update.leaderboard)
    for entry in leaderboard:
        leaderboard_entry = None
        for entry_db in leaderboard_db:
            if entry_db.pilot_id == entry["pilot_id"]:
                leaderboard_entry = entry_db
        if leaderboard_entry is None:
            raise HTTPException(status_code=404, detail="Pilot not found in the leaderboard")
        leaderboard_entry.position = entry["position"]
        leaderboard_entry.achievedLaps = entry["achievedLaps"]
        leaderboard_entry.pitstops = entry["pitstops"]
    session.commit()
    return leaderboard_db
