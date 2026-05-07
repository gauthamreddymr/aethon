from aethon import Cache


def test_set_and_get():
    cache = Cache()

    cache.set("name", "Gautham")

    assert cache.get("name") == "Gautham"


def test_delete():
    cache = Cache()

    cache.set("x", 100)

    cache.delete("x")

    assert cache.get("x") is None


def test_clear():
    cache = Cache()

    cache.set("a", 1)
    cache.set("b", 2)

    cache.clear()

    assert cache.size() == 0


def test_exists():
    cache = Cache()

    cache.set("token", "abc")

    assert cache.exists("token") is True
    assert cache.exists("missing") is False