#!/usr/bin/env python3
""" LRUCache module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache defines:
      - LRU caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        # Update the cache
        self.cache_data[key] = item
        
        # Update usage order - remove if exists and add to the end (most recently used)
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)
        
        # If cache exceeds max items, remove the least recently used item (LRU)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lru_key = self.usage_order.pop(0)  # First item is LRU
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        
        # Update usage order on get - item becomes most recently used
        self.usage_order.remove(key)
        self.usage_order.append(key)
        
        return self.cache_data.get(key)