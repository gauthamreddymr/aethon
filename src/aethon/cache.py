@author:gauthamreddymr

import json
import os
import tempfile
import threading
import time
from collections import OrderedDict

class Cache:
    def __init__(self, max_size=100):
        self.store = OrderedDict()
        self.max_size = max_size
        self.lock = threading.Lock()

        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expired_keys = 0

    def set(self, key, value, ttl=None):
        with self.lock:
            self._cleanup_expired()

            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl

            if key not in self.store and len(self.store) >= self.max_size:
                self.store.popitem(last=False)
                self.evictions += 1

            self.store[key] = {"value": value, "expires_at": expires_at}
            self.store.move_to_end(key)

    def get(self, key):
        with self.lock:
            item = self.store.get(key)
            if item is None:
                self.misses += 1
                return None

            expires_at = item["expires_at"]
            if expires_at is not None and time.time() > expires_at:
                del self.store[key]
                self.expired_keys += 1
                self.misses += 1
                return None

            self.store.move_to_end(key)
            self.hits += 1
            return item["value"]

    def delete(self, key):
        with self.lock:
            if key in self.store:
                del self.store[key]

    def clear(self):
        with self.lock:
            self.store.clear()

    def exists(self, key):
        with self.lock:
            item = self.store.get(key)
            if item is None:
                return False
            expires_at = item["expires_at"]
            if expires_at is not None and time.time() > expires_at:
                return False
            return True

    def size(self):
        with self.lock:
            return self._count_valid()

    def keys(self):
        with self.lock:
            now = time.time()
            return [
                key
                for key, item in self.store.items()
                if item["expires_at"] is None or now <= item["expires_at"]
            ]

    def values(self):
        with self.lock:
            now = time.time()
            return [
                item["value"]
                for item in self.store.values()
                if item["expires_at"] is None or now <= item["expires_at"]
            ]

    def items(self):
        with self.lock:
            now = time.time()
            return [
                (key, item["value"])
                for key, item in self.store.items()
                if item["expires_at"] is None or now <= item["expires_at"]
            ]

    def _cleanup_expired(self):
        now = time.time()
        keys_to_delete = [
            key
            for key, item in self.store.items()
            if item["expires_at"] is not None and now > item["expires_at"]
        ]
        for key in keys_to_delete:
            del self.store[key]
            self.expired_keys += 1

    def _count_valid(self):
        now = time.time()
        return sum(
            1
            for item in self.store.values()
            if item["expires_at"] is None or now <= item["expires_at"]
        )

    def save(self, filename):
        with self.lock:
            self._cleanup_expired()

            data = {
                "max_size": self.max_size,
                "metrics": {
                    "hits": self.hits,
                    "misses": self.misses,
                    "evictions": self.evictions,
                    "expired_keys": self.expired_keys,
                },
                "store": [[key, item] for key, item in self.store.items()],
            }

            dirname = os.path.dirname(filename) or "."
            with tempfile.NamedTemporaryFile(
                mode="w", dir=dirname, delete=False, suffix=".tmp"
            ) as tmp:
                json.dump(data, tmp, indent=4)
                temp_name = tmp.name
            os.replace(temp_name, filename)

    def load(self, filename):
        with self.lock:
            with open(filename, "r") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid cache file: root must be a dictionary")
            if "store" not in data or not isinstance(data["store"], list):
                raise ValueError("Invalid cache file: missing or invalid 'store'")

            self.max_size = data.get("max_size", 100)
            if not isinstance(self.max_size, int) or self.max_size <= 0:
                raise ValueError("max_size must be a positive integer")

            metrics = data.get("metrics", {})
            self.hits = metrics.get("hits", 0)
            self.misses = metrics.get("misses", 0)
            self.evictions = metrics.get("evictions", 0)
            self.expired_keys = metrics.get("expired_keys", 0)

            self.store.clear()
            for entry in data["store"]:
                if not isinstance(entry, list) or len(entry) != 2:
                    raise ValueError("Invalid store entry format")
                key, value_dict = entry
                if not isinstance(value_dict, dict) or "value" not in value_dict:
                    raise ValueError("Invalid entry value format")
                expires_at = value_dict.get("expires_at", None)
                if expires_at is not None and not isinstance(expires_at, (int, float)):
                    raise ValueError("Invalid expires_at type")
                self.store[key] = {
                    "value": value_dict["value"],
                    "expires_at": expires_at,
                }

            self._cleanup_expired()

    def get_metrics(self):
        with self.lock:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "expired_keys": self.expired_keys,
                "size": self._count_valid(),
                "max_size": self.max_size,
            }

    def hit_rate(self):
        with self.lock:
            total = self.hits + self.misses
            return self.hits / total if total else 0.0

    def __repr__(self):
        return (
            f"Cache(size={self.size()}, "
            f"max_size={self.max_size}, "
            f"hit_rate={self.hit_rate():.2f})"
        )
