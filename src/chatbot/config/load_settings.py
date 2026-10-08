import math
from pathlib import Path

from dotenv import dotenv_values

from src.chatbot.config.settings import (
    DEFAULT_HOST, DEFAULT_MAX_MESSAGES, DEFAULT_MEMORY_FILE,
    DEFAULT_OPENAI_MODEL, DEFAULT_OPENAI_TEMPERATURE,
    DEFAULT_OPENAI_TIMEOUT, DEFAULT_PORT,
    DEFAULT_SYSTEM_PROMPT_FILE, Settings,
)
from src.chatbot.config.settings_error import SettingsError

ALLOWED_HOSTS = ("127.0.0.1", "localhost")


def load_settings(env_path: Path) -> Settings:
    """PRE: env_path là đường dẫn tệp .env, được phép không tồn tại.
    POST: trả về Settings đóng băng đúng chín trường ở B3.
    INV: không ghi os.environ; thông điệp lỗi không chứa giá trị khóa API."""
    raw = dotenv_values(env_path, encoding="utf-8-sig") if env_path.exists() else {}
    host = _text(raw, "HOST", DEFAULT_HOST)
    if host not in ALLOWED_HOSTS:
        raise SettingsError("HOST phải là 127.0.0.1 hoặc localhost, không được dùng địa chỉ khác")
    return Settings(
        openai_api_key=_text(raw, "OPENAI_API_KEY", ""),
        openai_model=_text(raw, "OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        openai_temperature=_number(raw, "OPENAI_TEMPERATURE", DEFAULT_OPENAI_TEMPERATURE, 0.0, 2.0),
        openai_timeout=_integer(raw, "OPENAI_TIMEOUT", DEFAULT_OPENAI_TIMEOUT, 1, 300),
        host=host,
        port=_integer(raw, "PORT", DEFAULT_PORT, 1024, 65535),
        memory_file=_text(raw, "MEMORY_FILE", DEFAULT_MEMORY_FILE),
        max_messages=_integer(raw, "MAX_MESSAGES", DEFAULT_MAX_MESSAGES, 1, 50),
        system_prompt_file=_text(raw, "SYSTEM_PROMPT_FILE", DEFAULT_SYSTEM_PROMPT_FILE),
    )


def _text(raw, key, default):
    """IF thiếu hoặc rỗng sau cắt: RETURN default. ELSE RETURN chuỗi đã cắt."""
    value = raw.get(key)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def _number(raw, key, default, low, high):
    """Parse số thực trong khoảng; sai ký tự, ngoài khoảng hoặc không hữu hạn đều ném lỗi."""
    message = f"{key} phải là số trong khoảng {low} đến {high}"
    text = _text(raw, key, None)
    if text is None:
        return default
    try:
        number = float(text)
    except ValueError:
        raise SettingsError(message) from None
    if not math.isfinite(number) or not low <= number <= high:
        raise SettingsError(message)
    return number


def _integer(raw, key, default, low, high):
    """Parse số nguyên trong khoảng; chữ, số thực, ngoài khoảng đều ném lỗi."""
    message = f"{key} phải là số nguyên trong khoảng {low} đến {high}"
    text = _text(raw, key, None)
    if text is None:
        return default
    if not text.lstrip("+-").isdigit():
        raise SettingsError(message)
    number = int(text)
    if not low <= number <= high:
        raise SettingsError(message)
    return number
