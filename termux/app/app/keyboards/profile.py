# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_SERVICES, ICON_BACK


def profile_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_SERVICES} Dịch vụ", callback_data="services:list")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    kb.adjust(1, 1)
    return kb.as_markup()
