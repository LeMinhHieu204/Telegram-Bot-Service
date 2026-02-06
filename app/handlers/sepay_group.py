# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from aiogram import Router
from aiogram.types import Message

from app.config import Config
from app.db.users import list_user_ids


router = Router()
@router.message()
async def sepay_group_message(message: Message, config: Config) -> None:
    if not config.sepay_group_id:
        return
    if message.chat is None or message.chat.id != config.sepay_group_id:
        return
    await _broadcast_group_message(message, config)
    try:
        sender = message.from_user.username if message.from_user else "unknown"
        print(f"[sepay_group] msg from {sender} in {message.chat.id}")
    except Exception:
        pass
    text = message.text or message.caption or ""
    if not text:
        return
    try:
        print(f"[sepay_group] text: {text}")
    except Exception:
        pass


async def _broadcast_group_message(message: Message, config: Config) -> None:
    try:
        user_ids = await list_user_ids(config.db_path)
    except Exception as exc:
        try:
            print(f"[broadcast] failed to load users: {exc}")
        except Exception:
            pass
        return
    if not user_ids:
        return
    for user_id in user_ids:
        try:
            await message.bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
        except Exception as exc:
            try:
                print(f"[broadcast] copy_message to {user_id} failed: {exc}")
            except Exception:
                pass
