from __future__ import annotations

from app.db.connection import get_db


async def get_state(db_path: str, key: str) -> str | None:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT value FROM sepay_polling_state WHERE key = ?",
            (key,),
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return str(row["value"])


async def set_state(db_path: str, key: str, value: str) -> None:
    async with get_db(db_path) as db:
        await db.execute(
            "INSERT INTO sepay_polling_state (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        await db.commit()
