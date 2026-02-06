# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    DIVIDER_STANDARD,
    ICON_INFO,
    ICON_LOADING,
    ICON_SERVICES,
    ICON_TOPUP,
    SECTION_FOOTER,
    SECTION_HEADER,
)

def services_intro_text() -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{ICON_SERVICES} **DANH MỤC DỊCH VỤ** {ICON_SERVICES}",

            SECTION_FOOTER,

            "",

            "_Chọn dịch vụ dưới đây để xem chi tiết:_",

            "",

            DIVIDER_STANDARD,

        ]

    )





def service_detail_text(title: str, price: str, desc: str) -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"**{title}**",

            SECTION_FOOTER,

            "",

            f"{ICON_TOPUP} **Giá:** **{price}**",

            "",

            f"{ICON_INFO} **Mô tả:**",

            desc,

            "",

            DIVIDER_STANDARD,

        ]

    )





def service_order_stub_text() -> str:

    return join_lines(

        [

            f"{ICON_LOADING} **TÍNH NĂNG ĐANG PHÁT TRIỂN**",

            "",

            "_Vui lòng quay lại sau..._",

        ]

    )





