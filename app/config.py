# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


def _parse_admin_ids(raw: str | None) -> List[int]:
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    ids: List[int] = []
    for p in parts:
        try:
            ids.append(int(p))
        except ValueError:
            continue
    return ids


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: List[int]
    db_path: str
    sepay_api_key: str
    sepay_bank_name: str
    sepay_account_number: str
    sepay_account_name: str
    sepay_webhook_port: int
    sepay_group_id: int
    welcome_gif_id: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS"))
    db_path = os.getenv("DB_PATH", "./bot.sqlite3").strip()
    sepay_api_key = os.getenv("SEPAY_API_KEY", "").strip()
    sepay_bank_name = os.getenv("SEPAY_BANK_NAME", "").strip()
    sepay_account_number = os.getenv("SEPAY_ACCOUNT_NUMBER", "").strip()
    sepay_account_name = os.getenv("SEPAY_ACCOUNT_NAME", "").strip()
    sepay_webhook_port = int(os.getenv("SEPAY_WEBHOOK_PORT", "8080").strip() or "8080")
    sepay_group_id = int(os.getenv("SEPAY_GROUP_ID", "0").strip() or "0")
    welcome_gif_id = os.getenv("WELCOME_GIF_ID", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is required")
    return Config(
        bot_token=bot_token,
        admin_ids=admin_ids,
        db_path=db_path,
        sepay_api_key=sepay_api_key,
        sepay_bank_name=sepay_bank_name,
        sepay_account_number=sepay_account_number,
        sepay_account_name=sepay_account_name,
        sepay_webhook_port=sepay_webhook_port,
        sepay_group_id=sepay_group_id,
        welcome_gif_id=welcome_gif_id,
    )
