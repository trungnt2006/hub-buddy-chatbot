import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import Runnable

from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import ApiKeyMissing, UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.infrastructure import langchain_chat_model as lc
from src.chatbot.infrastructure.langchain_chat_model import LangChainChatModel

KHOA_MAU = "TEST_KEY_" + "x" * 20
KHOA_HAI = "TEST_KEY_" + "y" * 20
TRANG_THAI = {"loi": None, "noi_dung": "chào bạn", "ban_gia": []}


class StoreGia:
    def __init__(self, gia_tri=""):
        self.gia_tri = gia_tri

    def is_configured(self):
        return bool(self.gia_tri)

    def get(self):
        return self.gia_tri

    def save(self, khoa):
        self.gia_tri = khoa


class ChatOpenAIGia(Runnable):
    def __init__(self, model="", temperature=0.0, timeout=0, api_key="", **kwargs):
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.api_key = api_key
        self.tin_nhan = []

    def invoke(self, input, config=None, **kwargs):
        self.tin_nhan.append(getattr(input, "messages", input))
        if TRANG_THAI["loi"] is not None:
            raise TRANG_THAI["loi"]
        return AIMessage(content=TRANG_THAI["noi_dung"])


def _tao_ban_gia(**th_so):
    ban_gia = ChatOpenAIGia(**th_so)
    TRANG_THAI["ban_gia"].append(ban_gia)
    return ban_gia


def _settings():
    return Settings(openai_api_key="", openai_model="gpt-4o-mini",
                     openai_temperature=0.3, openai_timeout=30,
                     host="127.0.0.1", port=2610, memory_file="memory.json",
                     max_messages=5, system_prompt_file="system-prompt.txt")


@pytest.fixture(autouse=True)
def cai_dat_ban_gia(monkeypatch):
    TRANG_THAI["loi"] = None
    TRANG_THAI["noi_dung"] = "chào bạn"
    TRANG_THAI["ban_gia"] = []
    monkeypatch.setattr(lc, "ChatOpenAI", _tao_ban_gia)


def _model(gia_tri_khoa=KHOA_MAU):
    return LangChainChatModel(_settings(), StoreGia(gia_tri_khoa))


def test_reply_tra_ve_chuoi_noi_dung():
    assert _model().reply("bạn là trợ lý", [], "chào") == "chào bạn"


def test_reply_truyen_dung_tham_so_mau():
    _model().reply("bạn là trợ lý", [], "chào")
    ban_gia = TRANG_THAI["ban_gia"][0]
    assert ban_gia.model == "gpt-4o-mini"
    assert ban_gia.temperature == 0.3 and ban_gia.timeout == 30


def test_reply_doc_khoa_lai_moi_luot():
    store = StoreGia(KHOA_MAU)
    mo_hinh = LangChainChatModel(_settings(), store)
    mo_hinh.reply("bạn là trợ lý", [], "chào")
    store.save(KHOA_HAI)
    mo_hinh.reply("bạn là trợ lý", [], "chào lần nữa")
    assert [b.api_key for b in TRANG_THAI["ban_gia"]] == [KHOA_MAU, KHOA_HAI]


def test_reply_dung_thu_tu_tin_va_kieu_tin():
    lich_su = [Message("human", "tin cũ"), Message("ai", "trả lời cũ")]
    _model().reply("bạn là trợ lý", lich_su, "tin mới")
    tin = TRANG_THAI["ban_gia"][0].tin_nhan[0]
    assert [t.content for t in tin] == [
        "bạn là trợ lý", "tin cũ", "trả lời cũ", "tin mới"]
    assert [type(t) for t in tin] == [
        SystemMessage, HumanMessage, AIMessage, HumanMessage]


def test_reply_khong_co_khoa_bao_loi_thieu_khoa():
    with pytest.raises(ApiKeyMissing):
        _model("").reply("bạn là trợ lý", [], "chào")


def test_reply_dung_luong_goi_rieng_khong_dung_lai():
    mo_hinh = _model()
    mo_hinh.reply("bạn là trợ lý", [Message("human", "cũ")], "mới một")
    mo_hinh.reply("bạn là trợ lý", [Message("human", "cũ")], "mới hai")
    assert len(TRANG_THAI["ban_gia"]) == 2
    assert [len(b.tin_nhan) for b in TRANG_THAI["ban_gia"]] == [1, 1]


def test_tra_loi_rong_bao_loi_502():
    TRANG_THAI["noi_dung"] = "   "
    with pytest.raises(UpstreamError) as loi:
        _model().reply("bạn là trợ lý", [], "chào")
    assert loi.value.status == 502 and "model" in loi.value.message.lower()


def test_loi_chung_bien_thanh_loi_500():
    TRANG_THAI["loi"] = RuntimeError("hỏng kết nối nội bộ")
    with pytest.raises(UpstreamError) as loi:
        _model().reply("bạn là trợ lý", [], "chào")
    assert loi.value.status == 500
