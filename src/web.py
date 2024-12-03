from fastapi import FastAPI

app = FastAPI()

DEFAULT_PATH = "/api/v1"

from src.api.stables import *