# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_APPROVE, ICON_REJECT


def topup_admin_keyboard(topup_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_APPROVE} Duyệt", callback_data=f"admin:approve:{topup_id}")
    kb.button(text=f"{ICON_REJECT} Từ chối", callback_data=f"admin:reject:{topup_id}")
    kb.adjust(2)
    return kb.as_markup()
