import os
import sys
from pathlib import Path

from dotenv import dotenv_values

from src.chatbot.config.load_settings import load_settings
from src.chatbot.config.settings_error import SettingsError
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository
from src.chatbot.infrastructure.langchain_chat_model import LangChainChatModel
from src.chatbot.infrastructure.load_system_prompt import load_system_prompt
from src.chatbot.interface.create_app import create_app

BASE_DIR = Path(__file__).resolve().parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def main() -> int:
    try:
        settings = load_settings(BASE_DIR / ".env")
    except SettingsError as exc:
        print(f"Lỗi cấu hình: {exc}", file=sys.stderr)
        return 1
    raw_env = dotenv_values(BASE_DIR / ".env")
    if raw_env.get("OPENAI_BASE_URL"):
        os.environ["OPENAI_BASE_URL"] = raw_env["OPENAI_BASE_URL"].strip()
    store = EnvApiKeyStore(BASE_DIR / ".env")
    deps = {
        "settings": settings,
        "repo": JsonMemoryRepository(BASE_DIR / settings.memory_file),
        "model": LangChainChatModel(settings, store),
        "store": store,
        "system_prompt_loader": load_system_prompt,
    }
    app = create_app(deps)
    base_url = os.environ.get("OPENAI_BASE_URL", "OpenAI Standard Cloud")
    print(f"=======================================================")
    print(f" [🤖 AI Model]   : {settings.openai_model}")
    print(f" [🌐 Endpoint]   : {base_url}")
    print(f" [🛡️ Fallback]   : OpenAI gpt-4o-mini (tu dong khi loi)")
    print(f" [🚀 May chu]    : http://{settings.host}:{settings.port}")
    print(f"=======================================================")
    try:
        app.run(host=settings.host, port=settings.port, debug=False)
    except OSError:
        print(
            f"Cổng {settings.port} đang bận. Hãy đổi PORT trong .env rồi chạy lại.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
