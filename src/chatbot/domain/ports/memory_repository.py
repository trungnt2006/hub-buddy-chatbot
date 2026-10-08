import abc

from ..message import Message


class MemoryRepository(abc.ABC):
    """Cổng lưu lịch sử trò chuyện theo session_id."""

    @abc.abstractmethod
    def get(self, session_id: str) -> list[Message]:
        """Trả về toàn bộ tin của phiên, danh sách rỗng nếu phiên chưa tồn tại."""

    @abc.abstractmethod
    def append(self, session_id: str, messages: list[Message]) -> None:
        """Nối thêm tin vào cuối phiên."""

    @abc.abstractmethod
    def reset(self, session_id: str) -> None:
        """Xoá phiên; phiên chưa tồn tại vẫn là thành công im lặng."""
