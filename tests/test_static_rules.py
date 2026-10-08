from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
STATIC = ROOT / "static"
RULE_MARKERS = ("KISS", "DDD", "TDD", "100", ".env", "127.0.0.1", "PowerShell")
PROMPT_ORDER = tuple("P" + str(index) for index in range(10))
SCAN_ROOTS = ("AGENTS.md", "system-prompt.txt", "requirements.txt", "src", "static", "tests")
SUFFIXES = (".py", ".js", ".html", ".md", ".txt")
FORBIDDEN_JS = ("innerHTML", "dangerouslySetInnerHTML")
SECRET_PREFIX = "sk" + "-"
EXPECTED_PATHS = (
    "run.py",
    "requirements.txt",
    "pytest.ini",
    ".env.example",
    "system-prompt.txt",
    "static/index.html",
    "static/js/main.js",
    "src/chatbot/interface/create_app.py",
    "src/chatbot/application/send_message.py",
    "src/chatbot/infrastructure/json_memory_repository.py",
)


def _text(path):
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def _walk(base, suffixes):
    if not base.exists():
        return []
    items = [base] if base.is_file() else sorted(base.rglob("*"))
    return [p for p in items if p.is_file() and (base.is_file() or p.suffix in suffixes)]


def _static_files():
    return _walk(STATIC, (".js", ".html"))


def _oversized(paths):
    return [p.as_posix() for p in paths if len(_text(p).splitlines()) >= 100]


def test_agents_md_exists():
    assert AGENTS.is_file()


def test_agents_md_under_100_lines():
    assert len(_text(AGENTS).splitlines()) < 100


def test_agents_md_has_seven_rule_markers():
    assert [m for m in RULE_MARKERS if m not in _text(AGENTS)] == []


def test_agents_md_lists_ten_prompts_in_order():
    text = _text(AGENTS)
    positions = [text.find(name) for name in PROMPT_ORDER]
    assert all(position >= 0 for position in positions)
    assert positions == sorted(positions)


def test_agents_md_has_no_secret_prefix():
    assert SECRET_PREFIX not in _text(AGENTS)


def test_detector_flags_oversized_file_in_temp_dir(tmp_path):
    sample = tmp_path / "vi-pham.js"
    sample.write_text("const x0;\n" * 120, encoding="utf-8")
    assert _oversized([sample]) == [sample.as_posix()]


def test_static_files_under_100_lines():
    assert _oversized(_static_files()) == []


def test_static_js_has_no_raw_html_injection():
    for path in _static_files():
        if path.suffix == ".js":
            assert [w for w in FORBIDDEN_JS if w in _text(path)] == [], path.as_posix()


def test_no_secret_prefix_in_sources():
    hits = []
    for entry in SCAN_ROOTS:
        for path in _walk(ROOT / entry, SUFFIXES):
            if SECRET_PREFIX in _text(path):
                hits.append(path.relative_to(ROOT).as_posix())
    assert hits == []


def test_expected_paths_present_or_not_started():
    if not (ROOT / "run.py").exists() or not STATIC.is_dir():
        pytest.skip("chưa bắt đầu mốc P1 và mốc P7")
    assert [p for p in EXPECTED_PATHS if not (ROOT / p).exists()] == []
