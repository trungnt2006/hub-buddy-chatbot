import json
import threading
import time
from pathlib import Path

from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.infrastructure.atomic_write_json import atomic_write_json


class JsonMemoryRepository(MemoryRepository):
    def __init__(self, path: Path) -> None:
        self._path = Path(path)
        self._lock = threading.Lock()

    def _doc_rong(self) -> dict:
        if not self._path.exists():
            return {}
        try:
            raw = self._path.read_text(encoding="utf-8")
            if not raw.strip():
                return {}
            data = json.loads(raw)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            ts = int(time.time())
            corrupt_path = self._path.parent / f"{self._path.name}.corrupt-{ts}"
            try:
                self._path.rename(corrupt_path)
            except OSError:
                pass
            return {}

    def get(self, session_id: str) -> list[Message]:
        with self._lock:
            data = self._doc_rong()
            result = []
            for item in data.get(session_id, []):
                if isinstance(item, dict):
                    role = item.get("role")
                    content = item.get("content")
                    if role in ("human", "ai") and isinstance(content, str) and content.strip():
                        result.append(Message(role=role, content=content))
            return result

    def append(self, session_id: str, messages: list[Message]) -> None:
        with self._lock:
            data = self._doc_rong()
            branch = data.setdefault(session_id, [])
            for m in messages:
                branch.append({"role": m.role, "content": m.content})
            atomic_write_json(self._path, data)

    def reset(self, session_id: str) -> None:
        with self._lock:
            data = self._doc_rong()
            if session_id in data:
                del data[session_id]
                atomic_write_json(self._path, data)
