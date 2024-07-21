class Get:
    @classmethod
    def response(self, store, *args):
        key = args[0]
        value = store.get(key)
        if value is None:
            return "$-1\r\n"
        return f"+{value}\r\n"
