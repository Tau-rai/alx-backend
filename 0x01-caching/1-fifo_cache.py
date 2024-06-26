#!/usr/bin/python3
"""Module has a class that implements the FIFO caching system"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Implements the FIFO caching system"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Add an item to cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item
        self.queue.append(key)
        if len(self.cache_data) > self.MAX_ITEMS:
            oldest_key = self.queue.pop(0)
            print(f"DISCARD: {oldest_key}")
            del self.cache_data[oldest_key]

    def get(self, key):
        """Get an item by key"""
        if key is None:
            return None
        return self.cache_data.get(key)
