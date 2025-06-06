from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas
from app.db import get_db

app = FastAPI()

@app.get("/")
async def read_root():
    return{"Hello":"World"}

@app.post("/notes/")
async def post_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = models.Note(
        title=note.title,
        content=note.content
    )
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

@app.get("/notes/")
async def get_all_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note))
    return result.scalars().all()

@app.get("notes/{id}")
async def get_note_by_id(id, db: AsyncSession = Depends(get_db)):
    query = "select * from notes_db.Note where id = {id}".format(id)
    note = db.execute(query)
    return note