from pathlib import Path

MAC_DINH = "Bạn là trợ lý hỏi đáp. Trả lời ngắn gọn bằng tiếng Việt, rõ ràng, thân thiện."


def load_system_prompt(path: Path) -> str:
    try:
        noi_dung = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return MAC_DINH
    noi_dung = noi_dung.strip()
    return noi_dung or MAC_DINH
