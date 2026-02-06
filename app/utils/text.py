# -*- coding: utf-8 -*-
from __future__ import annotations

from app.utils.texts.common import join_lines
from app.utils.texts.home import welcome_text, admin_welcome_text
from app.utils.texts.hire import bot_hire_text
from app.utils.texts.guide import guide_text
from app.utils.texts.terms import terms_text
from app.utils.texts.profile import profile_text
from app.utils.texts.services import services_intro_text, service_detail_text, service_order_stub_text
from app.utils.texts.topup import topup_info_text, topup_created_text, topup_rejected_text, topup_approved_text
from app.utils.texts.mem import (
    mem_price_text, mem_foreign_text, pull_mem_text, pull_competitor_text,
    mem_foreign_price_text, mem_foreign_order_check_text, mem_foreign_order_created_text,
    mem_viet_text, mem_viet_price_text, mem_viet_order_check_text, mem_viet_order_created_text,
)

__all__ = [
    "welcome_text",
    "admin_welcome_text",
    "bot_hire_text",
    "guide_text",
    "terms_text",
    "profile_text",
    "services_intro_text",
    "service_detail_text",
    "service_order_stub_text",
    "topup_info_text",
    "topup_created_text",
    "topup_rejected_text",
    "topup_approved_text",
    "mem_price_text",
    "mem_foreign_text",
    "pull_mem_text",
    "pull_competitor_text",
    "mem_foreign_price_text",
    "mem_foreign_order_check_text",
    "mem_foreign_order_created_text",
    "mem_viet_order_check_text",
    "mem_viet_order_created_text",
]
