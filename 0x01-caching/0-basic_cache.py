#!/usr/bin/env python3
""" basic dictionary caching """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ dictionary caching system """
    def put(self, key, item):
        """ add an item in the cache """
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """ get an item by key """
        return self.cache_data.get(key)
