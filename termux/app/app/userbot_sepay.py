# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient, events
from aiogram import Bot

from app.config import load_config
from app.db.topups import get_topup_by_note, list_pending_topups, set_topup_status
from app.db.users import add_balance
from app.utils.text import topup_approved_text


NOTE_PATTERN = re.compile(r"(NAP\d+-\d+-\d+)")


def _extract_note(text: str) -> str:
    match = NOTE_PATTERN.search(text)
    if match:
        return match.group(1)
    fallback = re.search(r"(NAP\d+)", text)
    if fallback:
        return fallback.group(1)
    return ""


def _normalize_note(raw: str) -> str:
    digits = "".join(ch for ch in raw if ch.isdigit())
    return f"NAP{digits}" if digits else ""


async def _resolve_topup(db_path: str, note: str) -> dict | None:
    topup = await get_topup_by_note(db_path, note)
    if topup:
        return topup
    normalized = _normalize_note(note)
    if not normalized:
        return None
    for pending in await list_pending_topups(db_path):
        if _normalize_note(str(pending.get("note", ""))) == normalized:
            return pending
    return None


async def main() -> None:
    load_dotenv()
    config = load_config()
    api_id = int(os.getenv("TELEGRAM_API_ID", "0").strip() or "0")
    api_hash = os.getenv("TELEGRAM_API_HASH", "").strip()
    session_name = os.getenv("TELEGRAM_SESSION", "sepay_userbot").strip() or "sepay_userbot"
    if not api_id or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID and TELEGRAM_API_HASH are required for userbot")

    if not config.sepay_group_id:
        raise RuntimeError("SEPAY_GROUP_ID is required for userbot")

    bot = Bot(token=config.bot_token)
    client = TelegramClient(session_name, api_id, api_hash)

    @client.on(events.NewMessage(chats=config.sepay_group_id))
    async def handler(event) -> None:
        text = event.raw_text or ""
        if not text:
            return
        note = _extract_note(text)
        if not note:
            return
        topup = await _resolve_topup(config.db_path, note)
        if not topup or topup.get("status") != "pending":
            return
        await add_balance(config.db_path, int(topup["user_id"]), int(topup["amount"]))
        await set_topup_status(config.db_path, int(topup["id"]), "approved")
        await bot.send_message(int(topup["user_id"]), topup_approved_text(topup["note"]), parse_mode="HTML")

    await client.start()
    print("[userbot] running, listening for SePay messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
