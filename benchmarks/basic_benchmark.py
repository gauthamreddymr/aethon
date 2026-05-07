import time

from aethon import Cache


cache = Cache(max_size=100000)

start = time.perf_counter()

for i in range(100000):
    cache.set(f"key-{i}", i)

end = time.perf_counter()

print(f"100k writes: {end - start:.4f} seconds")


start = time.perf_counter()

for i in range(100000):
    cache.get(f"key-{i}")

end = time.perf_counter()

print(f"100k reads: {end - start:.4f} seconds")