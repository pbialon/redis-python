class BaseCommand:
    def __init__(self, kv_store, metadata_store):
        self._kv_store = kv_store
        self._metadata_store = metadata_store
