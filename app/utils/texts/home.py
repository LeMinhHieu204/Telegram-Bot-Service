# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.format import format_currency_vnd
from app.utils.icons import (
    DIVIDER_BOLD,
    ICON_BELL,
    ICON_HOME,
    ICON_LOCK,
    ICON_USER,
    ICON_WALLET,
    SECTION_FOOTER_ENHANCED,
    SECTION_HEADER_ENHANCED,
)


def welcome_text(user_id: int, name: str, balance: int, is_admin: bool = False) -> str:
    admin_line = f"\n{ICON_LOCK} **Admin mode:** **ON**" if is_admin else ""

    lines = [
        SECTION_HEADER_ENHANCED,
        f"{ICON_HOME} **Welcome to MemPrimebot** {ICON_HOME}",
        SECTION_FOOTER_ENHANCED,
        f"{ICON_USER} **UserID:** <code>{user_id}</code>",
        f"{ICON_USER} **Name:** <code>{name}</code>",
        f"{ICON_WALLET} **Balance:** **{format_currency_vnd(balance)}**",
        
        f"{ICON_BELL} **Notice:** Bot works 8:00 PM - 11:30 PM. Other times update services.",
    ]

    if admin_line:
        lines.append(admin_line)

    lines.extend(
        [
            "",
            DIVIDER_BOLD,
            f"{ICON_BELL} _Please check terms and guide_",
        ]
    )

    return join_lines(lines)


def admin_welcome_text(user_id: int, name: str) -> str:
    return join_lines(
        [
            SECTION_HEADER_ENHANCED,
            f"{ICON_LOCK} **ADMIN PANEL** {ICON_LOCK}",
            SECTION_FOOTER_ENHANCED,
            "",
            f"{ICON_USER} **UserID:** <code>{user_id}</code>",
            f"{ICON_USER} **Name:** <code>{name}</code>",
            "",
            DIVIDER_BOLD,
            "**Select admin actions below:**",
        ]
    )
