class Store:
    def __init__(self):
        self._store = {}
        
    def set(self, key, value):
        self._store[key] = value
    
    def get(self, key):
        return self._store.get(key)