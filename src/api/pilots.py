from ..web import app, DEFAULT_PATH
from ..database.models import session, Stable, Pilot
from fastapi import HTTPException
from pydantic import BaseModel, Field


class PilotRequest(BaseModel):
    firstname: str = Field(examples=["Michel"])
    lastname: str = Field(examples=["Michelin"])
    stable_id: int = Field(examples=[1])
    nationality: str = Field(examples=["Français"])


@app.get(f"{DEFAULT_PATH}/pilots", description="Get all pilots", tags=["Pilots"])
async def get_pilots():
    pilots = session.query(Pilot).all()
    return pilots


@app.get(f"{DEFAULT_PATH}/pilots/{{pilot_id}}", description="Get a pilot by ID", tags=["Pilots"])
async def get_pilot(pilot_id: int):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return pilot


@app.post(f"{DEFAULT_PATH}/pilots", description="Create a new pilot", tags=["Pilots"])
async def create_pilot(pilot_request: PilotRequest):
    stable = session.query(Stable).filter_by(id=pilot_request.stable_id).first()
    if stable is None:
        raise HTTPException(status_code=404, detail="Stable not found with the provided id")
    pilot = Pilot(
        firstname=pilot_request.firstname,
        lastname=pilot_request.lastname,
        stable_id=pilot_request.stable_id,
        nationality=pilot_request.nationality,
    )
    session.add(pilot)
    session.commit()
    return pilot


@app.put(
    f"{DEFAULT_PATH}/pilots/{{pilot_id}}",
    description="Update a pilot by ID",
    tags=["Pilots"],
)
async def update_pilot(pilot_id: int, pilot_request: PilotRequest):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    stable = session.query(Stable).filter_by(id=pilot_request.stable_id).first()
    if stable is None:
        raise HTTPException(status_code=404, detail="Stable not found with the provided id")
    pilot.firstname = pilot_request.firstname
    pilot.lastname = pilot_request.lastname
    pilot.stable_id = pilot_request.stable_id
    pilot.nationality = pilot_request.nationality
    session.commit()
    return pilot


@app.delete(
    f"{DEFAULT_PATH}/pilots/{{pilot_id}}",
    description="Delete a pilot by ID",
    tags=["Pilots"],
)
async def delete_pilot(pilot_id: int):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    session.delete(pilot)
    session.commit()
    return pilot
