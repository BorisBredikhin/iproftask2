from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def post_notes(db: Session, note: schemas.Note):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session):
    return db.query(models.Note).all()


def get_note(db: Session, id: int) -> models.Note:
    return db.query(models.Note).filter(models.Note.id == id).first()


def del_note(db: Session, id: int) -> bool:
    db.delete(db.query(models.Note).filter(models.Note.id == id).first())
    db.flush()
    return True


def query_note(db: Session, query: str) -> List[models.Note]:
    return db.query(models.Note).filter(query in models.Note.content or query in models.Note.title).all()


def edit_note(db: Session, note_id: int, note: schemas.EditNote):
    db_note: models.Note = db.query(models.Note).filter(models.Note.id == note_id).first()
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note
