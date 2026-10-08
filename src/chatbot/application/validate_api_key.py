"""Kiểm tra hình thức khóa API, KHÔNG kiểm tiền tố nhà cung cấp."""
from __future__ import annotations

from src.chatbot.domain.errors import InvalidApiKey

MIN_LENGTH = 20
MAX_LENGTH = 200


def validate_api_key(api_key: object) -> str:
    if not isinstance(api_key, str):
        raise InvalidApiKey("Khóa API phải là chuỗi ký tự")
    trimmed = api_key.strip()
    if not MIN_LENGTH <= len(trimmed) <= MAX_LENGTH:
        raise InvalidApiKey(f"Khóa API phải dài {MIN_LENGTH} đến {MAX_LENGTH} ký tự")
    for ch in trimmed:
        if ch.isspace():
            raise InvalidApiKey("Khóa API không được chứa khoảng trắng bên trong")
        if not 33 <= ord(ch) <= 126:
            raise InvalidApiKey("Khóa API chỉ được dùng ký tự ASCII in được")
    return trimmed
