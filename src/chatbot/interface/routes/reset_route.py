from flask import jsonify, request

from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.domain.errors import InvalidSession
from src.chatbot.interface.json_error import error_response
from src.chatbot.interface.require_json import MalformedJson
from src.chatbot.interface.require_json import UnsupportedMediaType
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_json import to_response as json_to_response


def register(app, deps) -> None:
    repo = deps["repo"]

    @app.post("/api/reset")
    def reset():
        try:
            require_json()()
        except UnsupportedMediaType as exc:
            return json_to_response(exc)
        except MalformedJson as exc:
            return json_to_response(exc)
        body = request.get_json(silent=True)
        try:
            reset_conversation(repo, body.get("session_id", ""))
        except InvalidSession:
            return error_response(400, "invalid_session", "Mã phiên không hợp lệ")
        return jsonify({"ok": True})
