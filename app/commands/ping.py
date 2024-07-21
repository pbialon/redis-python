class Ping:
    @classmethod
    def response(cls, store, *args):
        return "+PONG\r\n"
