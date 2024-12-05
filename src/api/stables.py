from ..web import app, DEFAULT_PATH
from ..database.models import session, Stable, Pilot

@app.get(f"{DEFAULT_PATH}/stables", description="Get all stables", tags=["Stables"])
async def get_stables():
    stables = session.query(Stable).all()
    return stables

@app.get(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Get a stable by ID", tags=["Stables"])
async def get_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    return stable

@app.post(f"{DEFAULT_PATH}/stables", description="Create a new stable", tags=["Stables"])
async def create_stable(name: str):
    stable = Stable(name=name)
    session.add(stable)
    session.commit()
    return stable

@app.put(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Update a stable by ID", tags=["Stables"])
async def update_stable(stable_id: int, name: str):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable not found"}, 404
    stable.name = name
    session.commit()
    return stable

@app.delete(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Delete a stable by ID", tags=["Stables"])
async def delete_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable not found"}, 404
    session.delete(stable)
    session.commit()
    return stable

@app.get(f"{DEFAULT_PATH}/stables/{{stable_id}}/pilots", description="Get all pilots from a stable", tags=["Stables"])
async def get_pilots_from_stable(stable_id: int):
    pilots = session.query(Pilot).join(Stable).filter(Stable.id == stable_id).all()
    if not pilots:
        return {"error": "Stable not found or no pilots in stable"}, 404
    return pilots