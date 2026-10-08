from flask import request

from src.chatbot.interface.json_error import error_response

ALLOWED_ADDRESSES = {"127.0.0.1", "::1"}


class ForbiddenAddress(Exception):
    pass


def require_localhost():
    def guard() -> None:
        if request.remote_addr not in ALLOWED_ADDRESSES:
            raise ForbiddenAddress()

    return guard


def to_response(_exc):
    return error_response(403, "forbidden", "Chỉ cho phép truy cập từ máy cục bộ")
