import json
from pathlib import Path

from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


def atomic_write_json(path: Path, data: object) -> None:
    van_ban = json.dumps(data, ensure_ascii=False, indent=2)
    atomic_write_text(path, van_ban)
