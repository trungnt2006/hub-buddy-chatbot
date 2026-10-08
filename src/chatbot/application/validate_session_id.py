"""Kiểm tra mã phiên theo biểu thức chính quy ở B5."""
from __future__ import annotations

import re

from src.chatbot.domain.errors import InvalidSession

PATTERN = re.compile(r"[A-Za-z0-9-]{8,64}")


def validate_session_id(session_id: object) -> str:
    if not isinstance(session_id, str):
        raise InvalidSession("Mã phiên phải là chuỗi ký tự")
    if PATTERN.fullmatch(session_id) is None:
        raise InvalidSession(
            "Mã phiên phải gồm 8 đến 64 ký tự a-z, A-Z, số hoặc dấu gạch ngang"
        )
    return session_id
