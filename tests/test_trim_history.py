import pytest

from src.chatbot.domain.errors import (
    ApiKeyMissing,
    ChatbotError,
    InvalidApiKey,
    InvalidMessage,
    InvalidSession,
    UpstreamError,
)
from src.chatbot.domain.message import Message
from src.chatbot.domain.trim_history import trim_history


def tao_tin(so):
    return [Message("human", f"tin {i}") for i in range(so)]


@pytest.mark.parametrize("vao, ra", [(0, 0), (1, 1), (5, 5), (6, 5), (12, 5)])
def test_trim_theo_so_luong(vao, ra):
    assert len(trim_history(tao_tin(vao), 5)) == ra


def test_trim_giu_thu_tu():
    ket_qua = trim_history(tao_tin(6), 5)
    assert [m.content for m in ket_qua] == ["tin 1", "tin 2", "tin 3", "tin 4", "tin 5"]


def test_trim_limit_khong_duong():
    with pytest.raises(ValueError):
        trim_history(tao_tin(3), 0)
    with pytest.raises(ValueError):
        trim_history(tao_tin(3), -2)


def test_trim_khong_sua_danh_sach_vao():
    danh_sach = tao_tin(6)
    truoc = [(m.role, m.content) for m in danh_sach]
    trim_history(danh_sach, 5)
    assert [(m.role, m.content) for m in danh_sach] == truoc


def test_trim_tra_lien_tuc_moi():
    danh_sach = tao_tin(6)
    ket_qua = trim_history(danh_sach, 5)
    assert ket_qua == danh_sach[1:]
    assert ket_qua is not danh_sach


def test_message_role_la():
    for role in ("bot", "system", "user", "assistant", "Human", ""):
        with pytest.raises(ValueError):
            Message(role, "xin chào")


def test_message_content_rong():
    for content in ("", "   ", "\n\t "):
        with pytest.raises(ValueError):
            Message("human", content)


def test_message_dong_bang():
    tin = Message("ai", "chào bạn")
    with pytest.raises(Exception):
        tin.role = "human"
    assert tin.role == "ai"


def test_loi_ke_thua_chatbot_error():
    for loi in (ApiKeyMissing, InvalidApiKey, InvalidMessage, InvalidSession):
        assert issubclass(loi, ChatbotError)
    assert issubclass(ChatbotError, Exception)
    loi = UpstreamError(503, "Hệ thống đang quá tải, thử lại sau")
    assert loi.status == 503
    assert loi.message == "Hệ thống đang quá tải, thử lại sau"
