import logging
from datetime import datetime
from typing import Optional
from src.validators.borrow_valid import book_exists, reader_exists,\
    borrowed_by_same, borrowed_by_other


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import db


log = logging.getLogger(__name__)
router = APIRouter()


class Borrow(BaseModel):
    reader_id: int
    book_id: int
    
  
@router.post("/v1/borrows")
async def add_borrow(borrow: Borrow):
    if await borrowed_by_same(borrow.reader_id, borrow.book_id):
        raise HTTPException(status_code=200, detail="Book is borrowed by you")
    
    if await borrowed_by_other(borrow.book_id):
        raise HTTPException(status_code=409, detail="Book is borrowed by someone")
    # Check if reader_id exists
    if not await reader_exists(borrow.reader_id):
        raise HTTPException(status_code=404, detail="Reader with such an id doesn't exist")

    # Check if book_id exists
    if not await book_exists(borrow.book_id):
        raise HTTPException(status_code=404, detail="Book with such an id doesn't exist")
    
    await db.connection.execute(
        """
        INSERT INTO borrows
            (reader_id, book_id, borrow_time, return_time)
        VALUES
            (?, ?, DATE('now'), NULL)
        """,
        (borrow.reader_id, borrow.book_id),
    )
    await db.connection.commit()
    log.debug(f"New borrow from reader id {borrow.reader_id}")


@router.delete("/v1/borrows/{book_id}")
async def del_borrow(book_id: int):
    await db.connection.execute(
        """
        UPDATE
            borrows
        SET
            return_time = DATE('now')
        WHERE
            book_id = ?
            AND return_time IS NULL;
        """,
        (book_id,),
    )
    log.debug(f"Book {book_id} returned.")
    await db.connection.commit()


@router.get("/v1/borrows")
async def get_borrows():
    async with db.connection.execute(
        """
        SELECT
            readers.name,
            books.title,
            authors.name,
            borrows.borrow_time
        FROM
            borrows
        LEFT JOIN
            books ON books.id = borrows.book_id
        LEFT JOIN
            authors ON authors.id = books.author_id
        LEFT JOIN
            readers ON readers.id = borrows.reader_id
        WHERE
            borrows.return_time IS NULL
        """
    ) as cursor:
        rows = await cursor.fetchall()

    return {
        "borrows": [{"reader": item[0], "title": item[1], "author": item[2], "borrow_time": item[3]} for item in rows]
    }
