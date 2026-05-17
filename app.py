from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
import os
from dotenv import load_dotenv

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://parser:secret@localhost:5432/quotes_db"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    author = Column(String)
    tags = Column(String)

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Привет, мир!"}

@app.get("/quotes/count")
def quotes_count():
    session = Session(engine)
    count = session.query(Quote).count()
    session.close()
    return {"count": count}

@app.post("/quotes/cleanup")
def cleanup_duplicates():
    session = Session(engine)
    from sqlalchemy import text
    session.execute(text("""
        DELETE FROM quotes
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM quotes
            GROUP BY text, author
        )
    """))
    session.commit()
    count = session.query(Quote).count()
    session.close()
    return {"message": "Дубликаты удалены", "count": count}