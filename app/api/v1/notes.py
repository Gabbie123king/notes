# app/api/v1/notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate

router = APIRouter()

@router.post("/", response_model=NoteRead)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    db_note = Note(**note.dict())
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/", response_model=list[NoteRead])
def get_notes(session: Session = Depends(get_session)):
    return session.exec(select(Note)).all()


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, updated: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if updated.title is not None:
        note.title = updated.title
    if updated.content is not None:
        note.content = updated.content

    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()
    return {"ok": True}