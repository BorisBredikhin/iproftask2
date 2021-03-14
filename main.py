from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

N=12

try:
    with open("config.txt") as f:
        N=int(f.readline())
except:
    pass

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notes", response_model=schemas.Note)
def post_notes(note: schemas.NoteBase, db: Session = Depends(get_db)):
    db_note = crud.post_notes(db, models.Note(title=note.title, content=note.content))
    return crud.post_notes(db, db_note)

@app.get("/notes/{note_id}", response_model=List[schemas.Note])
def get_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)

@app.get("/notes/{note_id}", response_model=schemas.Note)
def get_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db, note_id)
    if db_note.title == None:
        db_note.title = db_note.content[:min(len(db_note.content, N))]
    return db_note


@app.put("/notes/{note_id}", response_model=schemas.Note)
def put_note(note_id: int, note: schemas.EditNote, db: Session = Depends(get_db)):
    db_note = crud.edit_note(db, note_id, note)
    return db_note

@app.get("/notes/{note_id}", response_model=List[schemas.Note])
def query(q: str, db: Session = Depends(get_db)):
    return crud.query_note(db, q)

@app.delete("/notes/{note_id}", response_model=schemas.Note)
def delete(id: int, db: Session = Depends(get_db)):
    return crud.del_note(db, id)
