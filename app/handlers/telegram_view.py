# -*- coding: utf-8 -*-
from __future__ import annotations

import time

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramNetworkError

from app.keyboards.telegram_view import telegram_view_keyboard, telegram_view_confirm_keyboard
from app.keyboards.common import back_home_keyboard
from app.config import Config
from app.db.users import deduct_balance, get_balance

router = Router()
_tv_pending: set[int] = set()
_tv_order_pending: dict[int, dict[str, str | int]] = {}
_tv_selected: dict[int, str] = {}

TV_LABEL_MAP = {
    "tv:positive:active": "Telegram Phản ứng Tích Cực 🔥⚡️🎉🍓🥰😘🤩👻 + Views Đang hoạt động",
    "tv:positive:slow": "Telegram Phản ứng Tích Cực Kết Hợp 🔥🎆🎉🍓🥰😘🤩👻🧠❤️ + Views Chậm",
    "tv:negative": "Telegram Phản ứng Tiêu Cực 💡🤔🥴😡😭 + Views",
    "tv:like": "Telegram Like (👍) Phản ứng + Views 1M",
    "tv:dislike": "Telegram Dislike (👎) Phản ứng + Views 1M",
    "tv:heart": "Telegram Heart (❤️) Phản ứng + Views",
    "tv:fire": "Telegram Fire (🔥) Phản ứng + Views 1M",
    "tv:party": "Telegram Party-pooper (🎉🎊) Phản ứng + Views 1M",
    "tv:starstruck": "Telegram Starstruck (🎇) Phản ứng + Views 1M",
    "tv:scream": "Telegram Screaming Face (😱) Phản ứng + Views 1M",
    "tv:beaming": "Telegram Beaming Face (😁) Phản ứng + Views 1M",
    "tv:cry": "Telegram Crying Face (😢) Phản ứng + Views 1M",
    "tv:poo": "Telegram Pile of Poo (💩) Phản ứng + Views 1M",
    "tv:vomit": "Telegram Face Vomiting (🤮) Phản ứng + Views 1M",
    "tv:positive:fast": "Telegram Phản ứng Tích Cực 🔥⚡️🎉🍓🥰😘🤩👻 + Views Nhanh",
}


@router.callback_query(lambda c: c.data == "tv:list")
async def tv_list_callback(callback: CallbackQuery) -> None:
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_SERVICES, ICON_TOPUP
    text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_SERVICES} <b>TELEGRAM VIEW</b> {ICON_SERVICES}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_TOPUP} <b>Giá:</b> <b>5k / 1000 view</b> + tăng cảm xúc\n\n"
        f"<i>Chọn gói bạn cần:</i>"
    )
    await callback.message.edit_text(text, reply_markup=telegram_view_keyboard(), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("tv:") and c.data not in {"tv:order:confirm", "tv:order:deny"})
async def tv_type_callback(callback: CallbackQuery) -> None:
    if callback.from_user is None:
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_TOPUP, ICON_INFO
    _tv_selected[callback.from_user.id] = callback.data
    _tv_pending.add(callback.from_user.id)
    selected_label = TV_LABEL_MAP.get(callback.data, "Không xác định")
    text = (
        f"{SECTION_HEADER}\n"
        f"<b>CHI TIẾT GÓI</b>\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Gói:</b> {selected_label}\n"
        f"{ICON_TOPUP} <b>Giá:</b> <b>5k / 1000 view</b> + tăng cảm xúc\n\n"
        f"<b>📝 Nhập thông tin:</b>\n"
        f"<code>link_group số_lượng</code>\n\n"
        f"<b>💡 Ví dụ:</b>\n"
        f"<code>https://t.me/ten_group 1000</code>\n\n"
        f"<i>Tối thiểu: 1000</i>"
    )
    await callback.message.edit_text(text, reply_markup=back_home_keyboard(), parse_mode="HTML")


