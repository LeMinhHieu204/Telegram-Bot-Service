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
            f"{ICON_GUIDE} <b>HƯỚNG DẪN SỬ DỤNG</b> {ICON_GUIDE}",
            SECTION_FOOTER,
            "",
            f"{ICON_PHONE} <b>Admin:</b> <code>@Jimmy3212</code>",
            "",
            "<b>1) Hướng dẫn đặt hàng</b>",
            f"- Chọn <b>{ICON_MEM} Kéo mem</b> hoặc <b>📺 Telegram View</b> trong menu.",
            "- Chọn gói bạn cần.",
            "- Nhập theo mẫu bot yêu cầu: <code>link số_lượng</code>.",
            "- Kiểm tra lại đơn và bấm <b>Xác nhận</b> để gửi đơn.",
            "",
            "<b>2) Hướng dẫn nạp tiền</b>",
            f"- Chọn <b>{ICON_TOPUP} Nạp Tiền</b> trong menu.",
            "- Nhập số tiền bạn muốn nạp.",
            "- Bot sẽ gửi mã QR kèm thông tin chuyển khoản.",
            "- Quét QR hoặc chuyển khoản đúng số tiền và đúng nội dung.",
            "- Sau khi giao dịch được xác nhận, hệ thống sẽ tự động cộng tiền vào tài khoản.",
            "- Nếu lỗi khi nạp, vui lòng liên hệ admin: <code>@Jimmy3212</code>.",
            "",
            DIVIDER_STANDARD,
            f"{ICON_SERVICES} <i>Cần hỗ trợ, nhắn admin: <code>@Jimmy3212</code></i>",
        ]
    )
