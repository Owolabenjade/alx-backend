#!/usr/bin/env python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines:
      - LIFO caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        # If the key already exists, remove it from order list to update its position
        if key in self.cache_data:
            self.order.remove(key)
        
        # Add the key to the end of order list (most recent)
        self.order.append(key)
        
        # Update or add the item
        self.cache_data[key] = item
        
        # If cache exceeds max items, remove the last item added (LIFO)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Remove the key before the most recently added
            last_key = self.order[-2]
            self.order.remove(last_key)
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)