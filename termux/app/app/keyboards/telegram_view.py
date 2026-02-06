# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_BACK, ICON_APPROVE, ICON_REJECT


def telegram_view_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Telegram Phản ứng Tích Cực 🔥⚡️🎉🍓🥰😘🤩👻 + Views Đang hoạt động", callback_data="tv:positive:active")
    kb.button(text="Telegram Phản ứng Tích Cực Kết Hợp 🔥🎆🎉🍓🥰😘🤩👻🧠❤️ + Views Chậm", callback_data="tv:positive:slow")
    kb.button(text="Telegram Phản ứng Tiêu Cực 💡🤔🥴😡😭 + Views", callback_data="tv:negative")
    kb.button(text="Telegram Like (👍) Phản ứng + Views 1M", callback_data="tv:like")
    kb.button(text="Telegram Dislike (👎) Phản ứng + Views 1M", callback_data="tv:dislike")
    kb.button(text="Telegram Heart (❤️) Phản ứng + Views", callback_data="tv:heart")
    kb.button(text="Telegram Fire (🔥) Phản ứng + Views 1M", callback_data="tv:fire")
    kb.button(text="Telegram Party-pooper (🎉🎊) Phản ứng + Views 1M", callback_data="tv:party")
    kb.button(text="Telegram Starstruck (🎇) Phản ứng + Views 1M", callback_data="tv:starstruck")
    kb.button(text="Telegram Screaming Face (😱) Phản ứng + Views 1M", callback_data="tv:scream")
    kb.button(text="Telegram Beaming Face (😁) Phản ứng + Views 1M", callback_data="tv:beaming")
    kb.button(text="Telegram Crying Face (😢) Phản ứng + Views 1M", callback_data="tv:cry")
    kb.button(text="Telegram Pile of Poo (💩) Phản ứng + Views 1M", callback_data="tv:poo")
    kb.button(text="Telegram Face Vomiting (🤮) Phản ứng + Views 1M", callback_data="tv:vomit")
    kb.button(text="Telegram Phản ứng Tích Cực 🔥⚡️🎉🍓🥰😘🤩👻 + Views Nhanh", callback_data="tv:positive:fast")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    kb.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return kb.as_markup()


def telegram_view_confirm_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_APPROVE} Xác nhận", callback_data="tv:order:confirm")
    kb.button(text=f"{ICON_REJECT} Từ chối", callback_data="tv:order:deny")
    kb.adjust(1, 1)
    return kb.as_markup()
