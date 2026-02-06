# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.format import format_currency_vnd
from app.utils.icons import (
    DIVIDER_STANDARD,
    ICON_PROFILE,
    ICON_USER,
    ICON_WALLET,
    SECTION_FOOTER,
    SECTION_HEADER,
)

def profile_text(user_id: int, name: str, balance: int) -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{ICON_PROFILE} **THÔNG TIN CÁ NHÂN** {ICON_PROFILE}",

            SECTION_FOOTER,

            "",

            f"**{ICON_USER} User ID:**",

            f"<code>{user_id}</code>",

            "",

            f"**{ICON_USER} Tên:**",

            f"<code>{name}</code>",

            "",

            f"**{ICON_WALLET} Số dư hiện tại:**",

            f"**{format_currency_vnd(balance)}**",

            "",

            DIVIDER_STANDARD,

        ]

    )





