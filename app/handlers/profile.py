# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.config import Config
from app.db.users import get_balance, get_or_create_user
from app.keyboards.profile import profile_keyboard
from app.utils.text import profile_text

router = Router()


async def _edit_or_send(callback: CallbackQuery, text: str, reply_markup=None) -> None:
    msg = callback.message
    if msg is None:
        return
    if msg.text:
        await msg.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        return
    if msg.caption is not None:
        await msg.edit_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")
        return
    await msg.answer(text, reply_markup=reply_markup, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "profile:show")
async def profile_callback(callback: CallbackQuery, config: Config) -> None:
    user = callback.from_user
    if user is None:
        return
    await get_or_create_user(config.db_path, user.id)
    balance = await get_balance(config.db_path, user.id)
    name = user.full_name or "Unknown"
    await _edit_or_send(callback, profile_text(user.id, name, balance), reply_markup=profile_keyboard())
