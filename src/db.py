import logging
import os

import aiosqlite


log = logging.getLogger(__name__)
connection = None


async def initialize():
    global connection

    log.debug("Initializing database...")
    connection = await aiosqlite.connect(f"{os.getcwd()}/data/app.db")
    
    # Check if tables exist before creating them
    cursor = await connection.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table' AND name IN ('authors', 'books', 'readers', 'borrows')
        """
    )
    existing_tables = await cursor.fetchall()
    if len(existing_tables) != 4:
        await connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                author_id INTEGER NOT NULL,
                title TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS borrows (
                id INTEGER PRIMARY KEY,
                reader_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_time TEXT NOT NULL,
                return_time TEXT
            );
            """
        )

    log.debug("Database ready.")
