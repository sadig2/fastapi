import logging
import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import db


log = logging.getLogger(__name__)
router = APIRouter()


class Reader(BaseModel):
    name: str


@router.post("/v1/readers")
async def add_reader(reader: Reader):
    try:
        reader_id = (await db.connection.execute_insert(
            """
            INSERT INTO readers
                (name)
            VALUES (?)
            """,
            (reader.name,),
        ))[0]
        await db.connection.commit()
        log.debug(f"Reader added {reader.name}")
    except sqlite3.IntegrityError:
        return HTTPException(status_code=400, detail="Item name already exists")
    return {"reader_id": reader_id}


@router.get("/v1/readers")
async def get_readers():
    async with db.connection.execute(
        """
        SELECT
            id,
            name
        FROM
            readers
        """
    ) as cursor:
        rows = await cursor.fetchall()

    return {"readers": [{"id": item[0], "name": item[1]} for item in rows]}
