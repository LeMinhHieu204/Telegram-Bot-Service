# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    ICON_LOCK,
    ICON_TERMS,
    SECTION_FOOTER,
    SECTION_HEADER,
)

def terms_text() -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{ICON_TERMS} **ĐIỀU KHOẢN SỬ DỤNG** {ICON_TERMS}",

            SECTION_FOOTER,

            "",

            "**🔹 Nội dung chính:**",

            "",

            "**🔸 Quy tắc hành vi:**",

            "   • Không spam, không lạm dụng",

            "   • Không vi phạm pháp luật",

            f"   {ICON_LOCK} Tuân thủ các quy định chung",

            "",

            "**🔸 Chính sách hoàn tiền:**",

            "   • Hoàn tiền theo điều khoản cụ thể",

            "   • Liên hệ admin để được hỗ trợ",

            "",

            "**🔸 Đồng ý:**",

            "   Sử dụng dịch vụ = Chấp nhận toàn bộ điều khoản",

        ]

    )





