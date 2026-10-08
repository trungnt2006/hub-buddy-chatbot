import httpx
from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                    AuthenticationError, RateLimitError)

from src.chatbot.infrastructure.map_openai_error import map_openai_error

URL = "https://api.openai.com/v1/chat/completions"
KHOA_MAU = "TEST_KEY_" + "x" * 20


def _loi(co_lop, trang_thai=None):
    yeu_cau = httpx.Request("POST", URL)
    if trang_thai is None:
        return co_lop(request=yeu_cau)
    tra_loi = httpx.Response(trang_thai, request=yeu_cau)
    return co_lop("lỗi mô phỏng", response=tra_loi, body=None)


def test_loai_xac_thuc_ve_401():
    assert map_openai_error(_loi(AuthenticationError, 401)) == (
        401, "Khóa API không đúng, nhập lại")


def test_loai_quan_ta_ve_503():
    ma, thong_diep = map_openai_error(_loi(RateLimitError, 429))
    assert ma == 503 and "quá tải" in thong_diep


def test_loai_heo_tim_ve_504():
    assert map_openai_error(_loi(APITimeoutError)) == (
        504, "Mô hình trả lời quá lâu")


def test_loai_ket_noi_ve_502():
    assert map_openai_error(_loi(APIConnectionError)) == (
        502, "Không kết nối được dịch vụ mô hình")


def test_loai_trang_thai_khac_ve_500():
    assert map_openai_error(_loi(APIStatusError, 500)) == (
        500, "Có lỗi không mong đợi")


def test_ngoai_lev_lan_ve_500():
    assert map_openai_error(RuntimeError("lỗi lạ")) == (500, "Có lỗi không mong đợi")


def test_thong_diep_khong_chua_khoa():
    loi = AuthenticationError("lỗi", response=httpx.Response(
        401, request=httpx.Request("POST", URL)), body=None)
    loi.api_key = KHOA_MAU
    ma, thong_diep = map_openai_error(loi)
    assert ma == 401 and KHOA_MAU not in thong_diep
