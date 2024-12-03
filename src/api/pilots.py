from ..web import app, DEFAULT_PATH
from ..database.models import session, Stable, Pilot


@app.get(f"{DEFAULT_PATH}/pilots", description="Get all pilots")
async def get_pilots():
    pilots = session.query(Pilot).all()
    return pilots


@app.get(f"{DEFAULT_PATH}/pilots/{{pilot_id}}", description="Get a pilot by ID")
async def get_pilot(pilot_id: int):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    return pilot


@app.post(f"{DEFAULT_PATH}/pilots", description="Create a new pilot")
async def create_pilot(firstname: str, lastname: str, stable_id: int, nationality: str):
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable not found with the provided id"}, 404
    pilot = Pilot(
        firstname=firstname,
        lastname=lastname,
        stable_id=stable_id,
        nationality=nationality,
    )
    session.add(pilot)
    session.commit()
    return pilot


@app.put(f"{DEFAULT_PATH}/pilots/{{pilot_id}}", description="Update a pilot by ID")
async def update_pilot(pilot_id: int, firstname: str, lastname: str, stable_id: int, nationality: str):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        return {"error": "Pilot not found"}, 404
    
    stable = session.query(Stable).filter_by(id=stable_id).first()
    if stable is None:
        return {"error": "Stable id provided does not match any existing stable"}, 404
    
    pilot.firstname = firstname
    pilot.lastname = lastname
    pilot.stable_id = stable_id
    pilot.nationality = nationality
    session.commit()
    return pilot


@app.delete(f"{DEFAULT_PATH}/pilots/{{pilot_id}}", description="Delete a pilot by ID")
async def delete_pilot(pilot_id: int):
    pilot = session.query(Pilot).filter_by(id=pilot_id).first()
    if pilot is None:
        return {"error": "Pilot not found"}, 404
    session.delete(pilot)
    session.commit()
    return pilot
