# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Any

from aiohttp import web

from app.config import Config
from app.db.topups import get_topup_by_note, record_sepay_webhook, set_topup_status
from app.db.users import add_balance
from app.utils.text import topup_approved_text


NOTE_PATTERN = re.compile(r"(NAP\d+-\d+-\d+)")


def _auth_ok(request: web.Request, api_key: str) -> bool:
    if not api_key:
        return True
    auth = (request.headers.get("Authorization") or "").strip()
    if not auth:
        return False
    normalized = auth.replace("APIkey", "").replace("ApiKey", "").replace("APIKEY", "").strip()
    return normalized == api_key


def _extract_note(payload: dict[str, Any]) -> str:
    for field in ("content", "description", "note"):
        value = payload.get(field)
        if isinstance(value, str):
            match = NOTE_PATTERN.search(value)
            if match:
                return match.group(1)
    return ""


async def sepay_webhook(request: web.Request) -> web.Response:
    config: Config = request.app["config"]
    bot = request.app["bot"]
    if not _auth_ok(request, config.sepay_api_key):
        return web.json_response({"success": False, "message": "unauthorized"}, status=401)
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"success": False, "message": "invalid json"}, status=400)

    transfer_type = str(payload.get("transferType", "")).lower()
    if transfer_type and transfer_type != "in":
        return web.json_response({"success": True})

    note = _extract_note(payload)
    if not note:
        return web.json_response({"success": True})

    topup = await get_topup_by_note(config.db_path, note)
    if not topup or topup.get("status") != "pending":
        return web.json_response({"success": True})

    try:
        transfer_amount = int(payload.get("transferAmount", 0))
    except (TypeError, ValueError):
        transfer_amount = 0
    if transfer_amount != int(topup["amount"]):
        return web.json_response({"success": True})

    sepay_id_raw = payload.get("id")
    try:
        sepay_id = int(sepay_id_raw)
    except (TypeError, ValueError):
        sepay_id = 0
    if sepay_id:
        inserted = await record_sepay_webhook(
            config.db_path,
            sepay_id,
            str(payload.get("referenceCode", "")),
            note,
        )
        if not inserted:
            return web.json_response({"success": True})

    await add_balance(config.db_path, int(topup["user_id"]), int(topup["amount"]))
    await set_topup_status(config.db_path, int(topup["id"]), "approved")
    await bot.send_message(int(topup["user_id"]), topup_approved_text(note), parse_mode="HTML")

    return web.json_response({"success": True})


def create_sepay_app(bot, config: Config) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app["config"] = config
    app.router.add_post("/sepay/webhook", sepay_webhook)
    return app
