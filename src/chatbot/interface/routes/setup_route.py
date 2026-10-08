from flask import jsonify, request

from src.chatbot.application.configure_api_key import configure_api_key
from src.chatbot.domain.errors import InvalidApiKey
from src.chatbot.interface.json_error import error_response
from src.chatbot.interface.require_json import MalformedJson
from src.chatbot.interface.require_json import UnsupportedMediaType
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_json import to_response as json_to_response
from src.chatbot.interface.require_localhost import ForbiddenAddress
from src.chatbot.interface.require_localhost import require_localhost
from src.chatbot.interface.require_localhost import to_response as host_to_response


def register(app, deps) -> None:
    store = deps["store"]

    @app.post("/api/setup")
    def setup():
        try:
            require_json()()
            require_localhost()()
        except UnsupportedMediaType as exc:
            return json_to_response(exc)
        except MalformedJson as exc:
            return json_to_response(exc)
        except ForbiddenAddress as exc:
            return host_to_response(exc)
        body = request.get_json(silent=True)
        try:
            configure_api_key(store, body.get("api_key", ""))
        except InvalidApiKey:
            return error_response(400, "invalid_api_key", "Khóa API không đúng hình thức")
        except OSError:
            return error_response(500, "save_failed", "Không ghi được tệp .env trên đĩa")
        return jsonify({"ok": True})
