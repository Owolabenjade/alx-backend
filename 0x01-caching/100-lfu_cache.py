#!/usr/bin/env python3
""" LFUCache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines:
      - LFU caching system with LRU as tiebreaker
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.frequencies = {}  # key -> frequency count
        self.usage_times = {}  # key -> last usage timestamp
        self.time = 0  # pseudo-timestamp for tracking recency
        self.freq_lists = {}  # frequency -> list of keys with that frequency

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        # Update time counter
        self.time += 1

        # Check if key already exists
        if key in self.cache_data:
            # Update existing key
            self.cache_data[key] = item
            self._update_frequency(key)
            self.usage_times[key] = self.time
            return

        # If cache is full, remove the LFU item (with LRU as tiebreaker)
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            self._discard_lfu()

        # Add new item
        self.cache_data[key] = item
        self.frequencies[key] = 1
        self.usage_times[key] = self.time
        
        # Add to frequency list
        if 1 not in self.freq_lists:
            self.freq_lists[1] = []
        self.freq_lists[1].append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and timestamp on access
        self.time += 1
        self._update_frequency(key)
        self.usage_times[key] = self.time
        
        return self.cache_data[key]

    def _update_frequency(self, key):
        """ Update the frequency of a key
        """
        old_freq = self.frequencies[key]
        new_freq = old_freq + 1
        
        # Remove from old frequency list
        self.freq_lists[old_freq].remove(key)
        if not self.freq_lists[old_freq]:
            del self.freq_lists[old_freq]
        
        # Add to new frequency list
        if new_freq not in self.freq_lists:
            self.freq_lists[new_freq] = []
        self.freq_lists[new_freq].append(key)
        
        # Update frequency count
        self.frequencies[key] = new_freq

    def _discard_lfu(self):
        """ Discard the least frequently used item,
            or the least recently used if there's a tie
        """
        # Find the lowest frequency
        min_freq = min(self.freq_lists.keys())
        
        # If multiple items have the lowest frequency, find the least recently used
        lfu_keys = self.freq_lists[min_freq]
        
        if len(lfu_keys) == 1:
            discard_key = lfu_keys[0]
        else:
            # Find the LRU among the LFU items
            discard_key = min(lfu_keys, key=lambda k: self.usage_times[k])
        
        # Remove from frequency tracking
        self.freq_lists[min_freq].remove(discard_key)
        if not self.freq_lists[min_freq]:
            del self.freq_lists[min_freq]
        
        # Remove from other tracking dictionaries
        del self.frequencies[discard_key]
        del self.usage_times[discard_key]
        
        # Remove from cache
        del self.cache_data[discard_key]
        
        print(f"DISCARD: {discard_key}")