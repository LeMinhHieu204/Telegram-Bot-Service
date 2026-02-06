# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    BADGE_PENDING,
    BADGE_SUCCESS,
    DIVIDER_BOLD,
    DIVIDER_STANDARD,
    ICON_INFO,
    ICON_PHONE,
    ICON_REJECT,
    ICON_TOPUP,
    SECTION_FOOTER,
    SECTION_FOOTER_ENHANCED,
    SECTION_HEADER,
    SECTION_HEADER_ENHANCED,
)

def topup_info_text() -> str:

    return join_lines(

        [

            SECTION_HEADER_ENHANCED,

            f"{ICON_TOPUP} **NẠP TIỀN VÀO TÀI KHOẢN** {ICON_TOPUP}",

            SECTION_FOOTER_ENHANCED,

            "",

            "**Phương thức nạp tiền:** Xác nhận thủ công",

            "",

            "**Cách sử dụng lệnh:**",

            "<code>/topup [số_tiền]</code>",

            "",

            "**Ví dụ cụ thể:**",

            "<code>/topup 200000</code>",

            "",

            DIVIDER_BOLD,

            f"{ICON_INFO} _Admin sẽ xác nhận trong thời gian sớm nhất!_",

        ]

    )





def topup_created_text(note: str) -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{BADGE_PENDING} **PHIẾU NẠP TIỀN ĐÃ TẠO** {BADGE_PENDING}",

            SECTION_FOOTER,

            "",

            f"**Mã GD:** <code>{note}</code>",

            f"**Trạng thái:** _Chờ xác nhận_",

            "",

            f"{ICON_INFO} _Vui lòng chờ admin duyệt phiếu của bạn..._",

            DIVIDER_STANDARD,

        ]

    )





def topup_rejected_text(note: str) -> str:

    return join_lines(

        [

            SECTION_HEADER,

            f"{ICON_REJECT} **PHIẾU NẠP TIỀN BỊ TỪ CHỐI**",

            SECTION_FOOTER,

            "",

            f"<code>Mã GD: {note}</code>",

            "",

            f"{ICON_INFO} _Vui lòng liên hệ admin để tìm hiểu thêm._",

            f"{ICON_PHONE} <code>@Jimmy3212</code>",

        ]

    )





def topup_approved_text(note: str) -> str:

    return join_lines(

        [

            SECTION_HEADER_ENHANCED,

            f"{BADGE_SUCCESS} **NẠP TIỀN THÀNH CÔNG** {BADGE_SUCCESS}",

            SECTION_FOOTER_ENHANCED,

            "",

            f"{ICON_TOPUP} **Mã GD:** <code>{note}</code>",

            "",

            f"{BADGE_SUCCESS} **Trạng thái:** _Đã cập nhật vào tài khoản_",

            "",

            DIVIDER_BOLD,

        ]

    )





