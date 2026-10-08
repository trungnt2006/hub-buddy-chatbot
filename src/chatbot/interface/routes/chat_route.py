import time

from flask import jsonify, request

from src.chatbot.application.send_message import EMPTY_REPLY_MESSAGE, send_message
from src.chatbot.domain.errors import ApiKeyMissing, InvalidMessage, InvalidSession, UpstreamError
from src.chatbot.interface.json_error import error_response
from src.chatbot.interface.require_json import MalformedJson
from src.chatbot.interface.require_json import UnsupportedMediaType
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_json import to_response as json_to_response

UPSTREAM_ERRORS = {
    401: ("api_key_invalid", "Khóa API không đúng, nhập lại"),
    502: ("upstream_unavailable", "Không kết nối được dịch vụ mô hình"),
    503: ("upstream_busy", "Hệ thống đang quá tải, thử lại sau"),
    504: ("upstream_timeout", "Mô hình trả lời quá lâu"),
}


def register(app, deps) -> None:
    settings, repo = deps["settings"], deps["repo"]
    model, store = deps["model"], deps["store"]
    load_prompt = deps["system_prompt_loader"]

    @app.post("/api/chat")
    def chat():
        try:
            require_json()()
        except UnsupportedMediaType as exc:
            return json_to_response(exc)
        except MalformedJson as exc:
            return json_to_response(exc)
        payload = request.get_json(silent=True)
        session_id = payload.get("session_id", "")
        text = payload.get("message", "")
        system_prompt = load_prompt(settings.system_prompt_file)
        started = time.monotonic()
        try:
            reply = send_message(repo, model, store, system_prompt, settings.max_messages, session_id, text)
        except ApiKeyMissing:
            return error_response(409, "api_key_missing", "Chưa nhập khóa API")
        except InvalidMessage:
            return error_response(400, "invalid_message", "Tin nhắn rỗng hoặc quá 4000 ký tự")
        except InvalidSession:
            return error_response(400, "invalid_session", "Mã phiên không hợp lệ")
        except UpstreamError as exc:
            if exc.message in (EMPTY_REPLY_MESSAGE, "empty_reply"):
                return error_response(502, "empty_reply", "Mô hình trả lời rỗng, hãy thử lại")
            code, note = UPSTREAM_ERRORS.get(exc.status, ("internal_error", "Có lỗi không mong đợi"))
            return error_response(exc.status, code, note)
        if not reply.strip():
            return error_response(502, "empty_reply", "Mô hình trả lời rỗng, hãy thử lại")
        ms = int((time.monotonic() - started) * 1000)
        return jsonify({"reply": reply, "model": settings.openai_model, "ms": ms})
