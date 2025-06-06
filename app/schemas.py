from pydantic import BaseModel
from typing import List, Optional


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteGet(BaseModel):
     id: int
     title: str
     content: str
     embedding: list
     created: str