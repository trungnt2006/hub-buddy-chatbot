import os

import httpx
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import ApiKeyMissing, UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.infrastructure.map_openai_error import map_openai_error


class _NoAuth(httpx.HTTPTransport):
    def handle_request(self, req: httpx.Request) -> httpx.Response:
        req.headers.pop("authorization", None)
        return super().handle_request(req)


class LangChainChatModel(ChatModel):
    def __init__(self, settings: Settings, store: ApiKeyStore) -> None:
        self._settings = settings
        self._store = store

    def _invoke_llm(self, llm: ChatOpenAI, prompt, history: list[Message], user_text: str) -> str:
        msg_history = [
            HumanMessage(content=m.content) if m.role == "human" else AIMessage(content=m.content)
            for m in history
        ]
        res = (prompt | llm).invoke({"history": msg_history, "input": user_text})
        content = (getattr(res, "content", "") or "").strip()
        if not content and hasattr(res, "tool_calls") and res.tool_calls:
            content = "[Mô hình trả về tool call, không có văn bản]"
        if not content:
            raise UpstreamError(502, "Mô hình không trả về nội dung. Kiểm tra model name.")
        return content

    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        api_key = self._store.get()
        base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
        model = self._settings.openai_model
        if not api_key and not (base_url and "-free" in model):
            raise ApiKeyMissing("Chưa cấu hình khóa API")
        api_key = api_key or "none"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ])

        try:
            kw = {
                "model": model, "temperature": self._settings.openai_temperature,
                "timeout": self._settings.openai_timeout, "api_key": api_key,
            }
            if base_url:
                kw["base_url"] = base_url
                if api_key == "none":
                    kw["http_client"] = httpx.Client(transport=_NoAuth())
            return self._invoke_llm(ChatOpenAI(**kw), prompt, history, user_text)
        except UpstreamError:
            raise
        except Exception as exc:
            fb_exc = None
            if base_url:
                try:
                    fb = ChatOpenAI(
                        model="gpt-4o-mini", temperature=self._settings.openai_temperature,
                        timeout=self._settings.openai_timeout, api_key=api_key,
                        base_url="https://api.openai.com/v1",
                    )
                    return self._invoke_llm(fb, prompt, history, user_text)
                except UpstreamError:
                    raise
                except Exception as e:
                    fb_exc = e
            status, msg = map_openai_error(fb_exc or exc)
            raise UpstreamError(status, msg) from (fb_exc or exc)


