# -*- coding: utf-8 -*-
from __future__ import annotations

import time

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.mem import (
    mem_keyboard,
    mem_foreign_keyboard,
    mem_viet_keyboard,
    pull_mem_keyboard,
    mem_order_confirm_keyboard,
)
from app.keyboards.common import back_home_keyboard
from app.config import Config
from app.db.users import deduct_balance, get_balance
from app.utils.icons import ICON_MEM, SECTION_HEADER, SECTION_FOOTER

router = Router()
_mem_foreign_pending: dict[int, dict[str, str | int]] = {}
_mem_foreign_option: dict[int, str] = {}
_mem_viet_pending: dict[int, dict[str, str | int]] = {}
_mem_viet_option: dict[int, str] = {}


async def _edit_or_send(callback: CallbackQuery, text: str, reply_markup=None) -> None:
    msg = callback.message
    if msg is None:
        return
    if msg.text:
        await msg.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        return
    if msg.caption is not None:
        await msg.edit_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")
        return
    await msg.answer(text, reply_markup=reply_markup, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "mem:list")
async def mem_list_callback(callback: CallbackQuery) -> None:
    text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_MEM} <b>CHỌN LOẠI MEM</b> {ICON_MEM}\n"
        f"{SECTION_FOOTER}\n\n"
        f"<i>Hãy chọn loại mem bạn muốn:</i>"
    )
    await _edit_or_send(callback, text, reply_markup=mem_keyboard())


@router.callback_query(lambda c: c.data == "pull:list")
async def pull_list_callback(callback: CallbackQuery) -> None:
    from app.utils.text import pull_mem_text
    await _edit_or_send(callback, pull_mem_text(), reply_markup=pull_mem_keyboard())


@router.callback_query(lambda c: c.data == "pull:competitor")
async def pull_competitor_callback(callback: CallbackQuery) -> None:
    from app.utils.text import pull_competitor_text
    await _edit_or_send(callback, pull_competitor_text(), reply_markup=back_home_keyboard())


@router.callback_query(lambda c: c.data == "mem:type:foreign")
async def mem_foreign_list_callback(callback: CallbackQuery) -> None:
    from app.utils.text import mem_foreign_text
    await _edit_or_send(callback, mem_foreign_text(), reply_markup=mem_foreign_keyboard())


@router.callback_query(lambda c: c.data == "mem:type:viet")
async def mem_viet_list_callback(callback: CallbackQuery) -> None:
    from app.utils.text import mem_viet_text
    await _edit_or_send(callback, mem_viet_text(), reply_markup=mem_viet_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("mem:type:") and c.data not in {"mem:type:foreign", "mem:type:viet"})
async def mem_type_callback(callback: CallbackQuery) -> None:
    from app.utils.text import mem_price_text
    mem_type = callback.data.split(":", 2)[2] if callback.data else ""
    await _edit_or_send(callback, mem_price_text(mem_type), reply_markup=back_home_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("mem:foreign:"))
async def mem_foreign_type_callback(callback: CallbackQuery) -> None:
    from app.utils.text import mem_foreign_price_text
    option = callback.data.split(":", 2)[2] if callback.data else ""
    if callback.from_user:
        _mem_foreign_option[callback.from_user.id] = option
    await _edit_or_send(callback, mem_foreign_price_text(option), reply_markup=back_home_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("mem:viet:"))
async def mem_viet_type_callback(callback: CallbackQuery) -> None:
    from app.utils.text import mem_viet_price_text
    option = callback.data.split(":", 2)[2] if callback.data else ""
    if callback.from_user:
        _mem_viet_option[callback.from_user.id] = option
    await _edit_or_send(callback, mem_viet_price_text(option), reply_markup=back_home_keyboard())


def _is_mem_order_message(message: Message) -> bool:
    if message.from_user is None:
        return False
    user_id = message.from_user.id
    if user_id not in _mem_foreign_option and user_id not in _mem_viet_option:
        return False
    # Topup flow also expects a plain text amount. If we keep the stale mem
    # selection active, this handler will incorrectly consume the amount input.
    from app.handlers.topup import _topup_pending
    if user_id in _topup_pending:
        return False
    # If user is in Telegram View flow, let that handler process the message.
    from app.handlers.telegram_view import _tv_pending, _tv_order_pending
    if user_id in _tv_pending or user_id in _tv_order_pending:
        return False
    return True


