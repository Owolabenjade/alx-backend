#!/usr/bin/env python3
""" MRUCache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines:
      - MRU caching system
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

        # Check if we need to remove the most recently used item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            if self.usage_order:
                # Remove the most recently used item (last in usage_order)
                mru_key = self.usage_order.pop()
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")
        
        # Update the cache
        self.cache_data[key] = item
        
        # Update usage order - remove if exists and add to the end (most recently used)
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        
        # Update usage order on get - item becomes most recently used
        self.usage_order.remove(key)
        self.usage_order.append(key)
        
        return self.cache_data.get(key)