import threading

from aethon import Cache


def worker(cache, start, end):
    for i in range(start, end):
        cache.set(f"key-{i}", i)
        cache.get(f"key-{i}")


def test_concurrent_access():
    cache = Cache(max_size=10000)

    threads = []

    for i in range(5):
        t = threading.Thread(
            target=worker,
            args=(cache, i * 1000, (i + 1) * 1000)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert cache.size() <= 10000