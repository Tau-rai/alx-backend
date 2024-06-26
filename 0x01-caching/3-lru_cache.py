#!/usr/bin/python3
"""Module has a class that implements the LRU chaching system"""


from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Implements the LRU caching algorithm"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.queue.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # remove the recently used item
            recently_used_key = self.queue.pop(0)
            print(f"DISCARD: {recently_used_key}")
            del self.cache_data[recently_used_key]

        # add new key and item to the cache
        self.cache_data[key] = item
        self.queue.append(key)

    def get(self, key):
        """Gets an item by key"""
        if key is None or key not in self.cache_data:
            return None

        # update the position of the key and mark it as recently used
        self.queue.remove(key)
        self.queue.append(key)

        return self.cache_data.get(key)
