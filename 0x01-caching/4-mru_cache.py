#!/usr/bin/python3
"""Module has a class that implements the MRU caching system"""


from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Implements the MRU caching system"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item
        self.queue.append(key)

        if len(self.cache_data) > self.MAX_ITEMS:
            # remove th emost recently used item( last item in queue)
            recently_discarded_key = self.queue.pop(-2)
            print(f"DISCARD: {recently_discarded_key}")
            del self.cache_data[recently_discarded_key]

    def get(self, key):
        """Gets an item by key from the cache"""
        if key is None or key not in self.cache_data:
            return None

        # update the access order(move key to the end)
        self.queue.remove(key)
        self.queue.append(key)

        return self.cache_data.get(key)
