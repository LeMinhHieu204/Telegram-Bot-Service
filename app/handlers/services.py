# -*- coding: utf-8 -*-
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.services import SERVICE_ITEMS, service_detail_keyboard, services_list_keyboard
from app.keyboards.common import back_home_keyboard
from app.utils.text import service_detail_text, services_intro_text, service_order_stub_text

router = Router()


@router.callback_query(lambda c: c.data == "services:list")
async def services_list_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(services_intro_text(), reply_markup=services_list_keyboard(), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("services:detail:"))
async def service_detail_callback(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 2)[2]
    item = SERVICE_ITEMS.get(key)
    if not item:
        await callback.message.edit_text("Dịch vụ không tồn tại.", reply_markup=back_home_keyboard())
        return
    text = service_detail_text(item["title"], item["price"], item["desc"])
    await callback.message.edit_text(text, reply_markup=service_detail_keyboard(key), parse_mode="HTML")


@router.callback_query(lambda c: c.data and c.data.startswith("services:order:"))
async def service_order_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(service_order_stub_text(), reply_markup=services_list_keyboard(), parse_mode="HTML")
