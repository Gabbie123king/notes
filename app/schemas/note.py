# app/schemas/note.py
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional

class NoteCreate(SQLModel):
    title: str
    content: str

class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None