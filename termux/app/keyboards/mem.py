# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_BACK, ICON_APPROVE, ICON_REJECT


def mem_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🌍 Mem nước ngoài", callback_data="mem:type:foreign")
    kb.button(text="🇻🇳 Mem Việt Nam", callback_data="mem:type:viet")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    kb.adjust(1, 1, 1)
    return kb.as_markup()


def mem_foreign_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Mem không tụt bảo hành 30 ngày", callback_data="mem:foreign:stable30")
    kb.button(text="Mem all country rẻ nhất", callback_data="mem:foreign:allcountry")
    kb.button(text="Mem ít tụt không bảo hành", callback_data="mem:foreign:lowdrop")
    kb.button(text="Mem không tụt bảo hành 60 ngày", callback_data="mem:foreign:stable60")
    kb.button(text="Mem không tụt bảo hành 120 ngày", callback_data="mem:foreign:stable120")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="pull:list")
    kb.adjust(1, 1, 1, 1, 1, 1)
    return kb.as_markup()


def pull_mem_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🌍 Mem nước ngoài", callback_data="mem:type:foreign")
    kb.button(text="🇻🇳 Mem Việt Nam", callback_data="mem:type:viet")
    kb.button(text="⚔️ Kéo mem từ đối thủ", callback_data="pull:competitor")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    kb.adjust(1, 1, 1, 1)
    return kb.as_markup()


def mem_order_confirm_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{ICON_APPROVE} Xác nhận", callback_data="mem:order:confirm")
    kb.button(text=f"{ICON_REJECT} Từ chối", callback_data="mem:order:deny")
    kb.adjust(1, 1)
    return kb.as_markup()


def mem_viet_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Mem ít tụt không bảo hành", callback_data="mem:viet:lowdrop")
    kb.button(text="Mem không tụt bảo hành 30 ngày", callback_data="mem:viet:stable30")
    kb.button(text="Mem không tụt bảo hành 60 ngày", callback_data="mem:viet:stable60")
    kb.button(text="Mem không tụt bảo hành 120 ngày", callback_data="mem:viet:stable120")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="pull:list")
    kb.adjust(1, 1, 1, 1, 1)
    return kb.as_markup()
