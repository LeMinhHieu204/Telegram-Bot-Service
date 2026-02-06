# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_BACK


def back_home_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    return kb.as_markup()
