from pydantic import BaseModel
from typing import List, Optional


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteCreateByID(NoteCreate):
    id: int


class NoteUpdateByID(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
