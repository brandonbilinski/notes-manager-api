from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384))
    created = Column(TIMESTAMP(timezone=True), server_default=func.now())