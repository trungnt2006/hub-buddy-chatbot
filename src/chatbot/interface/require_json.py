from flask import request

from src.chatbot.interface.json_error import error_response


class UnsupportedMediaType(Exception):
    pass


class MalformedJson(Exception):
    pass


def require_json():
    def guard() -> None:
        if request.mimetype != "application/json":
            raise UnsupportedMediaType()
        if not isinstance(request.get_json(silent=True), dict):
            raise MalformedJson()

    return guard


def to_response(exc):
    if isinstance(exc, UnsupportedMediaType):
        return error_response(415, "unsupported_media_type", "Phải gửi Content-Type: application/json")
    return error_response(400, "bad_request", "Thân yêu cầu không phải đối tượng JSON")
