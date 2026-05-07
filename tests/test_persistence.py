from aethon import Cache


def test_save_and_load(tmp_path):
    filename = tmp_path / "cache.json"

    cache = Cache()

    cache.set("a", 100)
    cache.set("b", 200)

    cache.save(filename)

    new_cache = Cache()

    new_cache.load(filename)

    assert new_cache.get("a") == 100
    assert new_cache.get("b") == 200