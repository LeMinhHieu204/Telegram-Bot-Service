# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import (
    ICON_MEM, ICON_GUIDE, ICON_TOPUP, ICON_TERMS, 
    ICON_PROFILE, ICON_SERVICES, ICON_INFO
)


def home_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # Emphasize primary actions with extra padding and dedicated rows.
    kb.button(text=f"  {ICON_MEM}  Kéo mem  ", callback_data="pull:list")
    kb.button(text="  📺  Telegram View  ", callback_data="tv:list")
    kb.button(text=f"{ICON_GUIDE} Hướng Dẫn", callback_data="guide:show")
    kb.button(text=f"{ICON_INFO} Nhận làm bot", callback_data="bot:hire")
    kb.button(text=f"{ICON_TOPUP} Nạp Tiền", callback_data="topup:info")
    kb.button(text=f"{ICON_TERMS} Điều khoản", callback_data="terms:show")
    kb.button(text=f"{ICON_PROFILE} Cá nhân", callback_data="profile:show")
    kb.adjust(1, 1, 2, 2, 2, 1)
    return kb.as_markup()


def admin_home_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    from app.utils.icons import ICON_TOPUP, ICON_MEM, ICON_USER, ICON_WALLET, ICON_PROFILE
    kb.button(text=f"{ICON_TOPUP} Yêu cầu nạp tiền", callback_data="admin:topup:help")
    kb.button(text=f"{ICON_TOPUP} Nạp thủ công theo user", callback_data="admin:manual_topup:start")
    kb.button(text=f"{ICON_WALLET} Check ví user", callback_data="admin:wallet_check:start")
    kb.button(text=f"{ICON_PROFILE} DS user đã /start", callback_data="admin:users:list")
    kb.button(text=f"{ICON_MEM} Đơn mem", callback_data="admin:mem:help")
    kb.button(text=f"{ICON_USER} Về giao diện user", callback_data="home:show")
    kb.adjust(1, 1, 1, 1, 1, 1)
    return kb.as_markup()
