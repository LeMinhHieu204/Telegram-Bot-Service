# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import os
import re
from typing import Any, Iterable

from aiohttp import ClientSession
from dotenv import load_dotenv
from aiogram import Bot

from app.config import load_config
from app.db.sepay_polling import get_state, set_state
from app.db.topups import get_topup_by_note, list_pending_topups, set_topup_status
from app.db.users import add_balance
from app.utils.text import topup_approved_text


NOTE_PATTERN = re.compile(r"(NAP\d+-\d+-\d+)")


def _extract_note(text: str) -> str:
    match = NOTE_PATTERN.search(text)
    if match:
        return match.group(1)
    fallback = re.search(r"(NAP\d+)", text)
    if fallback:
        return fallback.group(1)
    return ""


def _normalize_note(raw: str) -> str:
    digits = "".join(ch for ch in raw if ch.isdigit())
    return f"NAP{digits}" if digits else ""


async def _resolve_topup(db_path: str, note: str) -> dict | None:
    topup = await get_topup_by_note(db_path, note)
    if topup:
        return topup
    normalized = _normalize_note(note)
    if not normalized:
        return None
    for pending in await list_pending_topups(db_path):
        if _normalize_note(str(pending.get("note", ""))) == normalized:
            return pending
    return None


def _iter_transactions(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for key in ("data", "transactions", "items", "rows"):
        val = payload.get(key)
        if isinstance(val, list):
            return val
        if isinstance(val, dict) and isinstance(val.get("items"), list):
            return val.get("items", [])
    if isinstance(payload, list):
        return payload
    return []


def _tx_id(tx: dict[str, Any]) -> int:
    for key in ("id", "transaction_id", "sepay_id"):
        if key in tx:
            try:
                return int(tx[key])
            except (TypeError, ValueError):
                continue
    return 0


def _tx_amount(tx: dict[str, Any]) -> int:
    for key in ("amount_in", "amount", "transferAmount", "value"):
        if key in tx:
            try:
                return int(float(tx[key]))
            except (TypeError, ValueError):
                continue
    return 0


def _tx_is_incoming(tx: dict[str, Any]) -> bool:
    amount_in = tx.get("amount_in")
    if amount_in is not None:
        try:
            return float(amount_in) > 0
        except (TypeError, ValueError):
            pass
    for key in ("transferType", "type", "direction"):
        val = str(tx.get(key, "")).lower()
        if val in {"in", "credit", "incoming"}:
            return True
        if val in {"out", "debit", "outgoing"}:
            return False
    return _tx_amount(tx) > 0


def _tx_content(tx: dict[str, Any]) -> str:
    for key in ("transaction_content", "content", "description", "note", "transactionContent"):
        val = tx.get(key)
        if isinstance(val, str):
            return val
    return ""


async def _poll_once(session: ClientSession, base_url: str, path: str, token: str) -> list[dict[str, Any]]:
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    headers = {"Authorization": f"Bearer {token}"}
    async with session.get(url, headers=headers) as resp:
        payload = await resp.json()
    return list(_iter_transactions(payload))


async def _fetch_details(session: ClientSession, base_url: str, token: str, tx_id: int) -> dict[str, Any] | None:
    url = base_url.rstrip("/") + f"/userapi/transactions/details/{tx_id}"
    headers = {"Authorization": f"Bearer {token}"}
    async with session.get(url, headers=headers) as resp:
        payload = await resp.json()
    tx = payload.get("transaction")
    if isinstance(tx, dict):
        return tx
    return None


async def run_polling() -> None:
    load_dotenv()
    config = load_config()
    token = os.getenv("SEPAY_API_TOKEN", "").strip()
    base_url = os.getenv("SEPAY_API_BASE", "https://my.sepay.vn").strip() or "https://my.sepay.vn"
    path = os.getenv("SEPAY_API_PATH", "/userapi/transactions/list").strip() or "/userapi/transactions/list"
    interval = int(os.getenv("SEPAY_POLL_INTERVAL", "60").strip() or "60")
    if not token:
        print("[sepay_polling] SEPAY_API_TOKEN missing, polling disabled")
        return

    last_id_raw = await get_state(config.db_path, "sepay_last_id")
    try:
        last_id = int(last_id_raw) if last_id_raw else 0
    except ValueError:
        last_id = 0

    print(f"[sepay_polling] start interval={interval}s base={base_url} path={path} last_id={last_id}")
    async with ClientSession() as session:
        while True:
            try:
                txs = await _poll_once(session, base_url, path, token)
                print(f"[sepay_polling] fetched {len(txs)} txs")
                txs.sort(key=_tx_id)
                max_seen = last_id
                for tx in txs:
                    tx_id = _tx_id(tx)
                    if tx_id <= last_id:
                        continue
                    if tx_id > max_seen:
                        max_seen = tx_id
                    detail = await _fetch_details(session, base_url, token, tx_id)
                    if not detail:
                        continue
                    if not _tx_is_incoming(detail):
                        continue
                    note = _extract_note(_tx_content(detail))
                    if not note:
                        continue
                    topup = await _resolve_topup(config.db_path, note)
                    if not topup or topup.get("status") != "pending":
                        continue
                    amount = _tx_amount(detail)
                    if amount and int(topup["amount"]) != amount:
                        continue
                    await add_balance(config.db_path, int(topup["user_id"]), int(topup["amount"]))
                    await set_topup_status(config.db_path, int(topup["id"]), "approved")
                    await Bot(token=config.bot_token).send_message(
                        int(topup["user_id"]),
                        topup_approved_text(topup["note"]),
                        parse_mode="HTML",
                    )
                if max_seen != last_id:
                    last_id = max_seen
                    await set_state(config.db_path, "sepay_last_id", str(last_id))
            except Exception as exc:
                print(f"[sepay_polling] error: {exc}")
            await asyncio.sleep(max(interval, 15))
