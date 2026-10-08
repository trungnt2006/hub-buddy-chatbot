"""Use case gửi một tin và trả lời của mô hình."""
from __future__ import annotations

from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import ApiKeyMissing, UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.domain.trim_history import trim_history

EMPTY_REPLY_MESSAGE = "Mô hình trả về nội dung rỗng"


def send_message(
    repo: MemoryRepository,
    model: ChatModel,
    store: ApiKeyStore,
    system_prompt: str,
    max_messages: int,
    session_id: str,
    text: str,
) -> str:
    sid = validate_session_id(session_id)
    msg = validate_message(text)
    if not store.is_configured():
        raise ApiKeyMissing("Chưa cấu hình khóa API, hãy nhập khóa ở hộp thoại")
    history = repo.get(sid)
    if history:
        history = trim_history(history, max_messages)
    reply = model.reply(system_prompt, history, msg)
    if not isinstance(reply, str) or not reply.strip():
        raise UpstreamError(502, EMPTY_REPLY_MESSAGE)
    reply = reply.strip()
    repo.append(sid, [Message(role="human", content=msg), Message(role="ai", content=reply)])
    return reply
