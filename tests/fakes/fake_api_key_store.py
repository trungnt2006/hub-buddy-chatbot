"""Bản giả ApiKeyStore, lưu khóa trong bộ nhớ tiến trình."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.chatbot.domain.ports.api_key_store import ApiKeyStore


@dataclass
class FakeApiKeyStore(ApiKeyStore):
    api_key: str = ""
    key: str = ""
    saved: list[str] = field(default_factory=list)
    fail_on_save: bool = False

    def __post_init__(self):
        if self.key and not self.api_key:
            self.api_key = self.key

    def is_configured(self) -> bool:
        return self.api_key.strip() != ""

    def get(self) -> str:
        return self.api_key

    def save(self, api_key: str) -> None:
        if self.fail_on_save:
            raise OSError("không ghi được tệp .env trong bản giả")
        self.api_key = api_key
        self.key = api_key
        self.saved.append(api_key)
