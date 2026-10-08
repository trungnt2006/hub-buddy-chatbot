import json
import os

import pytest

from src.chatbot.infrastructure.atomic_write_json import atomic_write_json
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


def _tu_choi_thay_the(*args, **kwargs):
    raise OSError("không thể thay thế tệp")


def test_ghi_tao_thu_muc_cha_va_tap(tmp_path):
    duong_dan = tmp_path / "thu_muc_con" / "du_lieu.txt"
    atomic_write_text(duong_dan, "xin chào bạn")
    assert duong_dan.read_text(encoding="utf-8") == "xin chào bạn"


def test_ghi_khong_con_lai_tap_tam(tmp_path):
    duong_dan = tmp_path / "du_lieu.txt"
    atomic_write_text(duong_dan, "a")
    assert [p.name for p in tmp_path.iterdir()] == ["du_lieu.txt"]


def test_loi_giua_chung_giu_nguyen_noi_dung_cu(tmp_path, monkeypatch):
    duong_dan = tmp_path / "du_lieu.txt"
    atomic_write_text(duong_dan, "noi_dung_cu")
    monkeypatch.setattr(os, "replace", _tu_choi_thay_the)
    with pytest.raises(OSError):
        atomic_write_text(duong_dan, "noi_dung_moi")
    assert duong_dan.read_text(encoding="utf-8") == "noi_dung_cu"


def test_loi_giua_chung_don_tap_tam(tmp_path, monkeypatch):
    duong_dan = tmp_path / "du_lieu.txt"
    monkeypatch.setattr(os, "replace", _tu_choi_thay_the)
    with pytest.raises(OSError):
        atomic_write_text(duong_dan, "x")
    assert list(tmp_path.iterdir()) == []


def test_ghi_json_dung_thu_mot_va_tieng_viet_that(tmp_path):
    duong_dan = tmp_path / "ket_qua.json"
    atomic_write_json(duong_dan, {"loi_chuc": "tiếng Việt có dấu"})
    raw = duong_dan.read_text(encoding="utf-8")
    assert raw == '{\n  "loi_chuc": "tiếng Việt có dấu"\n}'
    assert json.loads(raw)["loi_chuc"] == "tiếng Việt có dấu"


def test_ghi_json_giu_nguyen_bieu_tuong_von(tmp_path):
    duong_dan = tmp_path / "ket_qua.json"
    du_lieu = {"sesion0001": [{"role": "human", "content": "chào 🎉 <script>"}]}
    atomic_write_json(duong_dan, du_lieu)
    assert json.loads(duong_dan.read_text(encoding="utf-8")) == du_lieu
