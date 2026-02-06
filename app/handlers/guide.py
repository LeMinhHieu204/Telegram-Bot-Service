# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.common import back_home_keyboard
from app.utils.text import guide_text

router = Router()


@router.callback_query(lambda c: c.data == "guide:show")
async def guide_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(guide_text(), reply_markup=back_home_keyboard(), parse_mode="HTML")
