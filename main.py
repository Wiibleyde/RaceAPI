from src.database.models import init_db
from src.web import app

# Insert data
# redbull = Stable(name="Red Bull")
# session.add_all([redbull])
# session.commit()

# Query data (with filter)
# stmt = session.query(Stable).filter_by(name="Red Bull")

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)