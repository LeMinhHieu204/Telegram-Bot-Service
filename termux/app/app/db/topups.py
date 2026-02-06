from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from app.db.connection import get_db


async def create_topup(db_path: str, user_id: int, amount: int, note: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    async with get_db(db_path) as db:
        cur = await db.execute(
            "INSERT INTO topups (user_id, amount, note, status, created_at) VALUES (?, ?, ?, 'pending', ?)",
            (user_id, amount, note, created_at),
        )
        await db.commit()
        return int(cur.lastrowid)


async def get_topup(db_path: str, topup_id: int) -> Optional[dict]:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT id, user_id, amount, note, status, created_at FROM topups WHERE id = ?",
            (topup_id,),
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return dict(row)

async def get_topup_by_note(db_path: str, note: str) -> Optional[dict]:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT id, user_id, amount, note, status, created_at FROM topups WHERE note = ?",
            (note,),
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return dict(row)


async def set_topup_status(db_path: str, topup_id: int, status: str) -> None:
    async with get_db(db_path) as db:
        await db.execute(
            "UPDATE topups SET status = ? WHERE id = ?",
            (status, topup_id),
        )
        await db.commit()


async def list_pending_topups(db_path: str) -> list[dict]:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT id, user_id, amount, note, status, created_at FROM topups WHERE status = 'pending'"
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def record_sepay_webhook(db_path: str, sepay_id: int, reference_code: str | None, note: str) -> bool:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT sepay_id FROM sepay_webhooks WHERE sepay_id = ?",
            (sepay_id,),
        )
        row = await cur.fetchone()
        if row is not None:
            return False
        await db.execute(
            "INSERT INTO sepay_webhooks (sepay_id, reference_code, note, received_at) VALUES (?, ?, ?, ?)",
            (sepay_id, reference_code or "", note, datetime.now(timezone.utc).isoformat()),
        )
        await db.commit()
        return True
