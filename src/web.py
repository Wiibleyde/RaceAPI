from fastapi import FastAPI

app = FastAPI()

DEFAULT_PATH = "/api/v1"

@app.get("/", description="default route", include_in_schema=False, status_code=200)
async def get_default_route():
    return "OK"

from src.api.stables import *
from src.api.pilots import *
from src.api.races import *
from src.api.raceLeaderboards import *
from src.api.raceEvents import *