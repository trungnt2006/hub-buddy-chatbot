"""Xóa lịch sử của đúng một phiên."""
from __future__ import annotations

from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.ports.memory_repository import MemoryRepository


def reset_conversation(repo: MemoryRepository, session_id: object) -> None:
    repo.reset(validate_session_id(session_id))
