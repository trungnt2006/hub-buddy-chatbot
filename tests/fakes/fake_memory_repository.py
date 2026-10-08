"""Bản giả MemoryRepository cho tầng application."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.chatbot.domain.errors import ChatbotError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository


@dataclass
class FakeMemoryRepository(MemoryRepository):
    data: dict[str, list[Message]] = field(default_factory=dict)
    calls: list[tuple[str, str]] = field(default_factory=list)
    fail_on_append: bool = False

    def get(self, session_id: str) -> list[Message]:
        self.calls.append(("get", session_id))
        return list(self.data.get(session_id, []))

    def append(self, session_id: str, messages: list[Message]) -> None:
        self.calls.append(("append", session_id))
        if self.fail_on_append:
            raise ChatbotError("append bị lỗi giả lập")
        self.data.setdefault(session_id, []).extend(messages)

    def reset(self, session_id: str) -> None:
        self.calls.append(("reset", session_id))
        self.data.pop(session_id, None)

    def methods_called(self) -> list[str]:
        return [name for name, _ in self.calls]
