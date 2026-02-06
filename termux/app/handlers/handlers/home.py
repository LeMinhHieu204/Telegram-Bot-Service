# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.config import Config
from app.db.users import get_balance, get_or_create_user
from app.keyboards.home import home_keyboard, admin_home_keyboard
from app.keyboards.common import back_home_keyboard
from app.utils.text import welcome_text, admin_welcome_text, bot_hire_text

router = Router()


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


async def _render_home(message_or_callback: Message | CallbackQuery, config: Config) -> None:
    user = message_or_callback.from_user
    if user is None:
        return
    await get_or_create_user(config.db_path, user.id)
    balance = await get_balance(config.db_path, user.id)
    name = user.full_name or "Unknown"
    is_admin = user.id in config.admin_ids
    if is_admin:
        text = admin_welcome_text(user.id, name)
        keyboard = admin_home_keyboard()
    else:
        text = welcome_text(user.id, name, balance, is_admin=is_admin)
        keyboard = home_keyboard()

    if isinstance(message_or_callback, Message):
        if config.welcome_gif_id:
            await message_or_callback.answer_animation(
                config.welcome_gif_id,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            return
        await message_or_callback.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        msg = message_or_callback.message
        if msg is None:
            return
        if msg.text:
            await msg.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
            return
        if msg.caption is not None:
            await msg.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")
            return
        await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.message(CommandStart())
async def start_handler(message: Message, config: Config) -> None:
    await _render_home(message, config)


@router.message(Command("admin_test"))
async def admin_test_fallback(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        await message.answer("Không có quyền", parse_mode="HTML")
        return
    await message.answer("✅ Admin test: bạn đã nhận được tin nhắn từ bot.", parse_mode="HTML")


@router.message(Command("gifid"))
async def admin_gif_id_fallback(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        await message.answer("Không có quyền", parse_mode="HTML")
        return
    target = message.reply_to_message or message
    if target.animation:
        await message.answer(f"<code>{target.animation.file_id}</code>", parse_mode="HTML")
        return
    if target.video:
        await message.answer(f"<code>{target.video.file_id}</code>", parse_mode="HTML")
        return
    if target.document:
        await message.answer(f"<code>{target.document.file_id}</code>", parse_mode="HTML")
        return
    await message.answer("Hãy reply vào tin nhắn GIF để lấy file_id.", parse_mode="HTML")


@router.message(lambda m: m.animation is not None)
async def admin_gif_id_from_animation(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        return
    await message.answer(f"<code>{message.animation.file_id}</code>", parse_mode="HTML")


@router.message(lambda m: m.video is not None or m.document is not None)
async def admin_gif_id_from_video_doc(message: Message, config: Config) -> None:
    if message.from_user is None or not _is_admin(config, message.from_user.id):
        return
    if message.video:
        await message.answer(f"<code>{message.video.file_id}</code>", parse_mode="HTML")
        return
    if message.document:
        await message.answer(f"<code>{message.document.file_id}</code>", parse_mode="HTML")


@router.callback_query(lambda c: c.data in {"home:show", "home:noop1", "home:noop2", "home:noop3"})
async def home_callback(callback: CallbackQuery, config: Config) -> None:
    await _render_home(callback, config)


@router.callback_query(lambda c: c.data == "bot:hire")
async def bot_hire_callback(callback: CallbackQuery) -> None:
    await _edit_or_send(callback, bot_hire_text(), reply_markup=back_home_keyboard())
