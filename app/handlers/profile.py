# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.config import Config
from app.db.users import get_balance, get_or_create_user
from app.keyboards.profile import profile_keyboard
from app.utils.text import profile_text

router = Router()


@router.callback_query(lambda c: c.data == "profile:show")
async def profile_callback(callback: CallbackQuery, config: Config) -> None:
    user = callback.from_user
    if user is None:
        return
    await get_or_create_user(config.db_path, user.id)
    balance = await get_balance(config.db_path, user.id)
    name = user.full_name or "Unknown"
    await callback.message.edit_text(
        profile_text(user.id, name, balance),
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )
