from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(
    title="Fitness Intelligence Platform API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running"
    }

@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }