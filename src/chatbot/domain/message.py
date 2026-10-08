from dataclasses import dataclass

ROLE_HOP_LE = ("human", "ai")


@dataclass(frozen=True)
class Message:
    """Một tin trong lịch sử trò chuyện: chỉ 'human' hoặc 'ai', nội dung không rỗng."""

    role: str
    content: str

    def __post_init__(self):
        if self.role not in ROLE_HOP_LE:
            raise ValueError(f"role phải là 'human' hoặc 'ai', nhận '{self.role}'")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content không được rỗng hoặc chỉ có khoảng trắng")
