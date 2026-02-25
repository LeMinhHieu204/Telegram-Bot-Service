# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.config import Config
from app.db.topups import get_topup, set_topup_status
from app.db.users import add_balance, get_user_id_by_username, get_user_wallet, list_users_brief
from app.keyboards.admin import manual_topup_confirm_keyboard, manual_topup_start_keyboard
from app.utils.text import topup_approved_text, topup_rejected_text

router = Router()
_manual_topup_sessions: dict[int, dict[str, str | int]] = {}
_wallet_check_sessions: set[int] = set()


def _is_admin(config: Config, user_id: int) -> bool:
    return user_id in config.admin_ids


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
        f"<i>Bạn chỉ cần bấm nút trong tin nhắn đó.</i>\n\n"
        f"Hoặc chọn nạp thủ công theo username ở nút bên dưới."
    )
    await _edit_or_send(callback, text, reply_markup=manual_topup_start_keyboard())


@router.callback_query(lambda c: c.data == "admin:manual_topup:start")
async def admin_manual_topup_start(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    admin_id = callback.from_user.id
    _wallet_check_sessions.discard(admin_id)
    _manual_topup_sessions[admin_id] = {"step": "username"}
    await _edit_or_send(
        callback,
        "💰 <b>NẠP TIỀN THỦ CÔNG</b>\n\nNhập <b>username</b> user cần nạp.\nVí dụ: <code>@abc123</code>",
    )


@router.message(
    lambda m: m.from_user is not None
    and m.from_user.id in _manual_topup_sessions
    and m.from_user.id not in _wallet_check_sessions
    and m.text is not None
)
async def admin_manual_topup_input(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        return
    admin_id = message.from_user.id
    session = _manual_topup_sessions.get(admin_id)
    if session is None:
        return
    raw_text = message.text.strip()
    if raw_text == "" or raw_text.startswith("/"):
        return
    step = str(session.get("step", ""))

    if step == "username":
        username = raw_text.lstrip("@").lower()
        user_id = await get_user_id_by_username(config.db_path, username)
        if user_id is None:
            await message.answer(
                "Không tìm thấy user theo username này trong dữ liệu bot.\n"
                "Yêu cầu user vào bot bấm <code>/start</code> rồi thử lại.",
                parse_mode="HTML",
            )
            return
        session["step"] = "amount"
        session["target_username"] = username
        session["target_user_id"] = int(user_id)
        await message.answer(
            f"Đã chọn user <code>@{username}</code> (ID: <code>{user_id}</code>).\n"
            "Nhập số tiền muốn nạp (VNĐ). Ví dụ: <code>200000</code>",
            parse_mode="HTML",
        )
        return

    if step == "amount":
        try:
            amount = int(raw_text.replace(",", "").replace(".", ""))
        except ValueError:
            await message.answer("Số tiền không hợp lệ. Vui lòng nhập số nguyên dương.", parse_mode="HTML")
            return
        if amount <= 0:
            await message.answer("Số tiền phải lớn hơn 0.", parse_mode="HTML")
            return
        target_username = str(session.get("target_username", ""))
        target_user_id = int(session.get("target_user_id", 0))
        if not target_username or target_user_id <= 0:
            _manual_topup_sessions.pop(admin_id, None)
            await message.answer("Phiên nạp tiền không hợp lệ, vui lòng bắt đầu lại.", parse_mode="HTML")
            return
        session["step"] = "confirm"
        session["amount"] = amount
        await message.answer(
            "💰 <b>XÁC NHẬN NẠP TIỀN</b>\n\n"
            f"User: <code>@{target_username}</code>\n"
            f"User ID: <code>{target_user_id}</code>\n"
            f"Số tiền: <b>{amount:,} ₫</b>\n\n"
            "Bấm nút bên dưới để xác nhận.",
            reply_markup=manual_topup_confirm_keyboard(),
            parse_mode="HTML",
        )
        return

    await message.answer(
        "Phiên nạp tiền không hợp lệ hoặc đã hết hạn. Bấm lại nút nạp thủ công để bắt đầu.",
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "admin:manual_topup:cancel")
async def admin_manual_topup_cancel(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    _manual_topup_sessions.pop(callback.from_user.id, None)
    await _edit_or_send(callback, "Đã hủy phiên nạp tiền thủ công.")


@router.callback_query(lambda c: c.data == "admin:manual_topup:confirm")
async def admin_manual_topup_confirm(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    admin_id = callback.from_user.id
    session = _manual_topup_sessions.get(admin_id)
    if session is None or session.get("step") != "confirm":
        await callback.answer("Phiên nạp tiền đã hết hạn.", show_alert=True)
        return
    target_username = str(session.get("target_username", ""))
    target_user_id = int(session.get("target_user_id", 0))
    amount = int(session.get("amount", 0))
    if not target_username or target_user_id <= 0 or amount <= 0:
        _manual_topup_sessions.pop(admin_id, None)
        await callback.answer("Dữ liệu không hợp lệ.", show_alert=True)
        return

    await add_balance(config.db_path, target_user_id, amount)
    _manual_topup_sessions.pop(admin_id, None)

    await _edit_or_send(
        callback,
        "✅ <b>NẠP TIỀN THÀNH CÔNG</b>\n\n"
        f"User: <code>@{target_username}</code>\n"
        f"User ID: <code>{target_user_id}</code>\n"
        f"Số tiền đã nạp: <b>{amount:,} ₫</b>",
    )

    await callback.bot.send_message(
        target_user_id,
        "✅ <b>TÀI KHOẢN ĐÃ ĐƯỢC NẠP TIỀN</b>\n\n"
        f"Số tiền: <b>{amount:,} ₫</b>\n"
        "Bạn có thể dùng số dư ngay bây giờ.",
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "admin:wallet_check:start")
async def admin_wallet_check_start(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    admin_id = callback.from_user.id
    _manual_topup_sessions.pop(admin_id, None)
    _wallet_check_sessions.add(admin_id)
    await _edit_or_send(
        callback,
        "💳 <b>CHECK VÍ USER</b>\n\n"
        "Nhập <b>@username</b> hoặc <b>user_id</b> để kiểm tra số dư.",
    )


@router.message(
    lambda m: m.from_user is not None
    and m.from_user.id in _wallet_check_sessions
    and m.text is not None
)
async def admin_wallet_check_input(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        return
    admin_id = message.from_user.id
    raw_text = message.text.strip()
    if raw_text == "" or raw_text.startswith("/"):
        return

    user_id: int | None = None
    if raw_text.lstrip("-").isdigit():
        try:
            user_id = int(raw_text)
        except ValueError:
            user_id = None
    else:
        user_id = await get_user_id_by_username(config.db_path, raw_text)

    if user_id is None or user_id <= 0:
        await message.answer(
            "Không tìm thấy user. Nhập lại <code>@username</code> hoặc <code>user_id</code>.",
            parse_mode="HTML",
        )
        return

    wallet = await get_user_wallet(config.db_path, user_id)
    if wallet is None:
        await message.answer("User chưa có dữ liệu ví trong bot.", parse_mode="HTML")
        return

    username_raw = wallet["username"] if wallet["username"] else ""
    username_display = f"@{username_raw}" if username_raw else "chưa có"
    balance = int(wallet["balance"])
    _wallet_check_sessions.discard(admin_id)
    await message.answer(
        "💳 <b>THÔNG TIN VÍ USER</b>\n\n"
        f"User ID: <code>{wallet['user_id']}</code>\n"
        f"Username: <code>{username_display}</code>\n"
        f"Số dư: <b>{balance:,} ₫</b>",
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "admin:users:list")
async def admin_users_list(callback: CallbackQuery, config: Config) -> None:
    if callback.from_user is None or not _is_admin(config, callback.from_user.id):
        await callback.answer("Không có quyền", show_alert=True)
        return
    users = await list_users_brief(config.db_path)
    if not users:
        await _edit_or_send(callback, "Chưa có user nào bấm <code>/start</code>.", reply_markup=None)
        return

    header = f"👥 <b>DANH SÁCH USER ĐÃ /START</b>\nTổng: <b>{len(users)}</b>\n\n"
    lines = []
    for idx, u in enumerate(users, start=1):
        username = f"@{u['username']}" if u["username"] else "(chưa có username)"
        lines.append(f"{idx}. {username} | <code>{u['user_id']}</code>")

    chunks: list[str] = []
    current = header
    for line in lines:
        if len(current) + len(line) + 1 > 3900:
            chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current)

    await _edit_or_send(callback, chunks[0], reply_markup=None)
    for extra in chunks[1:]:
        await callback.message.answer(extra, parse_mode="HTML")


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
