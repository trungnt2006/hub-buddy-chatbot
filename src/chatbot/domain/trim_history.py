from .message import Message


def trim_history(messages: list[Message], limit: int) -> list[Message]:
    """Trả về `limit` tin CUỐI, giữ nguyên thứ tự, không sửa danh sách vào."""
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("limit phải là số nguyên")
    if limit <= 0:
        raise ValueError("limit phải lớn hơn 0")
    if len(messages) == 0:
        return []
    if len(messages) <= limit:
        return list(messages)
    return list(messages[len(messages) - limit:])
