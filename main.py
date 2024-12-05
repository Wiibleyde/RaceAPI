from src.database.models import init_db, init_test_data
from src.web import app

if __name__ == "__main__":
    init_db()
    init_test_data() # Only for testing purposes
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)