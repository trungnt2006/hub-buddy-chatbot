from flask import jsonify
from werkzeug.exceptions import HTTPException


def error_response(status: int, code: str, message: str):
    return jsonify({"error": code, "message": message}), status


def register_error_handlers(app) -> None:
    @app.errorhandler(400)
    def bad_request(_error):
        return error_response(400, "bad_request", "Thân yêu cầu không hợp lệ")

    @app.errorhandler(404)
    def not_found(_error):
        return error_response(404, "not_found", "Không tìm thấy đường dẫn")

    @app.errorhandler(405)
    def wrong_method(_error):
        return error_response(405, "method_not_allowed", "Phương thức không được phép")

    @app.errorhandler(413)
    def too_large(_error):
        return error_response(413, "payload_too_large", "Nội dung gửi lên vượt 16 KB")

    @app.errorhandler(Exception)
    def unhandled(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.error("Lỗi không mong đợi: %s", type(error).__name__)
        return error_response(500, "internal_error", "Có lỗi không mong đợi")
