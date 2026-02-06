# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utils.icons import ICON_BACK, ICON_SERVICES

SERVICE_ITEMS = {
    "s1": {
        "title": "📣 Đăng quảng cáo kênh",
        "price": "200.000",
        "desc": "Đăng quảng cáo kênh trên hệ thống.",
    },
    "s2": {
        "title": "🛡️ Setup & quản trị group",
        "price": "500.000",
        "desc": "Setup và quản trị group chuyên nghiệp.",
    },
    "s3": {
        "title": "🧰 Tool/Proxy/VPS",
        "price": "Tùy gói",
        "desc": "Cung cấp tool/proxy/vps theo yêu cầu.",
    },
}


def services_list_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, item in SERVICE_ITEMS.items():
        kb.button(text=item["title"], callback_data=f"services:detail:{key}")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="home:show")
    kb.adjust(1)
    return kb.as_markup()


def service_detail_keyboard(service_key: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Tạo đơn", callback_data=f"services:order:{service_key}")
    kb.button(text=f"{ICON_BACK} Quay lại", callback_data="services:list")
    kb.adjust(1, 1)
    return kb.as_markup()
