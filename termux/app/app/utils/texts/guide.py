# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    DIVIDER_STANDARD,
    ICON_GUIDE,
    ICON_PHONE,
    ICON_SERVICES,
    ICON_TOPUP,
    SECTION_FOOTER,
    SECTION_HEADER,
)

def guide_text() -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{ICON_GUIDE} **HƯỚNG DẪN SỬ DỤNG** {ICON_GUIDE}",

            SECTION_FOOTER,

            "",

            "**1️⃣ Chọn dịch vụ từ menu:**",

            f"   {ICON_SERVICES} Xem danh sách dịch vụ có sẵn",

            "",

            "**2️⃣ Nạp tiền khi cần thiết:**",

            f"   {ICON_TOPUP} Dùng lệnh: <code>/topup [số_tiền]</code>",

            "   💡 Ví dụ: <code>/topup 200000</code>",

            "",

            "**3️⃣ Liên hệ hỗ trợ:**",

            f"   {ICON_PHONE} Nhắn tin admin khi cần giúp đỡ",

            "",

            DIVIDER_STANDARD,

        ]

    )





