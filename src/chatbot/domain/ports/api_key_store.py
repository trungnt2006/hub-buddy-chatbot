import abc


class ApiKeyStore(abc.ABC):
    """Cổng đọc và ghi khóa API, giấu hoàn toàn chi tiết lưu trữ."""

    @abc.abstractmethod
    def is_configured(self) -> bool:
        """Đúng khi đã có khóa khác rỗng."""

    @abc.abstractmethod
    def get(self) -> str:
        """Trả khóa hiện tại, chuỗi rỗng nếu chưa cấu hình."""

    @abc.abstractmethod
    def save(self, api_key: str) -> None:
        """Ghi khóa mới theo cách ghi nguyên tử rồi cập nhật bộ nhớ tiến trình."""
