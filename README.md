# RaceAPI

## Summary

This project is a simple API that allows you to manage a race with runners, their times, events, stables, circuits.

## Table of contents

- [RaceAPI](#raceapi)
  - [Summary](#summary)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [Tests](#tests)
  - [Endpoints](#endpoints)
  - [Database](#database)

## Setup

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Generate an API key for the authentication
4. Create a .env file at the root of the repository with the following content :
    ```
    API_KEY=<your_generated_api_key>
    ```
5. Run `python main.py`

## Tests

Run `python tests.py` to run the tests, **be sure to start the API server before**.

**Note:** The tests need to be run in an empty database.


## Endpoints

Go on `http://localhost:8000/docs` to see the API documentation.

## Database

The database is a SQLite database, you can find it at the root of the repository under the name `database.db`.

