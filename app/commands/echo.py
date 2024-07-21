class Echo:
    @classmethod
    def response(cls, store, *args):
        data = args[0]
        return f"+{data}\r\n"
