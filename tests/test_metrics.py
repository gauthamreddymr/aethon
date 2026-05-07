from aethon import Cache


def test_hit_and_miss_metrics():
    cache = Cache()

    cache.set("x", 1)

    cache.get("x")
    cache.get("missing")

    metrics = cache.get_metrics()

    assert metrics["hits"] == 1
    assert metrics["misses"] == 1