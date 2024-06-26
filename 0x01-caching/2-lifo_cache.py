#!/usr/bin/python3
"""Module has a class that implements the LIFO caching system"""


from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Implements the lifo cache system"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Adds an item by key"""
        if key is None or item is None:
            return
        self.cache_data[key] = item
        self.queue.append(key)
        if len(self.cache_data) > self.MAX_ITEMS:
            last_key = self.queue.pop(-2)
            print(f"DISCARD: {last_key}")
            del self.cache_data[last_key]

    def get(self, key):
        """Gets an item by key"""
        if key is None:
            return None
        return self.cache_data.get(key)
