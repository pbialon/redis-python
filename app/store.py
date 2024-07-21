from collections import namedtuple
from time import time

SetCommandOptions = namedtuple("SetCommandOptions", ["key", "value", "expire_time"])

class Store:
    def __init__(self, role):
        self._store = {}
        self._role = role
        
    def set(self, set_command_options: SetCommandOptions):
        key = set_command_options.key
        value = set_command_options.value
        expiration = self._expiration_time(set_command_options.expire_time)
        
        self._store[key] = (value, expiration)
        
    def get(self, key):
        value, expiration = self._store.get(key)
        if self._is_expired(expiration):
            del self._store[key]
            return None
        
        return value
    
    def get_role(self):
        return self._role
    
    def _is_expired(self, expiration):
        return expiration is not None and expiration < self._get_current_ts()
    
    def _expiration_time(self, expiration):
        if expiration is None:
            return None
        return self._get_current_ts() + expiration
        
    def _get_current_ts(self):
        return int(time() * 1000)