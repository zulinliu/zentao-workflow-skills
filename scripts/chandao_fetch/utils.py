#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道下载工具公共工具函数。
"""

import re
from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlparse


INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]'


def sanitize_filename(name: str, fallback: str = "unnamed", max_length: int = 80) -> str:
    """清理文件名，兼容 Windows/macOS/Linux。"""
    candidate = unquote((name or "").strip())
    candidate = Path(candidate).name
    candidate = candidate.replace("\r", " ").replace("\n", " ")
    candidate = re.sub(INVALID_FILENAME_CHARS, "_", candidate)
    candidate = re.sub(r"\s+", " ", candidate).strip().rstrip(". ")

    if not candidate:
        return fallback

    if len(candidate) > max_length:
        candidate = candidate[:max_length].rstrip(". ")

    return candidate or fallback


def filename_from_url(url: str, fallback: str = "file") -> str:
    """从 URL 中提取安全文件名。"""
    parsed = urlparse(url or "")
    return sanitize_filename(Path(parsed.path).name, fallback=fallback)


def has_visible_text(content: str) -> bool:
    """判断 HTML/文本内容是否包含可见字符。"""
    if not content:
        return False

    text = re.sub(r"<[^>]+>", " ", content)
    text = unescape(text).replace("\xa0", " ")
    return bool(text.strip())
