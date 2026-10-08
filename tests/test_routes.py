from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import UpstreamError
from src.chatbot.interface.create_app import create_app
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository

KEY = "TEST_KEY_" + "x" * 20
SID = "abc-1234"
REMOTE = {"REMOTE_ADDR": "10.0.0.7"}
CHAT = {"message": "Chào bạn", "session_id": SID}
BAD_KEYS = ["", "   ", "abc", KEY + " mat", "TEST_KEY_" + "y" * 20 + " ñ"]
POST_PATHS = ["/api/setup", "/api/chat", "/api/reset"]
UPSTREAM_CASES = [
    (401, "api_key_invalid"),
    (502, "upstream_unavailable"),
    (503, "upstream_busy"),
    (504, "upstream_timeout"),
]
SETTINGS = {
    "openai_api_key": "",
    "openai_model": "gpt-4o-mini",
    "openai_temperature": 0.3,
    "openai_timeout": 30,
    "host": "127.0.0.1",
    "port": 2610,
    "memory_file": "memory.json",
    "max_messages": 5,
    "system_prompt_file": "system-prompt.txt",
}


def build_app(store=None, error=None, reply_text="Xin chào"):
    repo = FakeMemoryRepository()
    model = FakeChatModel(reply_text=reply_text, error=error)
    store = FakeApiKeyStore(key=KEY) if store is None else store
    deps = {
        "settings": Settings(**SETTINGS),
        "repo": repo,
        "model": model,
        "store": store,
        "system_prompt_loader": lambda path: "Bạn là trợ lý.",
    }
    app = create_app(deps)
    app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
    return app, repo


def client(store=None, error=None, reply_text="Xin chào"):
    return build_app(store, error, reply_text)[0].test_client()


def assert_error(response, status, code):
    assert response.status_code == status, response.get_data(as_text=True)
    assert response.get_json()["error"] == code


def test_setup_saves_valid_key_and_rejects_bad_ones():
    fresh = client(FakeApiKeyStore(key=""))
    body = fresh.post("/api/setup", json={"api_key": KEY, "model": "trường thừa"}).get_json()
    assert body == {"ok": True}
    assert KEY not in str(body)
    assert fresh.get("/api/setup/status").get_json() == {"configured": True}
    for bad in BAD_KEYS:
        assert_error(client().post("/api/setup", json={"api_key": bad}), 400, "invalid_api_key")


def test_setup_forbidden_from_remote_address():
    assert_error(client().post("/api/setup", json={"api_key": KEY}, environ_base=REMOTE), 403, "forbidden")


def test_protocol_errors_return_json():
    for path in POST_PATHS:
        assert_error(client().post(path, data='{"message":"Chào bạn"}'), 415, "unsupported_media_type")
        assert_error(client().post(path, data="{bad", content_type="application/json"), 400, "bad_request")
    assert_error(client().post("/api/chat", json=dict(CHAT, message="a" * 20000)), 413, "payload_too_large")
    assert_error(client().get("/api/khong-ton-tai"), 404, "not_found")
    assert_error(client().get("/api/chat"), 405, "method_not_allowed")


def test_chat_returns_reply_model_and_ms():
    body = client().post("/api/chat", json=dict(CHAT, history=["bỏ qua"])).get_json()
    assert body["reply"] == "Xin chào"
    assert body["model"] == "gpt-4o-mini"
    assert isinstance(body["ms"], int) and body["ms"] >= 0


def test_chat_error_codes():
    assert_error(client(FakeApiKeyStore(key="")).post("/api/chat", json=CHAT), 409, "api_key_missing")
    assert_error(client().post("/api/chat", json=dict(CHAT, message="   ")), 400, "invalid_message")
    assert_error(client().post("/api/chat", json=dict(CHAT, session_id="x")), 400, "invalid_session")
    assert_error(client(reply_text="  ").post("/api/chat", json=CHAT), 502, "empty_reply")
    crash = client(error=RuntimeError("lỗi nội bộ")).post("/api/chat", json=CHAT)
    assert_error(crash, 500, "internal_error")
    assert "Traceback" not in crash.get_data(as_text=True)


def test_chat_maps_upstream_status():
    for status, code in UPSTREAM_CASES:
        broken = client(error=UpstreamError(status, "lỗi mô hình")).post("/api/chat", json=CHAT)
        assert_error(broken, status, code)
