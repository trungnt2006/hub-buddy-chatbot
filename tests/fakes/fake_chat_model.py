"""Bản giả ChatModel, ghi nhận lời gọi và cho phép bơm lỗi."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.chatbot.domain.errors import UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.chat_model import ChatModel


@dataclass
class FakeChatModel(ChatModel):
    reply_text: str = "trả lời giả lập"
    seen_system_prompt: str = ""
    seen_history: list[Message] = field(default_factory=list)
    seen_user_text: str = ""
    call_count: int = 0
    raise_upstream: bool = False
    error: Exception | None = None

    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        self.call_count += 1
        self.seen_system_prompt = system_prompt
        self.seen_history = list(history)
        self.seen_user_text = user_text
        if self.error is not None:
            raise self.error
        if self.raise_upstream:
            raise UpstreamError(503, "Mô hình giả lập đang quá tải")
        return self.reply_text
