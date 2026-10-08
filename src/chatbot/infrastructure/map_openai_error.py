def map_openai_error(exc: Exception) -> tuple[int, str]:
    ma = getattr(exc, "status_code", None)
    if ma is None:
        ma = getattr(getattr(exc, "response", None), "status_code", None)
    ten_lop = [k.__name__ for k in type(exc).__mro__]
    err_str = str(exc).lower()
    if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str:
        return 503, "Khóa API đã hết hạn mức (hết tiền/credit). Vui lòng nạp thêm hoặc đổi key."
    if "AuthenticationError" in ten_lop or ma == 401:
        return 401, "Khóa API không đúng, nhập lại"
    if "RateLimitError" in ten_lop or ma == 429:
        return 503, "Hệ thống đang quá tải, thử lại sau"
    if any("Timeout" in ten for ten in ten_lop):
        return 504, "Mô hình trả lời quá lâu"
    if any("Connection" in ten for ten in ten_lop) or "notfound" in err_str or ma == 404:
        return 502, "Không kết nối được dịch vụ mô hình"
    if "model output" in err_str or ("tool call" in err_str and "empty" in err_str):
        return 502, "Mô hình không trả về văn bản"
    return 500, "Có lỗi không mong đợi"


