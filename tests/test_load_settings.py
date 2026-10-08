import os
from pathlib import Path

import pytest

from src.chatbot.config.load_settings import load_settings
from src.chatbot.config.settings import Settings
from src.chatbot.config.settings_error import SettingsError

KEY_20 = "TEST_KEY_" + "x" * 20


def write_env(tmp_path, body):
    path = tmp_path / ".env"
    path.write_bytes(body.encode("utf-8"))
    return path


def test_missing_env_uses_defaults(tmp_path):
    s = load_settings(tmp_path / ".env")
    assert s == Settings()
    assert (s.openai_model, s.host, s.port, s.max_messages) == ("gpt-4o-mini", "127.0.0.1", 2610, 5)
    t = load_settings(write_env(tmp_path, "OPENAI_API_KEY=chu-rac-123\n"))
    assert t.openai_api_key == "chu-rac-123"


def test_reads_all_nine_keys(tmp_path):
    body = (f"OPENAI_API_KEY={KEY_20}\nOPENAI_MODEL=gpt-4o-mini\nOPENAI_TEMPERATURE=1.25\n"
            "OPENAI_TIMEOUT=45\nHOST=localhost\nPORT=8080\nMEMORY_FILE=memory.json\n"
            "MAX_MESSAGES=9\nSYSTEM_PROMPT_FILE=system-prompt.txt\n")
    s = load_settings(write_env(tmp_path, body))
    assert s.openai_api_key == KEY_20 and s.openai_temperature == 1.25
    assert (s.openai_timeout, s.host, s.port, s.max_messages) == (45, "localhost", 8080, 9)
    assert (s.openai_model, s.memory_file, s.system_prompt_file) == ("gpt-4o-mini", "memory.json", "system-prompt.txt")


@pytest.mark.parametrize("raw", ["abc", "2610.5", "80", "70000", "-1"])
def test_port_rejected(tmp_path, raw):
    with pytest.raises(SettingsError) as info:
        load_settings(write_env(tmp_path, f"PORT={raw}\n"))
    assert "PORT" in str(info.value) and "1024" in str(info.value)


@pytest.mark.parametrize("raw", ["0.0.0.0", "192.168.1.5", "0:0:0:0:0:0:0:0"])
def test_host_rejected(tmp_path, raw):
    with pytest.raises(SettingsError) as info:
        load_settings(write_env(tmp_path, f"HOST={raw}\n"))
    assert "HOST" in str(info.value) and "127.0.0.1" in str(info.value)


@pytest.mark.parametrize("raw", ["2.5", "-0.1", "abc", "nan", "inf"])
def test_temperature_rejected(tmp_path, raw):
    with pytest.raises(SettingsError) as info:
        load_settings(write_env(tmp_path, f"OPENAI_TEMPERATURE={raw}\n"))
    assert "OPENAI_TEMPERATURE" in str(info.value) and "2.0" in str(info.value)


@pytest.mark.parametrize("key, raw", [("OPENAI_TIMEOUT", "0"), ("OPENAI_TIMEOUT", "301"),
                                      ("OPENAI_TIMEOUT", "thirty"), ("MAX_MESSAGES", "0"),
                                      ("MAX_MESSAGES", "51"), ("MAX_MESSAGES", "năm")])
def test_integer_range_rejected(tmp_path, key, raw):
    with pytest.raises(SettingsError) as info:
        load_settings(write_env(tmp_path, f"{key}={raw}\n"))
    assert key in str(info.value)


def test_boundaries_accepted(tmp_path):
    low = "PORT=1024\nOPENAI_TEMPERATURE=0.0\nOPENAI_TIMEOUT=1\nMAX_MESSAGES=1\n"
    high = "PORT=65535\nOPENAI_TEMPERATURE=2.0\nOPENAI_TIMEOUT=300\nMAX_MESSAGES=50\n"
    a, b = (load_settings(write_env(tmp_path, x)) for x in (low, high))
    assert (a.port, b.port, a.max_messages, b.max_messages) == (1024, 65535, 1, 50)
    assert (a.openai_temperature, b.openai_temperature) == (0.0, 2.0)
    assert (a.openai_timeout, b.openai_timeout) == (1, 300)


def test_error_message_never_contains_key(tmp_path):
    with pytest.raises(SettingsError) as info:
        load_settings(write_env(tmp_path, f"OPENAI_API_KEY={KEY_20}\nPORT=80\n"))
    assert KEY_20 not in str(info.value) and "xxxx" not in str(info.value)


def test_comments_quotes_spaces_ignored(tmp_path):
    body = "# ghi chu\n\n \nOPENAI_MODEL=\"gpt-4o-mini\"\nOPENAI_TIMEOUT = 30 \n"
    s = load_settings(write_env(tmp_path, body))
    assert (s.openai_model, s.openai_timeout) == ("gpt-4o-mini", 30)
    blank = "OPENAI_API_KEY=\nMEMORY_FILE=  \nSYSTEM_PROMPT_FILE=\n"
    t = load_settings(write_env(tmp_path, blank))
    assert (t.openai_api_key, t.memory_file, t.system_prompt_file) == ("", "memory.json", "system-prompt.txt")


def test_crlf_bom_and_duplicate_key(tmp_path):
    body = "\ufeff# ghi chu\r\nOPENAI_MODEL=ten-sai\r\nOPENAI_MODEL=gpt-4o-mini\r\nPORT=2610\r\n"
    s = load_settings(write_env(tmp_path, body))
    assert (s.openai_model, s.port) == ("gpt-4o-mini", 2610)


def test_does_not_mutate_os_environ(tmp_path):
    before = dict(os.environ)
    load_settings(write_env(tmp_path, "PORT=8080\nHOST=localhost\n"))
    assert dict(os.environ) == before
