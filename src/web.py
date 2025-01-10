from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv, find_dotenv
import os


app = FastAPI()

DEFAULT_PATH = "/api/v1"
# dotenv_file_path = "./.env"
dotenv_file_path = os.path.join(os.path.dirname(__file__), "..", ".env")
print(dotenv_file_path)

if not os.path.exists(dotenv_file_path):
    print(".env file not found, please refer to the README.md")
    exit(1)

load_dotenv(dotenv_path=dotenv_file_path)
# load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")
print(API_KEY)
if API_KEY is None:
    print("API key not found, please refer to the README.md to setup one")
    exit(1)

auth_scheme = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    # Verifies the request has a Bearer Token header and if the token provided is valid
    if credentials.scheme != "Bearer" or credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing token")


# Applies authentication on all routes
app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/", description="default route", include_in_schema=False, status_code=200)
async def get_default_route():
    return {"message": "Welcome to the API", "path": DEFAULT_PATH, "docs": "/docs"}


@app.get(
    f"{DEFAULT_PATH}/", description="default route", tags=["Default"], status_code=200
)
async def get_default_route():
    return {"message": "Welcome to the API", "path": DEFAULT_PATH, "docs": "/docs"}


from src.api.stables import *
from src.api.pilots import *
from src.api.races import *
from src.api.raceLeaderboards import *
from src.api.raceEvents import *
from src.api.engine import *
