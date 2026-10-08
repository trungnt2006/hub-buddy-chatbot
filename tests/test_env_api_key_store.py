import os

import pytest

from src.chatbot.infrastructure.atomic_write_text import atomic_write_text
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore
from src.chatbot.infrastructure.mask_secret import mask_secret

KHOA_MAU = "TEST_KEY_" + "x" * 20
KHOA_HAI = "TEST_KEY_" + "y" * 20


def _store(tmp_path):
    return EnvApiKeyStore(tmp_path / ".env")


@pytest.mark.parametrize("van_ban, ky_vong", [
    ("OPENAI_API_KEY=" + KHOA_MAU + "\n", KHOA_MAU),
    ("PORT=2610\r\nOPENAI_API_KEY=" + KHOA_MAU + "\r\n", KHOA_MAU),
    ('OPENAI_API_KEY="' + KHOA_MAU + '"\n', KHOA_MAU),
    ("OPENAI_API_KEY=cũ_1\nOPENAI_API_KEY=" + KHOA_MAU + "\n", KHOA_MAU),
    ("# chú thích\nOPENAI_API_KEY = " + KHOA_MAU + "\n", KHOA_MAU),
])
def test_get_doc_bien_theo_thu_tu_uu_tien(tmp_path, van_ban, ky_vong):
    duong_dan = tmp_path / ".env"
    duong_dan.write_bytes(van_ban.encode("utf-8"))
    assert _store(tmp_path).get() == ky_vong


def test_get_rong_khi_thieu_tap_va_khong_co_bien_moi_trong(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert _store(tmp_path).get() == ""


def test_is_configured_doi_ngay_sau_khi_luu(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    store = _store(tmp_path)
    assert store.is_configured() is False
    store.save(KHOA_MAU)
    assert store.is_configured() is True


def test_save_tao_tap_va_co_dung_mot_dong_khoa(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    duong_dan = tmp_path / ".env"
    _store(tmp_path).save(KHOA_MAU)
    assert duong_dan.read_text(encoding="utf-8") == "OPENAI_API_KEY=" + KHOA_MAU + "\n"


def test_save_thay_dung_dong_khoa_va_giu_dong_khac(tmp_path):
    duong_dan = tmp_path / ".env"
    van_ban = "PORT=2610\nOPENAI_API_KEY=giá_trị_cũ\nMAX_MESSAGES=5\n"
    atomic_write_text(duong_dan, van_ban)
    _store(tmp_path).save(KHOA_MAU)
    assert duong_dan.read_text(encoding="utf-8").splitlines() == [
        "PORT=2610", "OPENAI_API_KEY=" + KHOA_MAU, "MAX_MESSAGES=5"]


def test_save_xoa_cac_dong_khoa_trung_lap(tmp_path):
    duong_dan = tmp_path / ".env"
    atomic_write_text(duong_dan, "OPENAI_API_KEY=cũ_1\nOPENAI_API_KEY=cũ_2\n")
    _store(tmp_path).save(KHOA_MAU)
    dong = [d for d in duong_dan.read_text(encoding="utf-8").splitlines()
            if d.startswith("OPENAI_API_KEY=")]
    assert dong == ["OPENAI_API_KEY=" + KHOA_MAU]


def test_save_cap_nhat_bien_moi_trong_tien_trinh(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _store(tmp_path).save(KHOA_MAU)
    assert os.environ["OPENAI_API_KEY"] == KHOA_MAU


def test_save_that_bai_khi_bi_tu_choi_quyen_ghi(tmp_path, monkeypatch):
    duong_dan = tmp_path / ".env"
    atomic_write_text(duong_dan, "OPENAI_API_KEY=" + KHOA_MAU + "\n")

    def _tu_choi(*args, **kwargs):
        raise PermissionError("quyền ghi bị từ chối")

    monkeypatch.setattr(os, "replace", _tu_choi)
    with pytest.raises(PermissionError):
        _store(tmp_path).save(KHOA_HAI)
    assert duong_dan.read_text(encoding="utf-8") == "OPENAI_API_KEY=" + KHOA_MAU + "\n"
    assert list(tmp_path.iterdir()) == [duong_dan]


@pytest.mark.parametrize("gia_tri, ky_vong", [
    ("", "****"),
    ("abc", "****"),
    ("x" * 11, "****"),
    (KHOA_MAU, "****" + KHOA_MAU[-4:]),
    (KHOA_HAI, "****" + KHOA_HAI[-4:]),
])
def test_mask_secret(gia_tri, ky_vong):
    che = mask_secret(gia_tri)
    assert che == ky_vong
    assert gia_tri not in che or che == "****"
