from __future__ import annotations

from app.db.connection import get_db


async def get_or_create_user(db_path: str, user_id: int) -> None:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, 0)", (user_id,)
            )
            await db.commit()


async def get_balance(db_path: str, user_id: int) -> int:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT balance FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if row is None:
            return 0
        return int(row["balance"])


async def add_balance(db_path: str, user_id: int, amount: int) -> None:
    async with get_db(db_path) as db:
        await db.execute(
            "INSERT INTO users (user_id, balance) VALUES (?, 0) ON CONFLICT(user_id) DO NOTHING",
            (user_id,),
        )
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id),
        )
        await db.commit()


async def list_user_ids(db_path: str) -> list[int]:
    async with get_db(db_path) as db:
        cur = await db.execute("SELECT user_id FROM users")
        rows = await cur.fetchall()
        return [int(row["user_id"]) for row in rows]


async def deduct_balance(db_path: str, user_id: int, amount: int) -> bool:
    if amount <= 0:
        return True
    async with get_db(db_path) as db:
        await db.execute(
            "INSERT INTO users (user_id, balance) VALUES (?, 0) ON CONFLICT(user_id) DO NOTHING",
            (user_id,),
        )
        cur = await db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ? AND balance >= ?",
            (amount, user_id, amount),
        )
        await db.commit()
        return cur.rowcount > 0
