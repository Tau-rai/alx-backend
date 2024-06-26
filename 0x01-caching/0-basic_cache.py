#!/usr/bin/python3
"""Module for a basic cache class that is a caching system"""


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Caching system class"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.cache_data = {}

    def put(self, key, item):
        """Add an item in the cache"""
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if not key:
            return None
        value = self.cache_data.get(key)
        return value
