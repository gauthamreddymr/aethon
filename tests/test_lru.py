from aethon import Cache


def test_lru_eviction():
    cache = Cache(max_size=3)

    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)

    cache.get("a")

    cache.set("d", 4)

    assert cache.exists("b") is False
    assert cache.exists("a") is True
    assert cache.exists("c") is True
    assert cache.exists("d") is True