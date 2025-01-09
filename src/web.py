from fastapi import FastAPI

app = FastAPI()

DEFAULT_PATH = "/api/v1"

@app.get("/", description="default route", include_in_schema=False, status_code=200)
async def get_default_route():
    return {"message": "Welcome to the API", "path": DEFAULT_PATH, "docs": "/docs"}

@app.get(f"{DEFAULT_PATH}/", description="default route", tags=["Default"], status_code=200)
async def get_default_route():
    return {"message": "Welcome to the API", "path": DEFAULT_PATH, "docs": "/docs"}

from src.api.stables import *
from src.api.pilots import *
from src.api.races import *
from src.api.raceLeaderboards import *
from src.api.raceEvents import *
from src.api.engine import *