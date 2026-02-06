# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.icons import (
    DIVIDER_STANDARD,
    ICON_INFO,
    ICON_MEM,
    ICON_PHONE,
    ICON_TOPUP,
    SECTION_FOOTER,
    SECTION_HEADER,
)


def mem_price_text(mem_type: str) -> str:
    if mem_type == "foreign":
        price_line = "120k / 1000 mem"
        label = "Mem nước ngoài"
    elif mem_type == "viet":
        price_line = "260k / 1000 mem"
        label = "Mem Việt Nam"
    else:
        price_line = "Liên hệ admin để biết giá."
        label = "Mem"
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **{label}** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_TOPUP} **Giá:** **{price_line}**",
            "",
            "_Vui lòng liên hệ admin để đặt hàng._",
        ]
    )


def mem_foreign_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **MEM NƯỚC NGOÀI** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            "_Chọn loại mem bạn muốn:_",
        ]
    )


def mem_viet_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **MEM VIỆT NAM** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            "_Chọn loại mem bạn muốn:_",
        ]
    )


def pull_mem_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **KÉO MEM** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            "_Chọn dịch vụ bạn muốn:_",
            "",
            DIVIDER_STANDARD,
        ]
    )


def pull_competitor_text() -> str:
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **KÉO MEM TỪ ĐỐI THỦ** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_TOPUP} **Giá:** **3.500.000 VND / 1000 mem**",
            f"{ICON_INFO} **Tối thiểu:** 500 mem",
            "",
            f"{ICON_PHONE} _Yêu cầu liên hệ admin để đặt hàng._",
            f"<code>@Jimmy3212</code>",
            "",
            DIVIDER_STANDARD,
        ]
    )


def mem_foreign_price_text(option: str) -> str:
    link = "https://t.me/+eyt9XtMTiNkwZTM9"
    min_line = "Tối thiểu 500 mem"
    example_line = f"Ví dụ: {link} 1000"
    if option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_line = "90k / 1000 mem"
    elif option == "allcountry":
        label = "Mem all country rẻ nhất"
        price_line = "40k / 1000 mem"
    elif option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_line = "45k / 1000 mem"
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_line = "105k / 1000 mem"
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_line = "120k / 1000 mem"
    else:
        label = "Mem nước ngoài"
        price_line = "Liên hệ admin để biết giá."
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **{label}** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_TOPUP} **Giá:** **{price_line}**",
            "",
            f"{ICON_INFO} **Gửi link và số lượng theo mẫu:**",
            f"{ICON_INFO} {example_line}",
            f"{ICON_INFO} **{min_line}**",
            "",
            "_Yêu cầu liên hệ admin để đặt hàng._",
        ]
    )


def mem_viet_price_text(option: str) -> str:
    link = "https://t.me/+eyt9XtMTiNkwZTM9"
    min_line = "Tối thiểu 500 mem"
    example_line = f"Ví dụ: {link} 1000"
    if option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_line = "150k / 1000 mem"
    elif option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_line = "200k / 1000 mem"
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_line = "230k / 1000 mem"
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_line = "260k / 1000 mem"
    else:
        label = "Mem Việt Nam"
        price_line = "Liên hệ admin để biết giá."
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **{label}** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_TOPUP} **Giá:** **{price_line}**",
            "",
            f"{ICON_INFO} **Gửi link và số lượng theo mẫu:**",
            f"{ICON_INFO} {example_line}",
            f"{ICON_INFO} **{min_line}**",
            "",
            "_Yêu cầu liên hệ admin để đặt hàng._",
        ]
    )


def mem_foreign_order_check_text(option: str, link: str, quantity: int) -> str:
    if option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_per_1000 = 90_000
    elif option == "allcountry":
        label = "Mem all country rẻ nhất"
        price_per_1000 = 40_000
    elif option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_per_1000 = 45_000
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_per_1000 = 105_000
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_per_1000 = 120_000
    else:
        label = "Mem nước ngoài"
        price_per_1000 = 0
    if price_per_1000 <= 0:
        price_line = "Liên hệ admin để biết giá."
        total_line = "Liên hệ admin để biết tổng tiền."
    else:
        price_line = f"{price_per_1000:,} / 1000 mem"
        total_price = round(price_per_1000 * quantity / 1000)
        total_line = f"{total_price:,} ₫"
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **XÁC NHẬN ĐƠN MEM** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_INFO} **Loại:** **{label}**",
            f"{ICON_TOPUP} **Đơn giá:** **{price_line}**",
            f"{ICON_INFO} **Link:** <code>{link}</code>",
            f"{ICON_INFO} **Số lượng:** **{quantity}**",
            f"{ICON_TOPUP} **Tổng tiền:** **{total_line}**",
            "",
            "_Bấm xác nhận để tạo đơn hoặc từ chối để nhập lại._",
        ]
    )


