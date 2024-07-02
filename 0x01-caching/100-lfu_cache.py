from base_caching import BaseCaching
from collections import defaultdict

class LFUCache(BaseCaching):
    def __init__(self):
        """Initialize the LFU cache."""
        super().__init__()  # Call the parent class's init method
        self.frequency_counter = defaultdict(int)  # Track item frequencies

    def put(self, key, item):
        """Add an item to the cache using LFU algorithm."""
        if key is None or item is None:
            return  # Do nothing if key or item is None

        # Update the cache data and frequency counter
        self.cache_data[key] = (item, self.frequency_counter[key] + 1)
        self.frequency_counter[key] += 1

        # Check if cache size exceeds the maximum capacity
        if len(self.cache_data) > self.MAX_ITEMS:
            # Find the least frequently used item(s)
            min_frequency = min(self.frequency_counter.values())
            least_frequent_keys = [k for k, v in self.frequency_counter.items() if v == min_frequency]

            # Use LRU algorithm to discard the least recently used among the least frequent items
            lru_key = least_frequent_keys[0]
            for key in least_frequent_keys:
                if self.cache_data[key][1] < self.cache_data[lru_key][1]:
                    lru_key = key

            # Evict the least frequently used (and least recently used) item
            del self.cache_data[lru_key]
            del self.frequency_counter[lru_key]
            print(f"DISCARD: {lru_key}")

    def get(self, key):
        """Get an item by key from the cache."""
        if key is None:
            return None

        # Update the frequency counter
        self.frequency_counter[key] += 1

        # Return the value associated with the key (or None if not found)
        return self.cache_data.get(key, (None, None))[0]

