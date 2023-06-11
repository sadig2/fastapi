import asyncio
import logging
from fastapi import FastAPI
from uvicorn import Config, Server
import aiosqlite

app = FastAPI()

class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await aiosqlite.connect("database.db")
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        await self.connection.commit()

    async def close(self):
        await self.connection.close()

db = Database()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/authors")
async def get_authors():
    async with db.connection.execute("SELECT * FROM author") as cursor:
        authors = await cursor.fetchall()
        return {"authors": authors}

@app.post("/authors")
async def create_author(author: dict):
    async with db.connection.execute("INSERT INTO author (name) VALUES (?)", (author["name"],)) as cursor:
        author_id = cursor.lastrowid
        await db.connection.commit()
        return {"author_id": author_id}

@app.put("/authors/{author_id}")
async def update_author(author_id: int, author: dict):
    async with db.connection.execute("UPDATE author SET name=? WHERE id=?", (author["name"], author_id)) as cursor:
        await db.connection.commit()
        return {"message": "Author updated"}

@app.delete("/authors/{author_id}")
async def delete_author(author_id: int):
    async with db.connection.execute("DELETE FROM author WHERE id=?", (author_id,)) as cursor:
        await db.connection.commit()
        return {"message": "Author deleted"}

async def run():
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)
    server = Server(config)

    try:
        await server.serve()
    finally:
        await shutdown()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
