from fastapi import FastAPI

app = FastAPI()

DEFAULT_PATH = "/api/v1"

from src.api.stables import *
from src.api.pilots import *
from src.api.races import *
from src.api.raceLeaderboards import *
from src.api.raceEvents import *