# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from urllib.parse import quote

from app.config import Config
from app.db.topups import create_topup, get_topup
from app.keyboards.common import back_home_keyboard
from app.keyboards.admin import topup_admin_keyboard
from app.utils.text import topup_created_text, topup_info_text

router = Router()
_topup_pending: set[int] = set()


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


def _sepay_enabled(config: Config) -> bool:
    return bool(config.sepay_account_number and config.sepay_bank_name)


def _build_sepay_qr_url(config: Config, amount: int, note: str) -> str:
    acc = quote(config.sepay_account_number, safe="")
    bank = quote(config.sepay_bank_name, safe="")
    des = quote(note, safe="")
    return f"https://qr.sepay.vn/img?acc={acc}&bank={bank}&amount={amount}&des={des}&template=compact"


@router.callback_query(lambda c: c.data == "topup:info")
async def topup_info_callback(callback: CallbackQuery, config: Config) -> None:
    if not _sepay_enabled(config):
        await _edit_or_send(callback, topup_info_text(), reply_markup=back_home_keyboard())
        return
    if callback.from_user is None:
        return
    _topup_pending.add(callback.from_user.id)
    from app.utils.icons import ICON_TOPUP, ICON_INFO
    text = (
        f"{ICON_TOPUP} <b>NẠP TIỀN TỰ ĐỘNG</b>\n\n"
        f"{ICON_INFO} <i>Nhập số tiền bạn muốn nạp (VNĐ).</i>\n"
        f"Ví dụ: <code>200000</code>"
    )
    await _edit_or_send(callback, text, reply_markup=back_home_keyboard())


@router.message(Command("topup"))
async def topup_command(message: Message, config: Config) -> None:
    if message.from_user is None:
        return
    parts = message.text.split() if message.text else []
    if len(parts) < 2:
        from app.utils.icons import ICON_ERROR
        error_text = (
            f"{ICON_ERROR} <b>Cú pháp không đúng!</b>\n\n"
            f"<b>Cách sử dụng:</b>\n"
            f"<code>/topup [số_tiền]</code>\n\n"
            f"<b>Ví dụ:</b>\n"
            f"<code>/topup 200000</code>"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    try:
        amount = int(parts[1])
    except ValueError:
        from app.utils.icons import ICON_ERROR
        error_text = (
            f"{ICON_ERROR} <b>Số tiền không hợp lệ!</b>\n\n"
            f"Vui lòng nhập một số nguyên dương.\n"
            f"Ví dụ: <code>/topup 200000</code>"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    if amount <= 0:
        from app.utils.icons import ICON_ERROR
        error_text = (
            f"{ICON_ERROR} <b>Số tiền không hợp lệ!</b>\n\n"
            f"Số tiền phải lớn hơn 0."
        )
        await message.answer(error_text, parse_mode="HTML")
        return

    await _create_topup_flow(message, config, amount)


@router.message(lambda message: message.from_user is not None and message.from_user.id in _topup_pending)
async def topup_amount_input(message: Message, config: Config) -> None:
    if message.text is None or message.text.strip() == "" or message.text.strip().startswith("/"):
        return
    _topup_pending.discard(message.from_user.id)
    try:
        amount = int(message.text.strip())
    except ValueError:
        from app.utils.icons import ICON_ERROR
        error_text = (
            f"{ICON_ERROR} <b>Số tiền không hợp lệ!</b>\n\n"
            f"Vui lòng nhập một số nguyên dương.\n"
            f"Ví dụ: <code>200000</code>"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    if amount <= 0:
        from app.utils.icons import ICON_ERROR
        error_text = (
            f"{ICON_ERROR} <b>Số tiền không hợp lệ!</b>\n\n"
            f"Số tiền phải lớn hơn 0."
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    await _create_topup_flow(message, config, amount)


@router.callback_query(lambda c: c.data and c.data.startswith("topup:check:"))
async def topup_check_callback(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None:
        return
    try:
        topup_id = int(callback.data.split(":", 2)[2])
    except (IndexError, ValueError):
        return
    topup = await get_topup(config.db_path, topup_id)
    from app.utils.icons import ICON_INFO
    if not topup:
        await callback.answer("Không tìm thấy phiếu nạp.", show_alert=True)
        return
    if topup["status"] == "approved":
        await callback.answer("Nạp tiền đã thành công.", show_alert=True)
        from app.utils.text import topup_approved_text
        await callback.message.answer(topup_approved_text(topup["note"]), parse_mode="HTML")
        return
    try:
        await callback.answer("Hệ thống đang kiểm tra giao dịch...", show_alert=True)
    except Exception:
        pass
    await callback.message.answer(
        f"{ICON_INFO} <i>Đang chờ SePay xác nhận giao dịch. Vui lòng đợi...</i>",
        parse_mode="HTML",
    )


async def _create_topup_flow(message: Message, config: Config, amount: int) -> None:
    topup_id = await create_topup(config.db_path, message.from_user.id, amount, note="")
    note = f"NAP{message.from_user.id}-{amount}-{topup_id}"

    # Update note after we have ID
    from app.db.connection import get_db

    async with get_db(config.db_path) as db:
        await db.execute("UPDATE topups SET note = ? WHERE id = ?", (note, topup_id))
        await db.commit()

    if not _sepay_enabled(config):
        await message.answer(topup_created_text(note), parse_mode="HTML")
        for admin_id in config.admin_ids:
            from app.utils.icons import ICON_TOPUP
            admin_text = (
                f"{ICON_TOPUP} <b>YÊU CẦU NẠP TIỀN MỚI</b>\n\n"
                f"<b>Mã GD:</b> <code>{note}</code>\n"
                f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                f"<b>Số tiền:</b> <b>{amount:,} ₫</b>"
            )
            await message.bot.send_message(
                admin_id,
                admin_text,
                reply_markup=topup_admin_keyboard(topup_id),
                parse_mode="HTML"
            )
        return

    from app.utils.icons import ICON_TOPUP, ICON_INFO
    qr_url = _build_sepay_qr_url(config, amount, note)
    text = (
        f"{ICON_TOPUP} <b>NẠP TIỀN TỰ ĐỘNG</b>\n\n"
        f"<b>Ngân hàng:</b> {config.sepay_bank_name}\n"
        f"<b>Chủ TK:</b> {config.sepay_account_name or 'Chưa cấu hình'}\n"
        f"<b>Số TK:</b> <code>{config.sepay_account_number}</code>\n"
        f"<b>Số tiền:</b> <b>{amount:,} ₫</b>\n"
        f"<b>Nội dung:</b> <code>{note}</code>\n\n"
        f"{ICON_INFO} Quét QR hoặc chuyển khoản đúng nội dung, hệ thống sẽ tự cộng tiền."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Tôi đã chuyển khoản", callback_data=f"topup:check:{topup_id}")
    await message.answer_photo(qr_url, caption=text, reply_markup=kb.as_markup(), parse_mode="HTML")
