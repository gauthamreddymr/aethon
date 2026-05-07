import time
from aethon import Cache


def test_ttl_expiration():
    cache = Cache()

    cache.set("temp", "data", ttl=1)

    assert cache.get("temp") == "data"

    time.sleep(2)

    assert cache.get("temp") is None


def test_cleanup_expired():
    cache = Cache()

    cache.set("a", 1, ttl=1)
    cache.set("b", 2)

    time.sleep(2)

    cache._cleanup_expired()

    assert cache.exists("a") is False
    assert cache.exists("b") is True