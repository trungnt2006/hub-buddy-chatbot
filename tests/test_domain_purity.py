from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "src" / "chatbot" / "domain"
BANNED = ("flask", "langchain", "openai", "dotenv", "os", "pathlib", "json")


def _domain_files():
    if not DOMAIN.is_dir():
        return []
    return [p for p in sorted(DOMAIN.rglob("*.py")) if p.name != "__init__.py"]


def _read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def _imported_roots(line):
    text = line.strip()
    if text.startswith("import "):
        return [part.strip().split(".")[0] for part in text[len("import "):].split(",")]
    if text.startswith("from "):
        head = text[len("from "):].split(" import ")[0]
        return [head.lstrip(".").split(".")[0]]
    return []


def _offenders():
    found = []
    for path in _domain_files():
        for number, line in enumerate(_read(path).splitlines(), 1):
            for name in _imported_roots(line):
                if name in BANNED:
                    found.append(f"{path.relative_to(ROOT).as_posix()}:{number}:{name}")
    return found


def test_domain_directory_exists():
    assert DOMAIN.is_dir()


def test_import_roots_parser_flags_banned_module():
    assert _imported_roots("import os") == ["os"]


def test_import_roots_parser_reads_relative_import():
    assert _imported_roots("from .ports.memory_repository import MemoryRepository") == ["ports"]


def test_import_roots_parser_ignores_plain_line():
    assert _imported_roots("x = 1") == []


def test_domain_has_no_framework_import():
    assert _offenders() == []
