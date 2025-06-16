from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app import models, schemas
from app.db import get_db
from sentence_transformers import SentenceTransformer
import pickle

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/notes/")
async def post_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = models.Note(
        title=note.title,
        content=note.content
    )

    embed = model.encode(note.content).tolist()
    
    new_note.embedding = embed

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content
    }

@app.post("/notes/{id}")
async def post_note_by_id(note: schemas.NoteCreateByID, db: AsyncSession=Depends(get_db)):
    new_note = models.Note(
        title=note.title,
        content=note.content,
        id=note.id
    )
    embed = model.encode(note.content).tolist()
    
    new_note.embedding = embed

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content
    }

@app.get("/notes/")
async def get_all_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note))
    notes = result.scalars().all()
    return [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content
            # omit embedding
        }
        for note in notes
    ]

@app.get("/notes/{id}")
async def get_note_by_id(id:int, db: AsyncSession = Depends(get_db)):
    note = await db.execute(select(models.Note).filter(models.Note.id == id))
    note = note.scalar_one_or_none()
    return {
        "id":note.id,
        "title":note.title,
        "content":note.content
    }

@app.put("/notes/{id}")
async def update_note_by_id(id: int, note:schemas.NoteUpdateByID, db: AsyncSession = Depends(get_db)):
    note_old = await db.execute(select(models.Note).filter(models.Note.id == id))
    note_old = note_old.scalar_one_or_none()

    if note.content:
        note_old.content = note.content
    if note.title:
        note_old.title = note.title
    
    await db.commit()
    await db.refresh(note_old)
    return {
        "id":note_old.id,
        "title":note_old.title,
        "content":note_old.content
    }
        
@app.delete("/notes/all")
async def delete_all_notes(db: AsyncSession = Depends(get_db)):
    stmt = delete(models.Note)
    await db.execute(stmt)
    await db.commit()
    return

@app.delete("/notes/{id}")
async def delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(models.Note).where(models.Note.id == id)
    await db.execute(stmt)
    await db.commit()
    return