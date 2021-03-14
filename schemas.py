from typing import Optional

from pydantic import BaseModel

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str

class Note(NoteBase):
    id: int

class EditNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
