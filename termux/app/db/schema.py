from __future__ import annotations

from app.db.connection import get_db


async def init_db(db_path: str) -> None:
    async with get_db(db_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER NOT NULL DEFAULT 0,
                username TEXT
            )
            """
        )
        try:
            await db.execute("ALTER TABLE users ADD COLUMN username TEXT")
        except Exception:
            # Column already exists on upgraded databases.
            pass
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS topups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                note TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sepay_webhooks (
                sepay_id INTEGER PRIMARY KEY,
                reference_code TEXT,
                note TEXT NOT NULL,
                received_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sepay_polling_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        await db.commit()
