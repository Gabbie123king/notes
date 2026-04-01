# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.notes import router as notes_router
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(notes_router, prefix="/api/v1/notes", tags=["Notes"])


@app.get("/")
def root():
    return {"message": "Notes API is running"}
