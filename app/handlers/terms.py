# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.common import back_home_keyboard
from app.utils.text import terms_text

router = Router()


@router.callback_query(lambda c: c.data == "terms:show")
async def terms_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(terms_text(), reply_markup=back_home_keyboard(), parse_mode="HTML")
