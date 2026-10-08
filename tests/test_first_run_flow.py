from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import UpstreamError
from src.chatbot.interface import create_app as create_app_module
from src.chatbot.interface.create_app import create_app
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository

KEY = "TEST_KEY_" + "x" * 20
SID = "luong-dau-tien"
ANSWER = "Xin chào, mình là Lan."
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


def build_client(store, error=None):
    repo = FakeMemoryRepository()
    model = FakeChatModel(reply_text=ANSWER, error=error)
    deps = {
        "settings": Settings(**SETTINGS),
        "repo": repo,
        "model": model,
        "store": store,
        "system_prompt_loader": lambda path: "Bạn là trợ lý.",
    }
    app = create_app(deps)
    app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
    return app.test_client(), repo


def send(client, text):
    return client.post("/api/chat", json={"message": text, "session_id": SID})


def test_first_run_flow_full_seven_steps():
    client, repo = build_client(FakeApiKeyStore(key=""))
    assert client.get("/api/setup/status").get_json() == {"configured": False}
    assert send(client, "Chào").status_code == 409
    assert client.post("/api/setup", json={"api_key": KEY}).get_json() == {"ok": True}
    assert client.get("/api/setup/status").get_json() == {"configured": True}
    assert send(client, "Chào").get_json()["reply"] == ANSWER
    assert [m.content for m in repo.get(SID)] == ["Chào", ANSWER]


def test_root_and_health_answer_before_any_key(tmp_path, monkeypatch):
    page = tmp_path / "index.html"
    page.write_text("<!doctype html><title>chatbot</title>", encoding="utf-8")
    monkeypatch.setattr(create_app_module, "STATIC_DIR", tmp_path)
    client, _ = build_client(FakeApiKeyStore(key=""))
    assert client.get("/").status_code == 200
    assert client.get("/api/health").get_json() == {"ok": True}


def test_key_survives_new_app_instance():
    store = FakeApiKeyStore(key="")
    first, _ = build_client(store)
    assert first.post("/api/setup", json={"api_key": KEY}).get_json() == {"ok": True}
    second, _ = build_client(store)
    assert second.get("/api/setup/status").get_json() == {"configured": True}
    assert send(second, "Chào").status_code == 200


def test_model_error_does_not_store_history():
    client, repo = build_client(FakeApiKeyStore(key=KEY), error=UpstreamError(503, "quá tải"))
    assert send(client, "Chào").status_code == 503
    assert repo.get(SID) == []


def test_two_turns_same_session_keep_all_messages():
    client, repo = build_client(FakeApiKeyStore(key=KEY))
    for text in ("Câu một", "Câu hai"):
        assert send(client, text).status_code == 200
    assert [m.content for m in repo.get(SID)] == ["Câu một", ANSWER, "Câu hai", ANSWER]


def test_vietnamese_and_script_tag_are_plain_text():
    client, repo = build_client(FakeApiKeyStore(key=KEY))
    text = "Xin chào <script>alert(1)</script> 😀"
    assert send(client, text).status_code == 200
    assert repo.get(SID)[0].content == text
    assert client.get("/api/setup/status").get_json() == {"configured": True}


def test_reset_clears_history_and_accepts_new_session():
    client, repo = build_client(FakeApiKeyStore(key=KEY))
    assert send(client, "Chào").status_code == 200
    assert client.post("/api/reset", json={"session_id": SID}).get_json() == {"ok": True}
    assert repo.get(SID) == []
    assert client.post("/api/reset", json={"session_id": "khong-co-luu"}).get_json() == {"ok": True}
    bad = client.post("/api/reset", json={"session_id": "sai"})
    assert bad.status_code == 400
    assert bad.get_json()["error"] == "invalid_session"
