"""Kiểm thử send_message bằng bản giả, không gọi mô hình thật."""
import pytest

from src.chatbot.application.send_message import EMPTY_REPLY_MESSAGE, send_message
from src.chatbot.domain.errors import ApiKeyMissing, ChatbotError, UpstreamError
from src.chatbot.domain.errors import InvalidSession
from src.chatbot.domain.message import Message
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository

KEY = "TEST_KEY_xxxxxxxxxxxxxxxxxxxx"
SID = "sess-2026a"
SYSTEM = "Bạn là trợ lý giảng dạng, trả lời bằng tiếng Việt."


def _go(repo, model, store=None, limit=5, session_id=SID, text="Xin chào"):
    used = store if store is not None else FakeApiKeyStore(api_key=KEY)
    return send_message(repo, model, used, SYSTEM, limit, session_id, text)


def _history(count):
    return [Message(role=("human", "ai")[i % 2], content=f"t{i}") for i in range(count)]


def test_send_message_thanh_congh():
    repo = FakeMemoryRepository()
    model = FakeChatModel(reply_text="Chào bạn!")
    assert _go(repo, model) == "Chào bạn!"
    assert [m.role for m in repo.data[SID]] == ["human", "ai"]
    assert repo.data[SID][0].content == "Xin chào"
    assert model.seen_user_text == "Xin chào"
    assert model.seen_system_prompt == SYSTEM


def test_send_message_loi_model_khong_ghi_bo_nho():
    repo = FakeMemoryRepository()
    with pytest.raises(UpstreamError):
        _go(repo, FakeChatModel(raise_upstream=True))
    assert repo.methods_called() == ["get"]
    assert repo.data == {}


def test_send_message_thieu_khoa_kiem_truoc_khi_doc_bo_nho():
    repo = FakeMemoryRepository()
    model = FakeChatModel()
    with pytest.raises(ApiKeyMissing):
        _go(repo, model, FakeApiKeyStore(api_key=""))
    assert (repo.calls, model.call_count) == ([], 0)


def test_send_message_cat_lich_su_con_5():
    model = FakeChatModel()
    _go(FakeMemoryRepository({SID: _history(12)}), model, limit=5)
    assert [m.content for m in model.seen_history] == ["t7", "t8", "t9", "t10", "t11"]


def test_send_message_lich_su_rong_khong_goi_cat():
    model = FakeChatModel()
    _go(FakeMemoryRepository(), model, limit=0)
    assert model.seen_history == []


def test_send_message_model_tra_chuoi_rong():
    repo = FakeMemoryRepository()
    with pytest.raises(UpstreamError) as info:
        _go(repo, FakeChatModel(reply_text="   "))
    assert (info.value.status, info.value.message) == (502, EMPTY_REPLY_MESSAGE)
    assert "append" not in repo.methods_called()


def test_send_message_session_xau_khong_goi_repo():
    repo = FakeMemoryRepository()
    with pytest.raises(InvalidSession):
        _go(repo, FakeChatModel(), FakeApiKeyStore(api_key=""), session_id="sai!")
    assert repo.calls == []


def test_send_message_loi_append_lan_len():
    repo = FakeMemoryRepository(fail_on_append=True)
    model = FakeChatModel()
    with pytest.raises(ChatbotError):
        _go(repo, model)
    assert (model.call_count, "append" in repo.methods_called()) == (1, True)
