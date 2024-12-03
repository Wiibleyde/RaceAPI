from ..web import app, DEFAULT_PATH
from ..database.models import session, Stable

@app.get(f"{DEFAULT_PATH}/stables", description="Get all stables")
async def get_stables():
    stables = session.query(Stable).all()
    return stables

@app.get(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Get a stable by ID")
async def get_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    return stable

@app.post(f"{DEFAULT_PATH}/stables", description="Create a new stable")
async def create_stable(name: str):
    stable = Stable(name=name)
    session.add(stable)
    session.commit()
    return stable

@app.put(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Update a stable by ID")
async def update_stable(stable_id: int, name: str):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable not found"}, 404
    stable.name = name
    session.commit()
    return stable

@app.delete(f"{DEFAULT_PATH}/stables/{{stable_id}}", description="Delete a stable by ID")
async def delete_stable(stable_id: int):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable not found"}, 404
    session.delete(stable)
    session.commit()
    return stable
