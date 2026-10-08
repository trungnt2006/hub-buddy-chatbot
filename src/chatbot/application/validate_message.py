"""Kiểm tra nội dung tin nhắn theo B5."""
from __future__ import annotations

from src.chatbot.domain.errors import InvalidMessage

MAX_LENGTH = 4000


def validate_message(text: object) -> str:
    if not isinstance(text, str):
        raise InvalidMessage("Nội dung tin phải là chuỗi ký tự")
    trimmed = text.strip()
    if not trimmed:
        raise InvalidMessage("Nội dung tin không được rỗng")
    if len(trimmed) > MAX_LENGTH:
        raise InvalidMessage(f"Nội dung tin dài quá {MAX_LENGTH} ký tự")
    return trimmed
