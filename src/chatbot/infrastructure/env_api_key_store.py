import os
from pathlib import Path

from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text

TEN_KHOA = "OPENAI_API_KEY"


class EnvApiKeyStore(ApiKeyStore):
    def __init__(self, env_path: Path) -> None:
        self._path = Path(env_path)

    @staticmethod
    def _la_dong_khoa(dong: str) -> str | None:
        dong = dong.strip()
        if not dong or dong.startswith("#") or "=" not in dong:
            return None
        ten, _, gia = dong.partition("=")
        if ten.strip() == TEN_KHOA:
            val = gia.strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            return val
        return None

    def _dong_khoa(self) -> str:
        if self._path.exists():
            ket_qua = None
            for dong in self._path.read_text(encoding="utf-8").splitlines():
                gia = self._la_dong_khoa(dong)
                if gia is not None:
                    ket_qua = gia
            if ket_qua is not None:
                return ket_qua
        return os.environ.get(TEN_KHOA, "")

    def get(self) -> str:
        return self._dong_khoa()

    def is_configured(self) -> bool:
        return bool(self.get())

    def save(self, api_key: str) -> None:
        dong_moi = f"{TEN_KHOA}={api_key}"
        danh_sach = []
        thay_the = False
        if self._path.exists():
            for dong in self._path.read_text(encoding="utf-8").splitlines():
                if self._la_dong_khoa(dong) is not None:
                    if not thay_the:
                        danh_sach.append(dong_moi)
                        thay_the = True
                else:
                    danh_sach.append(dong)
        if not thay_the:
            danh_sach.append(dong_moi)
        atomic_write_text(self._path, "\n".join(danh_sach) + "\n")
        os.environ[TEN_KHOA] = api_key
