import time
from aethon import Cache

cache = Cache(max_size=3)

cache.set("a", 100)
cache.set("b", 200)
cache.set("c", 300, ttl=3)

print(cache)

print(cache.get("a"))

print(cache.get("x"))

cache.set("d", 400)

print(cache.keys())

time.sleep(4)

print(cache.get("c"))

cache.cleanup_expired()

print(cache.keys())

print(cache.get_metrics())

print(cache.hit_rate())

cache.save("cache.json")

new_cache = Cache()

new_cache.load("cache.json")

print(new_cache)

print(new_cache.items())