from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text
from app import models, schemas
from app.db import get_db
from sentence_transformers import SentenceTransformer

description = """ The Notes Manager API helps you keep all your notes in one place, 
easily access them, and utilize search functions for checking similarity or gathering related notes.

## Notes

You are able to:
* **Post a note**
* **Update a note**
* **Search for similar text in all notes**
* **Delete a note**

"""

tags_metadata = [
    {"name": "Notes", "description": "Ways to interact with the notes themselves"},
    {"name":"Status", "description": "Handy call to see if the API service is running."}
]

app = FastAPI(
    title="Notes Manager API",
    description=description,
    summary="All of your thoughts at the click of a button",
    version="0.0.1",
    contact={"name": "Brandon Bilinski", "url": "https://github.com/brandonbilinski"},
    openai_tags=tags_metadata,
)

model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/")
async def root():
    return {"message": "Running"}


@app.post("/notes", tags=["notes"])
async def post_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = models.Note(title=note.title, content=note.content)

    embed = model.encode(note.content).tolist()

    new_note.embedding = embed

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "content": new_note.content}


@app.get("/notes", tags=["notes"])
async def get_all_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note))
    notes = result.scalars().all()
    return [
        {"id": note.id, "title": note.title, "content": note.content} for note in notes
    ]


@app.get("/notes/{id}", tags=["notes"])
async def get_note_by_id(id: int, db: AsyncSession = Depends(get_db)):
    note = await db.execute(select(models.Note).filter(models.Note.id == id))
    note = note.scalar_one_or_none()
    return {"id": note.id, "title": note.title, "content": note.content}


@app.get("/search", tags=["notes"])
async def get_by_search_query(q: str, db: AsyncSession = Depends(get_db)):
    query_embed = model.encode(q).tolist()
    query_embed = "[" + ",".join(map(str, query_embed)) + "]"

    query = text(
        """
SELECT id, title, content,
       1 - (embedding <#> CAST(:query_embed as vector)) AS similarity
FROM notes
ORDER BY embedding <#> CAST(:query_embed as vector)
LIMIT 5;
"""
    )

    similar = await db.execute(query, {"query_embed": query_embed})
    rows = similar.fetchall()
    return [
        {"id": note.id, "title": note.title, "content": note.content} for note in rows
    ]


@app.put("/notes/{id}", tags=["notes"])
async def update_note_by_id(
    id: int, note: schemas.NoteUpdateByID, db: AsyncSession = Depends(get_db)
):
    note_old = await db.execute(select(models.Note).filter(models.Note.id == id))
    note_old = note_old.scalar_one_or_none()

    if note.content:
        note_old.content = note.content
    if note.title:
        note_old.title = note.title

    await db.commit()
    await db.refresh(note_old)
    return {"id": note_old.id, "title": note_old.title, "content": note_old.content}


@app.delete("/notes/{id}", tags=["notes"])
async def delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(models.Note).where(models.Note.id == id)
    await db.execute(stmt)
    await db.commit()
    return