def mem_viet_order_check_text(option: str, link: str, quantity: int) -> str:
    if option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_per_1000 = 150_000
    elif option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_per_1000 = 200_000
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_per_1000 = 230_000
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_per_1000 = 260_000
    else:
        label = "Mem Việt Nam"
        price_per_1000 = 0
    if price_per_1000 <= 0:
        price_line = "Liên hệ admin để biết giá."
        total_line = "Liên hệ admin để biết tổng tiền."
    else:
        price_line = f"{price_per_1000:,} / 1000 mem"
        total_price = round(price_per_1000 * quantity / 1000)
        total_line = f"{total_price:,} ₫"
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **XÁC NHẬN ĐƠN MEM** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_INFO} **Loại:** **{label}**",
            f"{ICON_TOPUP} **Đơn giá:** **{price_line}**",
            f"{ICON_INFO} **Link:** <code>{link}</code>",
            f"{ICON_INFO} **Số lượng:** **{quantity}**",
            f"{ICON_TOPUP} **Tổng tiền:** **{total_line}**",
            "",
            "_Bấm xác nhận để tạo đơn hoặc từ chối để nhập lại._",
        ]
    )


def mem_foreign_order_created_text(option: str, link: str, quantity: int, order_id: str) -> str:
    service_line = "Mem nước ngoài"
    if option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_per_1000 = 90_000
    elif option == "allcountry":
        label = "Mem all country rẻ nhất"
        price_per_1000 = 40_000
    elif option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_per_1000 = 45_000
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_per_1000 = 105_000
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_per_1000 = 120_000
    else:
        label = "Mem nước ngoài"
        price_per_1000 = 0
    if price_per_1000 <= 0:
        total_line = "Liên hệ admin để biết tổng tiền."
    else:
        total_price = round(price_per_1000 * quantity / 1000)
        total_line = f"{total_price:,} ₫"
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **THÔNG TIN ĐƠN ĐẶT HÀNG** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_INFO} **Dịch vụ:** **{service_line}**",
            f"{ICON_INFO} **Loại:** **{label}**",
            f"{ICON_INFO} **Mã đơn:** `{order_id}`",
            f"{ICON_INFO} **Link:** `{link}`",
            f"{ICON_INFO} **Số lượng:** **{quantity}**",
            f"{ICON_TOPUP} **Tổng tiền:** **{total_line}**",
            "",
        ]
    )


def mem_viet_order_created_text(option: str, link: str, quantity: int, order_id: str) -> str:
    service_line = "Mem Việt Nam"
    if option == "lowdrop":
        label = "Mem ít tụt không bảo hành"
        price_per_1000 = 150_000
    elif option == "stable30":
        label = "Mem không tụt bảo hành 30 ngày"
        price_per_1000 = 200_000
    elif option == "stable60":
        label = "Mem không tụt bảo hành 60 ngày"
        price_per_1000 = 230_000
    elif option == "stable120":
        label = "Mem không tụt bảo hành 120 ngày"
        price_per_1000 = 260_000
    else:
        label = "Mem Việt Nam"
        price_per_1000 = 0
    if price_per_1000 <= 0:
        total_line = "Liên hệ admin để biết tổng tiền."
    else:
        total_price = round(price_per_1000 * quantity / 1000)
        total_line = f"{total_price:,} ₫"
    return join_lines(
        [
            SECTION_HEADER,
            f"{ICON_MEM} **THÔNG TIN ĐƠN ĐẶT HÀNG** {ICON_MEM}",
            SECTION_FOOTER,
            "",
            f"{ICON_INFO} **Dịch vụ:** **{service_line}**",
            f"{ICON_INFO} **Loại:** **{label}**",
            f"{ICON_INFO} **Mã đơn:** `{order_id}`",
            f"{ICON_INFO} **Link:** `{link}`",
            f"{ICON_INFO} **Số lượng:** **{quantity}**",
            f"{ICON_TOPUP} **Tổng tiền:** **{total_line}**",
            "",
        ]
    )
