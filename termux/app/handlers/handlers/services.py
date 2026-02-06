# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.services import SERVICE_ITEMS, service_detail_keyboard, services_list_keyboard
from app.keyboards.common import back_home_keyboard
from app.utils.text import service_detail_text, services_intro_text, service_order_stub_text

router = Router()


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


@router.callback_query(lambda c: c.data == "services:list")
async def services_list_callback(callback: CallbackQuery) -> None:
    await _edit_or_send(callback, services_intro_text(), reply_markup=services_list_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("services:detail:"))
async def service_detail_callback(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 2)[2]
    item = SERVICE_ITEMS.get(key)
    if not item:
        await _edit_or_send(callback, "Dịch vụ không tồn tại.", reply_markup=back_home_keyboard())
        return
    text = service_detail_text(item["title"], item["price"], item["desc"])
    await _edit_or_send(callback, text, reply_markup=service_detail_keyboard(key))


@router.callback_query(lambda c: c.data and c.data.startswith("services:order:"))
async def service_order_callback(callback: CallbackQuery) -> None:
    await _edit_or_send(callback, service_order_stub_text(), reply_markup=services_list_keyboard())
