class ChatbotError(Exception):
    """Gốc của mọi lỗi nghiệp vụ của tầng domain."""


class ApiKeyMissing(ChatbotError):
    """Chưa có khóa API trong bộ nhớ tiến trình."""


class InvalidApiKey(ChatbotError):
    """Khóa API sai hình thức."""


class InvalidMessage(ChatbotError):
    """Tin người dùng rỗng hoặc quá dài."""


class InvalidSession(ChatbotError):
    """session_id không khớp mẫu ^[A-Za-z0-9-]{8,64}$."""


class UpstreamError(ChatbotError):
    """Lỗi từ dịch vụ mô hình, mang mã HTTP đã ánh xạ sẵn."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
