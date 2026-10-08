import os
from pathlib import Path


def atomic_write_text(path: Path, text: str) -> None:
    duong_dan = Path(path)
    thu_muc_cha = duong_dan.parent
    if not thu_muc_cha.exists():
        thu_muc_cha.mkdir(parents=True, exist_ok=True)
    tam = thu_muc_cha / (duong_dan.name + ".tmp")
    try:
        with tam.open("w", encoding="utf-8", newline="\n") as tep:
            tep.write(text)
        os.replace(tam, duong_dan)
    except Exception:
        tam.unlink(missing_ok=True)
        raise
