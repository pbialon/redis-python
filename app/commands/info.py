from app.protocol.parser import BulkString


class Info:
    @classmethod
    def response(cls, store, *args):
        role = store.get_role()
        return BulkString.encode(f"role:{role}")