@router.message(_is_mem_order_message)
async def mem_order_input(message: Message) -> None:
    user_id = message.from_user.id
    if message.text is None or message.text.strip() == "" or message.text.strip().startswith("/"):
        return
    from app.utils.icons import ICON_ERROR, ICON_INFO
    parts = message.text.strip().split()
    if len(parts) < 2:
        error_text = (
            f"{ICON_ERROR} <b>Cú pháp không đúng!</b>\n\n"
            f"<b>Mẫu:</b> <code>link số_lượng</code>\n"
            f"<b>Ví dụ:</b> <code>https://t.me/+eyt9XtMTiNkwZTM9 1000</code>"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    link = parts[0]
    qty_raw = parts[1]
    try:
        quantity = int(qty_raw)
    except ValueError:
        error_text = (
            f"{ICON_ERROR} <b>Số lượng không hợp lệ!</b>\n\n"
            f"Vui lòng nhập một số nguyên dương."
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    if quantity <= 0:
        error_text = (
            f"{ICON_ERROR} <b>Số lượng không hợp lệ!</b>\n\n"
            f"Số lượng phải lớn hơn 0."
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    if quantity < 500:
        error_text = (
            f"{ICON_ERROR} <b>Số lượng không đủ!</b>\n\n"
            f"{ICON_INFO} <b>Tối thiểu:</b> 500 mem"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    if user_id in _mem_foreign_option:
        option = _mem_foreign_option.get(user_id, "")
        _mem_foreign_pending[user_id] = {"option": option, "link": link, "quantity": quantity}
        from app.utils.text import mem_foreign_order_check_text
        await message.answer(
            mem_foreign_order_check_text(option, link, quantity),
            reply_markup=mem_order_confirm_keyboard(),
            parse_mode="HTML",
        )
        return
    option = _mem_viet_option.get(user_id, "")
    _mem_viet_pending[user_id] = {"option": option, "link": link, "quantity": quantity}
    from app.utils.text import mem_viet_order_check_text
    await message.answer(
        mem_viet_order_check_text(option, link, quantity),
        reply_markup=mem_order_confirm_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "mem:order:confirm")
async def mem_foreign_order_confirm(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None:
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_MEM, ICON_INFO, ICON_USER
    data = _mem_foreign_pending.get(callback.from_user.id)
    order_type = "foreign"
    pending_bucket = "foreign"
    if data is None:
        data = _mem_viet_pending.get(callback.from_user.id)
        order_type = "viet"
        pending_bucket = "viet"
    if data is None:
        return
    option = str(data.get("option", ""))
    link = str(data.get("link", ""))
    quantity = int(data.get("quantity", 0))
    order_id = f"MEM-{int(time.time())}-{callback.from_user.id}"
    if order_type == "foreign":
        from app.utils.text import mem_foreign_order_created_text
        user_text = mem_foreign_order_created_text(option, link, quantity, order_id)
    else:
        from app.utils.text import mem_viet_order_created_text
        user_text = mem_viet_order_created_text(option, link, quantity, order_id)
    await _edit_or_send(callback, user_text, reply_markup=back_home_keyboard())
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Unknown"
    
    # Get mem type label
    if order_type == "foreign":
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
    else:
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

    total_price = 0

    if price_per_1000 <= 0:
        price_line = "Liên hệ admin để biết giá."
        total_line = "Liên hệ admin để biết tổng tiền."
    else:
        price_line = f"{price_per_1000:,} / 1000 mem"
        total_price = round(price_per_1000 * quantity / 1000)
        total_line = f"{total_price:,} ₫"

    if total_price <= 0:
        await callback.answer("Kh??ng x??c ?????nh gi??, vui l??ng li??n h??? admin.", show_alert=True)
        return
    balance = await get_balance(config.db_path, callback.from_user.id)
    if balance < total_price:
        from app.utils.icons import ICON_ERROR, ICON_TOPUP
        await callback.answer("So du khong du.", show_alert=True)
        await _edit_or_send(
            callback,
            f"{ICON_ERROR} <b>So du khong du!</b>\n\n"
            f"{ICON_TOPUP} <b>Can:</b> <b>{total_price:,} vnd</b>\n"
            f"{ICON_TOPUP} <b>So du:</b> <b>{balance:,} vnd</b>",
            reply_markup=back_home_keyboard(),
        )
        return
    deducted = await deduct_balance(config.db_path, callback.from_user.id, total_price)
    if not deducted:
        await callback.answer("S??? d?? kh??ng ?????.", show_alert=True)
        return
    if pending_bucket == "foreign":
        _mem_foreign_pending.pop(callback.from_user.id, None)
    else:
        _mem_viet_pending.pop(callback.from_user.id, None)


    admin_text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_MEM} <b>ĐƠN MEM MỚI</b> {ICON_MEM}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Mã đơn:</b> <code>{order_id}</code>\n"
        f"{ICON_INFO} <b>Dịch vụ:</b> <b>{service_line}</b>\n"
        f"{ICON_INFO} <b>Loại:</b> <b>{label}</b>\n"
        f"{ICON_INFO} <b>Đơn giá:</b> <b>{price_line}</b>\n"
        f"{ICON_INFO} <b>Tổng tiền:</b> <b>{total_line}</b>\n"
        f"{ICON_INFO} <b>Link:</b> <code>{link}</code>\n"
        f"{ICON_INFO} <b>Số lượng:</b> <b>{quantity}</b>\n\n"
        f"{ICON_USER} <b>User ID:</b> <code>{user_id}</code>\n"
        f"{ICON_USER} <b>Name:</b> <code>{user_name}</code>\n"
        f"{ICON_INFO} <i>Vui lòng xử lý đơn theo quy trình nội bộ.</i>"
    )
    for admin_id in config.admin_ids:
        await callback.bot.send_message(admin_id, admin_text, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "mem:order:deny")
async def mem_foreign_order_deny(callback: CallbackQuery) -> None:
    if callback.from_user is None:
        return
    data = _mem_foreign_pending.pop(callback.from_user.id, None)
    if data is not None:
        option = _mem_foreign_option.get(callback.from_user.id, "")
        from app.utils.text import mem_foreign_price_text
        await _edit_or_send(callback, mem_foreign_price_text(option), reply_markup=back_home_keyboard())
        return
    data = _mem_viet_pending.pop(callback.from_user.id, None)
    if data is not None:
        option = _mem_viet_option.get(callback.from_user.id, "")
        from app.utils.text import mem_viet_price_text
        await _edit_or_send(callback, mem_viet_price_text(option), reply_markup=back_home_keyboard())
