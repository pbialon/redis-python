from collections import namedtuple
from time import time

SetCommandOptions = namedtuple("SetCommandOptions", ["key", "value", "expire_time"])

Value = namedtuple("Value", ["value", "expiration"])

class KVStore:
    def __init__(self):
        self._store = {}

    def set(self, set_command_options: SetCommandOptions):
        key = set_command_options.key
        value = set_command_options.value
        expiration = self._expiration_time(set_command_options.expire_time)

        self._store[key] = Value(value, expiration)

    def get(self, key):
        value = self._store.get(key)
        if value is None:
            return None
        if self._is_expired(value.expiration):
            del self._store[key]
            return None

        return value.value

    def _is_expired(self, expiration):
        return expiration is not None and expiration < self._get_current_ts()

    def _expiration_time(self, expiration):
        if expiration is None:
            return None
        return self._get_current_ts() + expiration

    def _get_current_ts(self):
        return int(time() * 1000)
