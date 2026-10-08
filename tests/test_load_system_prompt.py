from pathlib import Path

from src.chatbot.infrastructure.load_system_prompt import load_system_prompt

ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PROMPT_FILE = ROOT / "system-prompt.txt"
REQUIRED_MARKERS = [
    "RCIFENI-O",
    "VAI TRÒ",
    "PHẠM VI",
    "GIỚI HẠN",
    "PHONG CÁCH TRẢ LỜI",
    "KHÔNG ĐƯỢC",
    "LUẬT SUY ĐIỂN",
]
GACH_DAI = chr(8212)
FORBIDDEN_MARKERS = ["OPENAI_API_KEY", "http://", "https://", ".env", "TEST_KEY_"]


def test_tap_thieu_tra_ve_mac_dinh(tmp_path):
    assert "tiếng Việt" in load_system_prompt(tmp_path / "khong_co.txt")


def test_tap_rong_tra_ve_mac_dinh(tmp_path):
    f = tmp_path / "rong.txt"
    f.write_text("   \n", encoding="utf-8")
    assert "tiếng Việt" in load_system_prompt(f)


def test_doc_duoc_tieng_viet_co_dau(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Lan trợ lý học tập.", encoding="utf-8")
    assert load_system_prompt(f) == "Lan trợ lý học tập."


def test_loi_doc_tap_thi_tra_ve_mac_dinh(tmp_path, monkeypatch):
    monkeypatch.setattr(
        Path, "read_text", lambda *a, **k: (_ for _ in ()).throw(OSError)
    )
    assert "tiếng Việt" in load_system_prompt(tmp_path / "x.txt")


def test_system_prompt_file_exists():
    assert SYSTEM_PROMPT_FILE.is_file()


def test_system_prompt_file_has_required_sections():
    doc = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    assert [m for m in REQUIRED_MARKERS if m not in doc] == []


def test_system_prompt_file_is_utf8_with_diacritics():
    doc = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    assert "HUB-Buddy" in doc and "cố vấn học tập" in doc


def test_system_prompt_file_lines_are_short():
    lines = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").splitlines()
    assert 20 <= len(lines) <= 120 and all(len(line) <= 120 for line in lines)


def test_system_prompt_file_has_no_long_dash_or_secret():
    doc = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    assert GACH_DAI not in doc
    assert [m for m in FORBIDDEN_MARKERS if m in doc] == []
