from ..web import app, DEFAULT_PATH
from ..database.models import session, Stable, Pilot
from pydantic import BaseModel, Field
from fastapi import HTTPException


class StableRequest(BaseModel):
    name: str = Field(examples=["Ferrari"])


@app.get(f"{DEFAULT_PATH}/stables", description="Get all stables", tags=["Stables"])
async def get_stables():
    stables = session.query(Stable).all()
    return stables

@app.get(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Get a stable by ID", tags=["Stables"])
async def get_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        raise HTTPException(status_code=404, detail="Stable not found")
    return stable

@app.post(f"{DEFAULT_PATH}/stables", description="Create a new stable", tags=["Stables"])
async def create_stable(stable_request: StableRequest):
    stable = Stable(name=stable_request.name)
    session.add(stable)
    session.commit()
    return stable

@app.put(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Update a stable by ID", tags=["Stables"])
async def update_stable(stable_id: int, stable_request: StableRequest):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        raise HTTPException(status_code=404, detail="Stable not found")
    stable.name = stable_request.name
    session.commit()
    return stable

@app.delete(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Delete a stable by ID", tags=["Stables"])
async def delete_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        raise HTTPException(status_code=404, detail="Stable not found")
    session.delete(stable)
    session.commit()
    return stable

@app.get(f"{DEFAULT_PATH}/stables/{{stable_id}}/pilots", description="Get all pilots from a stable", tags=["Stables"])
async def get_pilots_from_stable(stable_id: int):
    pilots = session.query(Pilot).join(Stable).filter(Stable.id == stable_id).all()
    if not pilots:
        raise HTTPException(status_code=404, detail="Stable not found or no pilots in stable")
    return pilots