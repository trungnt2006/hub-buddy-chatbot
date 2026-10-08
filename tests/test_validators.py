"""Kiểm thử ba bộ kiểm tra đầu vào của tầng application."""
import pytest

from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import InvalidApiKey, InvalidMessage, InvalidSession

KEY = "TEST_KEY_xxxxxxxxxxxxxxxxxxxx"
BAD_SESSION = ["", "abc1234", "a" * 65, "sess 1234", "sess_1234", "sess.1234",
               "phiên1234", "abc12345\n", 12345678, None]
BAD_KEY = [KEY[:18], KEY + "y" * 180, "TEST_KEY_xxxx xxxxxxxxxxxxxxxx",
           "TEST_KEY_xxxxxxxxxxxxxxxxxxxxđ"]


@pytest.mark.parametrize("sid", ["abc12345", "0" * 8, "a" * 64, "sess-2026-a"])
def test_validate_session_id_hop_le(sid):
    assert validate_session_id(sid) == sid


@pytest.mark.parametrize("sid", BAD_SESSION)
def test_validate_session_id_sai(sid):
    with pytest.raises(InvalidSession):
        validate_session_id(sid)


def test_validate_message_cat_khoang_trang():
    assert validate_message("  Xin chào  ") == "Xin chào"


@pytest.mark.parametrize("text", ["", "   ", "\n\t "])
def test_validate_message_rong(text):
    with pytest.raises(InvalidMessage):
        validate_message(text)


def test_validate_message_do_dai_bien():
    assert validate_message("a" * 4000) == "a" * 4000
    with pytest.raises(InvalidMessage):
        validate_message("a" * 4001)


def test_validate_message_tieng_viet_va_emoji():
    assert validate_message("Tôi tên là Lan, học Python 🌸") == "Tôi tên là Lan, học Python 🌸"


def test_validate_message_ky_tu_html_gi_nguyen_van():
    raw = "<script>alert(1)</script>"
    assert validate_message(raw) == raw


@pytest.mark.parametrize("key", BAD_KEY)
def test_validate_api_key_sai_hinh_thuc(key):
    with pytest.raises(InvalidApiKey):
        validate_api_key(key)


def test_validate_api_key_hop_le():
    assert validate_api_key(f"  {KEY}\n") == KEY


def test_validate_api_key_khong_kiem_tien_to():
    plain = "X" * 20
    assert validate_api_key(plain) == plain


def test_validate_api_key_thong_diep_khong_lo_khoa():
    with pytest.raises(InvalidApiKey) as info:
        validate_api_key(KEY + " đ")
    assert KEY not in str(info.value)
