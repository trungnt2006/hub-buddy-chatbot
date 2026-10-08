import json
import threading

from src.chatbot.domain.message import Message
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository

KHOA_MAU = "TEST_KEY_" + "x" * 20


def _repo(tmp_path):
    return JsonMemoryRepository(tmp_path / "memory.json")


def test_get_tra_ve_rong_khi_tap_thieu(tmp_path):
    assert _repo(tmp_path).get("sesion0001") == []


def test_append_roi_get_giu_dung_thu_tu_tin(tmp_path):
    repo = _repo(tmp_path)
    repo.append("sesion0001", [Message("human", "chào"), Message("ai", "chào bạn")])
    nhan = [(m.role, m.content) for m in repo.get("sesion0001")]
    assert nhan == [("human", "chào"), ("ai", "chào bạn")]


def test_append_luu_toan_bo_tin_khong_cat(tmp_path):
    repo = _repo(tmp_path)
    for i in range(12):
        repo.append("sesion0001", [Message("human", f"câu hỏi số {i}")])
    assert len(repo.get("sesion0001")) == 12


def test_reset_chi_xoa_dung_phien_can_xoa(tmp_path):
    repo = _repo(tmp_path)
    repo.append("sesion0001", [Message("human", "a")])
    repo.append("sesion0002", [Message("human", "b")])
    repo.reset("sesion0001")
    assert repo.get("sesion0001") == [] and len(repo.get("sesion0002")) == 1


def test_reset_phien_chua_ton_tai_la_thanh_cong_im_lang(tmp_path):
    _repo(tmp_path).reset("khong-co")
    assert list(tmp_path.iterdir()) == []


def test_tap_hong_doi_ten_roi_bat_dau_rong(tmp_path):
    duong_dan = tmp_path / "memory.json"
    duong_dan.write_text("{đây không phải JSON", encoding="utf-8")
    repo = JsonMemoryRepository(duong_dan)
    assert repo.get("sesion0001") == []
    assert [p.name for p in tmp_path.iterdir()][0].startswith("memory.json.corrupt-")
    repo.append("sesion0001", [Message("human", "vẫn chạy")])
    assert len(repo.get("sesion0001")) == 1


def test_tieng_viet_va_ky_tu_dac_biet_con_lai(tmp_path):
    duong_dan = tmp_path / "memory.json"
    repo = JsonMemoryRepository(duong_dan)
    tin = "tiếng Việt 🎉 <script>"
    repo.append("sesion0001", [Message("human", tin)])
    raw = duong_dan.read_text(encoding="utf-8")
    assert "🎉" in raw and "\\u" not in raw
    assert repo.get("sesion0001")[0].content == tin


def test_hai_muoi_luong_ghi_dong_thoi_khong_mat_tin(tmp_path):
    repo = _repo(tmp_path)

    def nhan_vien(chi_so):
        repo.append("sesion0001", [Message("human", f"tin-{chi_so}")])

    luong = [threading.Thread(target=nhan_vien, args=(i,)) for i in range(20)]
    for t in luong:
        t.start()
    for t in luong:
        t.join()
    nhan = repo.get("sesion0001")
    assert len(nhan) == 20
    assert sorted(m.content for m in nhan) == sorted(f"tin-{i}" for i in range(20))


def test_tap_nho_khong_chua_khoa_api(tmp_path):
    duong_dan = tmp_path / "memory.json"
    repo = JsonMemoryRepository(duong_dan)
    repo.append("sesion0001", [Message("human", "chào bạn")])
    raw = duong_dan.read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" not in raw and KHOA_MAU not in raw


def test_get_bo_qua_ban_ghi_sai_hinh_thuc(tmp_path):
    duong_dan = tmp_path / "memory.json"
    du_lieu = {"sesion0001": [
        {"role": "human", "content": "bản ghi ổn"},
        {"role": "bot", "content": "sai vai trò"},
        {"role": "ai", "content": ""}]}
    duong_dan.write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")
    repo = JsonMemoryRepository(duong_dan)
    assert [m.content for m in repo.get("sesion0001")] == ["bản ghi ổn"]
