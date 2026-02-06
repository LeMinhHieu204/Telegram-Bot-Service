# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.common import back_home_keyboard
from app.utils.text import terms_text

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


@router.callback_query(lambda c: c.data == "terms:show")
async def terms_callback(callback: CallbackQuery) -> None:
    await _edit_or_send(callback, terms_text(), reply_markup=back_home_keyboard())
