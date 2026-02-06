# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
from wcwidth import wcswidth

from app.utils.icons import (
    SECTION_HEADER,
    SECTION_FOOTER,
    SECTION_HEADER_ENHANCED,
    SECTION_FOOTER_ENHANCED,
)

USE_ASCII_BOX = os.getenv("USE_ASCII_BOX", "").strip() in {"1", "true", "yes", "on"}


def _visible_len(text: str) -> int:
    stripped = re.sub(r"<.*?>", "", text)
    width = wcswidth(stripped)
    return width if width >= 0 else len(stripped)


def _build_box(lines: list[str], style: str) -> str:
    if USE_ASCII_BOX:
        tl, h, tr, v, bl, br = "+", "-", "+", "|", "+", "+"
    elif style == "enhanced":
        tl, h, tr, v, bl, br = "┏", "━", "┓", "┃", "┗", "┛"
    else:
        tl, h, tr, v, bl, br = "┌", "─", "┐", "│", "└", "┘"
    content_width = max((_visible_len(line) for line in lines), default=0)
    inner_width = content_width + 2
    top = tl + (h * inner_width) + tr
    bottom = bl + (h * inner_width) + br
    boxed = []
    for line in lines:
        pad = content_width - _visible_len(line)
        boxed.append(f"{v} {line}{' ' * (pad + 1)}{v}")
    return "\n".join([top, *boxed, bottom])


def box_text(text: str) -> str:
    lines = text.splitlines()
    style = "standard"
    if lines and lines[0] == SECTION_HEADER_ENHANCED:
        style = "enhanced"
        lines = lines[1:]
    elif lines and lines[0] == SECTION_HEADER:
        lines = lines[1:]
    if lines and lines[-1] == SECTION_FOOTER_ENHANCED:
        style = "enhanced"
        lines = lines[:-1]
    elif lines and lines[-1] == SECTION_FOOTER:
        lines = lines[:-1]
    return _build_box(lines, style)


def join_lines(lines: list[str]) -> str:
    # Only frame the section title; keep the rest clean.
    style = "standard"
    if lines and lines[0] == SECTION_HEADER_ENHANCED:
        style = "enhanced"
        lines = lines[1:]
    elif lines and lines[0] == SECTION_HEADER:
        lines = lines[1:]
    if lines and lines[-1] == SECTION_FOOTER_ENHANCED:
        style = "enhanced"
        lines = lines[:-1]
    elif lines and lines[-1] == SECTION_FOOTER:
        lines = lines[:-1]

    title_idx = None
    for i, line in enumerate(lines):
        if line.strip():
            title_idx = i
            break
    if title_idx is None:
        return "\n".join(lines)

    title = lines[title_idx]
    before = lines[:title_idx]
    after = lines[title_idx + 1:]

    boxed_title = _build_box([title], style)
    parts = []
    if before:
        parts.append("\n".join(before))
    parts.append(boxed_title)
    if after:
        parts.append("\n".join(after))
    return "\n".join(parts)
