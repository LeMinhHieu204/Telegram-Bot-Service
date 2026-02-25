from __future__ import annotations

from app.db.connection import get_db


def _normalize_username(username: str | None) -> str | None:
    if username is None:
        return None
    cleaned = username.strip().lstrip("@").lower()
    return cleaned or None


async def get_or_create_user(db_path: str, user_id: int, username: str | None = None) -> None:
    normalized_username = _normalize_username(username)
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT user_id, username FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO users (user_id, balance, username) VALUES (?, 0, ?)",
                (user_id, normalized_username),
            )
        elif normalized_username and row["username"] != normalized_username:
            await db.execute(
                "UPDATE users SET username = ? WHERE user_id = ?",
                (normalized_username, user_id),
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


async def get_user_id_by_username(db_path: str, username: str) -> int | None:
    normalized_username = _normalize_username(username)
    if not normalized_username:
        return None
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT user_id FROM users WHERE lower(username) = ?",
            (normalized_username,),
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return int(row["user_id"])


async def get_user_wallet(db_path: str, user_id: int) -> dict | None:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT user_id, username, balance FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return {
            "user_id": int(row["user_id"]),
            "username": row["username"],
            "balance": int(row["balance"]),
        }


async def list_user_ids(db_path: str) -> list[int]:
    async with get_db(db_path) as db:
        cur = await db.execute("SELECT user_id FROM users")
        rows = await cur.fetchall()
        return [int(row["user_id"]) for row in rows]


async def list_users_brief(db_path: str) -> list[dict]:
    async with get_db(db_path) as db:
        cur = await db.execute(
            "SELECT user_id, username FROM users ORDER BY user_id DESC"
        )
        rows = await cur.fetchall()
        return [
            {
                "user_id": int(row["user_id"]),
                "username": row["username"] or "",
            }
            for row in rows
        ]


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
