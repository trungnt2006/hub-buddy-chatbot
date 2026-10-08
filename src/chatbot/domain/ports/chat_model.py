import abc

from ..message import Message


class ChatModel(abc.ABC):
    """Cổng gọi dịch vụ mô hình và nhận về một chuỗi trả lời."""

    @abc.abstractmethod
    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        """Trả về nội dung trả lời; lỗi dịch vụ thì ném UpstreamError."""
