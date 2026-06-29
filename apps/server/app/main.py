from fastapi import FastAPI
from sqlalchemy import text
from app.core.security import hash_password
from app.db.session import engine
from app.modules.auth.api import router as auth_router


app = FastAPI(
    title="Fitness Intelligence Platform API",
    version="1.0.0"
)
app.include_router(auth_router)


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
@app.get("/test/hash")
def test_hash():
    return {
        "password": hash_password("password123")
    }