@router.message(lambda message: message.from_user is not None and message.from_user.id in _tv_pending)
async def tv_link_input(message: Message) -> None:
    if message.text is None or message.text.strip() == "" or message.text.strip().startswith("/"):
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_INFO, ICON_TOPUP, ICON_ERROR
    parts = message.text.strip().split()
    if len(parts) < 2:
        error_text = (
            f"{ICON_ERROR} <b>Cú pháp không đúng!</b>\n\n"
            f"<b>Mẫu:</b> <code>link số_lượng</code>\n"
            f"<b>Ví dụ:</b> <code>https://t.me/ten_group 1000</code>"
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
    if quantity < 1000:
        error_text = (
            f"{ICON_ERROR} <b>Số lượng không đủ!</b>\n\n"
            f"Tối thiểu: 1000"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    _tv_pending.discard(message.from_user.id)
    order_id = f"TV-{int(time.time())}-{message.from_user.id}"
    _tv_order_pending[message.from_user.id] = {
        "link": link,
        "quantity": quantity,
        "order_id": order_id,
    }
    selected = _tv_selected.get(message.from_user.id, "")
    selected_label = TV_LABEL_MAP.get(selected, "Không xác định")
    await message.answer(
        f"{SECTION_HEADER}\n"
        f"<b>XÁC NHẬN ĐƠN</b>\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Gói:</b> {selected_label}\n"
        f"{ICON_INFO} <b>Link:</b> <code>{link}</code>\n"
        f"{ICON_INFO} <b>Số lượng:</b> <b>{quantity}</b>\n"
        f"{ICON_TOPUP} <b>Giá:</b> 5k / 1000 view + tăng cảm xúc",
        reply_markup=telegram_view_confirm_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "tv:order:confirm")
async def tv_order_confirm(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None:
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_SUCCESS, ICON_SERVICES, ICON_INFO, ICON_TOPUP
    data = _tv_order_pending.get(callback.from_user.id)
    if data is None:
        await callback.answer("Đơn đã hết hạn, vui lòng nhập lại.", show_alert=True)
        return
    link = str(data.get("link", ""))
    quantity = int(data.get("quantity", 0))
    order_id = str(data.get("order_id", ""))
    selected = _tv_selected.pop(callback.from_user.id, "")
    selected_label = TV_LABEL_MAP.get(selected, "Không xác định")
    cost = ((quantity + 999) // 1000) * 5000
    balance = await get_balance(config.db_path, callback.from_user.id)
    if balance < cost:
        from app.utils.icons import ICON_ERROR, ICON_TOPUP
        await callback.answer("S??? d?? kh??ng ?????.", show_alert=True)
        await callback.message.answer(
            f"{ICON_ERROR} <b>S??? d?? kh??ng ?????!</b>\n\n"
            f"{ICON_TOPUP} <b>C???n:</b> <b>{cost:,} ???</b>\n"
            f"{ICON_TOPUP} <b>S??? d??:</b> <b>{balance:,} ???</b>",
            parse_mode="HTML",
        )
        return
    deducted = await deduct_balance(config.db_path, callback.from_user.id, cost)
    if not deducted:
        await callback.answer("S??? d?? kh??ng ?????.", show_alert=True)
        return
    _tv_order_pending.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        f"{ICON_SUCCESS} <b>ĐẶT ĐƠN THÀNH CÔNG</b>\n\n"
        f"{ICON_SERVICES} <b>Gói:</b> {selected_label}\n"
        f"{ICON_INFO} <b>Link:</b> <code>{link}</code>\n"
        f"{ICON_INFO} <b>Số lượng:</b> <b>{quantity}</b>\n"
        f"{ICON_TOPUP} <b>Giá:</b> 5k / 1000 view + tăng cảm xúc",
        reply_markup=back_home_keyboard(),
        parse_mode="HTML",
    )
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Unknown"
    admin_text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_SERVICES} <b>ĐƠN TELEGRAM VIEW</b> {ICON_SERVICES}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Mã đơn:</b> <code>{order_id}</code>\n"
        f"{ICON_INFO} <b>Gói:</b> <code>{selected_label}</code>\n"
        f"{ICON_INFO} <b>Link:</b> <code>{link}</code>\n"
        f"{ICON_INFO} <b>Số lượng:</b> <b>{quantity}</b>\n"
        f"{ICON_TOPUP} <b>Giá:</b> <b>5k / 1000 view</b> + tăng cảm xúc\n\n"
        f"{ICON_INFO} <b>User ID:</b> <code>{user_id}</code>\n"
        f"{ICON_INFO} <b>Name:</b> <code>{user_name}</code>\n"
        f"{ICON_INFO} <i>Vui lòng xử lý đơn theo quy trình nội bộ.</i>"
    )
    for admin_id in config.admin_ids:
        try:
            await callback.bot.send_message(admin_id, admin_text, parse_mode="HTML")
        except (TelegramForbiddenError, TelegramBadRequest, TelegramNetworkError):
            continue


@router.callback_query(lambda c: c.data == "tv:order:deny")
async def tv_order_deny(callback: CallbackQuery) -> None:
    if callback.from_user is None:
        return
    from app.utils.icons import ICON_ERROR
    _tv_order_pending.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        f"{ICON_ERROR} <b>Đã hủy</b>\n\n"
        f"Vui lòng nhập lại: <code>link số_lượng</code>",
        reply_markup=back_home_keyboard(),
        parse_mode="HTML",
    )
