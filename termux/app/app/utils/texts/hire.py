# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    ICON_INFO,
    SECTION_FOOTER,
    SECTION_HEADER,
)

def bot_hire_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_INFO} **NHẬN LÀM BOT**",
            SECTION_FOOTER,
            "",
            "**Liên hệ admin:** <code>@Jimmy3212</code>",
            "",
            "**Ưu điểm khi làm bot:**",
            "• Tư vấn & lên ý tưởng theo đúng nhu cầu kinh doanh của bạn",
            "• Thiết kế giao diện bot rõ ràng, dễ dùng, tối ưu thao tác",
            "• Luồng đặt đơn gọn, có xác nhận, hạn chế nhầm lẫn",
            "• Tự động hóa: trả lời, báo giá, hướng dẫn, xử lý đơn",
            "• Tích hợp nạp tiền/duyệt đơn theo yêu cầu",
            "• Tùy biến nhiều menu/dịch vụ, mở rộng linh hoạt",
            "• Bảo trì nhanh, hỗ trợ chỉnh sửa theo phản hồi",
            "• Bảo mật thông tin, quyền admin rõ ràng",
            "• Có thể gửi thông báo tới admin & user tức thì",
            "• Tốc độ phản hồi nhanh, hoạt động ổn định",
            "• Hỗ trợ thêm tính năng theo giai đoạn",
            "• Tối ưu chi phí vận hành, giảm công sức quản lý",
            "• Dễ nâng cấp khi mở rộng dịch vụ sau này",
            "• Thời gian triển khai nhanh, bàn giao đầy đủ",
            "• Cam kết đồng hành & hỗ trợ lâu dài",
        ]
    )


