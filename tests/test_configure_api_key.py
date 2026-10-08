"""Kiểm thử configure_api_key và get_setup_status."""
import pytest

from src.chatbot.application.configure_api_key import configure_api_key
from src.chatbot.application.get_setup_status import get_setup_status
from src.chatbot.domain.errors import InvalidApiKey
from tests.fakes.fake_api_key_store import FakeApiKeyStore

KEY = "TEST_KEY_xxxxxxxxxxxxxxxxxxxx"
BAD_KEY = [KEY[:18], "TEST_KEY_xxxx xxxxxxxxxxxxxxxx", "TEST_KEY_xxxxxxxxxxxxxxxxxxxxđ"]


def test_get_setup_status_chua_co_khoa():
    assert get_setup_status(FakeApiKeyStore(api_key="")) == {"configured": False}


def test_get_setup_status_da_co_khoa():
    assert get_setup_status(FakeApiKeyStore(api_key=KEY)) == {"configured": True}


def test_get_setup_status_doi_trang_thai():
    store = FakeApiKeyStore(api_key="")
    assert get_setup_status(store) == {"configured": False}
    configure_api_key(store, KEY)
    assert get_setup_status(store) == {"configured": True}


def test_configure_luu_khoa_hop_le():
    store = FakeApiKeyStore()
    configure_api_key(store, f"  {KEY}\n")
    assert store.saved == [KEY]
    assert store.get() == KEY


@pytest.mark.parametrize("key", BAD_KEY)
def test_configure_khoa_sai_hinh_thuc_khong_goi_save(key):
    store = FakeApiKeyStore()
    with pytest.raises(InvalidApiKey):
        configure_api_key(store, key)
    assert store.saved == []


def test_configure_loi_ghi_tai_lan_len():
    store = FakeApiKeyStore(fail_on_save=True)
    with pytest.raises(OSError):
        configure_api_key(store, KEY)
    assert store.saved == []
    assert store.get() == ""


def test_configure_thay_khoa_cu():
    store = FakeApiKeyStore(api_key=KEY)
    new_key = KEY + "y"
    configure_api_key(store, new_key)
    assert store.saved == [new_key]
    assert store.get() == new_key
