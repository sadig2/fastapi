from src import db


async def borrowed_by_other(book_id: int):
    async with db.connection.execute(
        """
        SELECT * FROM borrows as b
        WHERE b.book_id = ?
        """, (book_id)
    ) as cursor:
        rows = await cursor.fetchall()
        return rows


async def borrowed_by_same(reader_id: int, book_id: int):
    async with db.connection.execute(
        """
        SELECT * FROM borrows as b
        WHERE b.reader_id = ? AND b.book_id = ?
        """, (reader_id, book_id)
    ) as cursor:
        rows = await cursor.fetchall()
        return rows


async def reader_exists(id: int):
    async with db.connection.execute(
        """
        SELECT * FROM readers where readers.id = ?
        """, (id,)
    ) as cursor:
        rows = await cursor.fetchall()
    if len(rows) == 1:
        return True
    return False


async def book_exists(id: int):
    async with db.connection.execute(
        """
        SELECT * FROM books where books.id = ?
        """, (id,)
    ) as cursor:
        rows = await cursor.fetchall()
    if len(rows) == 1:
        return True
    return False
