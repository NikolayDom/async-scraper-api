import asyncio
import httpx
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

BASE_URL = "https://quotes.toscrape.com/api/quotes?page={}"

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    author = Column(String)
    tags = Column(String)

# Подключение к PostgreSQL в контейнере db
engine = create_engine("postgresql://parser:secret@db:5432/quotes_db")
Base.metadata.create_all(engine)

async def fetch_page(client, page):
    url = BASE_URL.format(page)
    headers = {"User-Agent": "Mozilla/5.0 ..."}
    try:
        response = await client.get(url, headers=headers, timeout=10)
        data = response.json()
        
        quotes = []
        for item in data["quotes"]:  # data["quotes"] — это СПИСОК словарей
            quotes.append({
                "text": item.get("text", ""),
                "author": item.get("author", {}).get("name", "Unknown") if isinstance(item.get("author"), dict) else item.get("author", "Unknown"),
                "tags": ", ".join(item.get("tags", [])) if isinstance(item.get("tags"), list) else item.get("tags", "")
            })
        return quotes
    except Exception as e:
        print(f"Ошибка на странице {page}: {e}")
        return []

async def fetch_all():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, page) for page in range(1, 11)]
        results = await asyncio.gather(*tasks)
        all_quotes = sum(results, [])
        session = Session(engine)
        for quote in all_quotes:
            q = Quote(
                text=quote["text"],
                author=quote["author"],
                tags=quote["tags"]   # уже строка, не список
            )
            session.add(q)

        session.commit()
        
        count = session.query(Quote).count()
        print(f"Сохранено: {count}")
        session.close()

asyncio.run(fetch_all())