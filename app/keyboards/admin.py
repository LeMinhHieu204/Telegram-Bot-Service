# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_APPROVE, ICON_REJECT, ICON_TOPUP


def topup_admin_keyboard(topup_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_APPROVE} Duyệt", callback_data=f"admin:approve:{topup_id}")
    kb.button(text=f"{ICON_REJECT} Từ chối", callback_data=f"admin:reject:{topup_id}")
    kb.adjust(2)
    return kb.as_markup()


def manual_topup_start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_TOPUP} Nạp tiền thủ công", callback_data="admin:manual_topup:start")
    kb.adjust(1)
    return kb.as_markup()


def manual_topup_confirm_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_APPROVE} Xác nhận nạp", callback_data="admin:manual_topup:confirm")
    kb.button(text=f"{ICON_REJECT} Hủy", callback_data="admin:manual_topup:cancel")
    kb.adjust(2)
    return kb.as_markup()
