# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    DIVIDER_STANDARD,
    ICON_GUIDE,
    ICON_PHONE,
    ICON_SERVICES,
    ICON_TOPUP,
    ICON_MEM,
    SECTION_FOOTER,
    SECTION_HEADER,
)


def guide_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_GUIDE} <b>HUONG DAN SU DUNG</b> {ICON_GUIDE}",
            SECTION_FOOTER,
            "",
            f"{ICON_PHONE} <b>Admin:</b> <code>@Jimmy3212</code>",
            "",
            "<b>1) Huong dan dat hang</b>",
            f"- Chon <b>{ICON_MEM} Keo mem</b> hoac <b>📺 Telegram View</b> trong menu.",
            "- Chon goi ban can.",
            "- Nhap theo mau bot yeu cau: <code>link so_luong</code>.",
            "- Kiem tra lai don va bam <b>Xac nhan</b> de gui don.",
            "",
            "<b>2) Huong dan nap tien</b>",
            f"- Chon <b>{ICON_TOPUP} Nap Tien</b> trong menu hoac dung lenh:",
            "  <code>/topup [so_tien]</code>",
            "- Vi du: <code>/topup 200000</code>",
            "- Bot se tao ma giao dich va QR de chuyen khoan.",
            "- Chuyen dung noi dung, sau do bam <b>Toi da chuyen khoan</b> de kiem tra.",
            "",
            DIVIDER_STANDARD,
            f"{ICON_SERVICES} <i>Can ho tro, nhan admin: <code>@Jimmy3212</code></i>",
        ]
    )
