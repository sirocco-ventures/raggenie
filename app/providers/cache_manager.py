from collections import OrderedDict
from app.providers.config import configs

class CacheManager(object):
    _instance = None
    _cache_store = OrderedDict()
    _cache_limit = configs.config_cache_limit
 
    def __init__(self):
        raise RuntimeError("Call get_instance() instead")
 
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
 
    def set(self, key, value):
        if key in self._cache_store:
            self._cache_store.move_to_end(key)
        elif len(self._cache_store) >= self._cache_limit:
            self._cache_store.popitem(last=False)
            
        self._cache_store[key] = value
 
    def get(self, key):
        return self._cache_store.get(key)
 
    def clear(self, key):
        if key in self._cache_store:
            del self._cache_store[key]
 
cache_manager = CacheManager.get_instance()
