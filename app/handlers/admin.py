# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.config import Config
from app.db.topups import get_topup, set_topup_status
from app.db.users import add_balance
from app.utils.text import topup_approved_text, topup_rejected_text

router = Router()


def _is_admin(config: Config, user_id: int) -> bool:
    return user_id in config.admin_ids


async def _edit_or_send(callback: CallbackQuery, text: str) -> None:
    msg = callback.message
    if msg is None:
        return
    if msg.text:
        await msg.edit_text(text, parse_mode="HTML")
        return
    if msg.caption is not None:
        await msg.edit_caption(caption=text, parse_mode="HTML")
        return
    await msg.answer(text, parse_mode="HTML")


@router.message(Command("admin_test"))
async def admin_test_command(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        await message.answer("Không có quyền", parse_mode="HTML")
        return
    await message.answer("✅ Admin test: bạn đã nhận được tin nhắn từ bot.", parse_mode="HTML")


@router.message(Command("gifid"))
async def admin_gif_id_command(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        await message.answer("Không có quyền", parse_mode="HTML")
        return
    target = message.reply_to_message or message
    if target.animation:
        await message.answer(f"<code>{target.animation.file_id}</code>", parse_mode="HTML")
        return
    await message.answer("Hãy reply vào tin nhắn GIF để lấy file_id.", parse_mode="HTML")


@router.message(lambda m: m.animation is not None)
async def admin_gif_id_from_animation(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        return
    await message.answer(f"<code>{message.animation.file_id}</code>", parse_mode="HTML")


@router.callback_query(lambda c: c.data == "admin:topup:help")
async def admin_topup_help(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_TOPUP, ICON_INFO
    text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_TOPUP} <b>QUẢN LÝ NẠP TIỀN</b> {ICON_TOPUP}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Hướng dẫn:</b>\n"
        f"Khi user tạo lệnh <code>/topup</code>, bot sẽ gửi thông báo kèm nút duyệt/từ chối.\n\n"
        f"<i>Bạn chỉ cần bấm nút trong tin nhắn đó.</i>"
    )
    await _edit_or_send(callback, text)


@router.callback_query(lambda c: c.data == "admin:mem:help")
async def admin_mem_help(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    from app.utils.icons import SECTION_HEADER, SECTION_FOOTER, ICON_MEM, ICON_INFO
    text = (
        f"{SECTION_HEADER}\n"
        f"{ICON_MEM} <b>QUẢN LÝ ĐƠN MEM</b> {ICON_MEM}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_INFO} <b>Hướng dẫn:</b>\n"
        f"Khi user xác nhận đơn mem, bot sẽ gửi thông tin đơn vào chat admin.\n\n"
        f"<i>Hiện tại đơn chưa có bước duyệt tự động.</i>"
    )
    await _edit_or_send(callback, text)


@router.callback_query(lambda c: c.data and c.data.startswith("admin:approve:"))
async def admin_approve_callback(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    topup_id = int(callback.data.split(":", 2)[2])
    topup = await get_topup(config.db_path, topup_id)
    if not topup:
        await callback.answer("Phiếu không tồn tại", show_alert=True)
        return
    if topup["status"] != "pending":
        await callback.answer("Phiếu đã xử lý", show_alert=True)
        return

    await add_balance(config.db_path, int(topup["user_id"]), int(topup["amount"]))
    await set_topup_status(config.db_path, topup_id, "approved")
    
    from app.utils.icons import ICON_APPROVE, SECTION_HEADER, SECTION_FOOTER, ICON_TOPUP
    admin_msg = (
        f"{SECTION_HEADER}\n"
        f"{ICON_APPROVE} <b>PHIẾU ĐÃ ĐƯỢC DUYỆT</b> {ICON_APPROVE}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_TOPUP} <b>Mã GD:</b> <code>{topup['note']}</code>"
    )
    await _edit_or_send(callback, admin_msg)

    await callback.bot.send_message(int(topup["user_id"]), topup_approved_text(topup["note"]), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("admin:reject:"))
async def admin_reject_callback(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    topup_id = int(callback.data.split(":", 2)[2])
    topup = await get_topup(config.db_path, topup_id)
    if not topup:
        await callback.answer("Phiếu không tồn tại", show_alert=True)
        return
    if topup["status"] != "pending":
        await callback.answer("Phiếu đã xử lý", show_alert=True)
        return

    await set_topup_status(config.db_path, topup_id, "rejected")
    
    from app.utils.icons import ICON_REJECT, SECTION_HEADER, SECTION_FOOTER, ICON_TOPUP
    admin_msg = (
        f"{SECTION_HEADER}\n"
        f"{ICON_REJECT} <b>PHIẾU ĐÃ BỊ TỪ CHỐI</b> {ICON_REJECT}\n"
        f"{SECTION_FOOTER}\n\n"
        f"{ICON_TOPUP} <b>Mã GD:</b> <code>{topup['note']}</code>"
    )
    await _edit_or_send(callback, admin_msg)

    await callback.bot.send_message(int(topup["user_id"]), topup_rejected_text(topup["note"]), parse_mode="HTML")
