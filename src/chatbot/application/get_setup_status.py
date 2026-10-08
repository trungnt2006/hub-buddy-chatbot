"""Trả trạng thái đã cấu hình khóa API hay chưa."""
from __future__ import annotations

from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def get_setup_status(store: ApiKeyStore) -> dict[str, bool]:
    return {"configured": store.is_configured()}
