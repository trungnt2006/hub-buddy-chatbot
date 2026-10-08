"""Kiểm thử use case reset_conversation bằng bản giả."""
import pytest

from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.domain.errors import InvalidSession
from src.chatbot.domain.message import Message
from tests.fakes.fake_memory_repository import FakeMemoryRepository

A = "sess-2026a"
B = "sess-2026b"
BAD_SESSION = ["", "abc", "sess 2026", "sess_2026", "a" * 65]


def _repo() -> FakeMemoryRepository:
    return FakeMemoryRepository(
        {A: [Message(role="human", content="a")], B: [Message(role="human", content="b")]}
    )


def test_reset_xoa_dung_mot_phien():
    repo = _repo()
    reset_conversation(repo, A)
    assert A not in repo.data
    assert B in repo.data
    assert repo.calls == [("reset", A)]


def test_reset_phien_chua_co_thanh_cong_im_lang():
    repo = FakeMemoryRepository()
    reset_conversation(repo, A)
    assert repo.data == {}
    assert repo.calls == [("reset", A)]


@pytest.mark.parametrize("sid", BAD_SESSION)
def test_reset_session_xau_khong_goi_repo(sid):
    repo = _repo()
    with pytest.raises(InvalidSession):
        reset_conversation(repo, sid)
    assert repo.calls == []
    assert A in repo.data


def test_reset_giu_thu_tu_goi():
    repo = FakeMemoryRepository({A: [], B: []})
    reset_conversation(repo, B)
    reset_conversation(repo, A)
    assert repo.calls == [("reset", B), ("reset", A)]
