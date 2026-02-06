from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import aiosqlite


@asynccontextmanager
async def get_db(db_path: str) -> AsyncIterator[aiosqlite.Connection]:
    conn = await aiosqlite.connect(db_path)
    conn.row_factory = aiosqlite.Row
    try:
        yield conn
    finally:
        await conn.close()
