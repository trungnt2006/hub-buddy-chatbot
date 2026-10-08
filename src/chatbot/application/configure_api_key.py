"""Lưu khóa API sau khi đã kiểm tra hình thức."""
from __future__ import annotations

from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def configure_api_key(store: ApiKeyStore, api_key: object) -> None:
    store.save(validate_api_key(api_key))
