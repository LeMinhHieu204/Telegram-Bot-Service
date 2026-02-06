from __future__ import annotations


def format_currency_vnd(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + " VND"
