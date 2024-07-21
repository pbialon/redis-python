class Ping:
    @classmethod
    def response(cls, store, *args):
        return "+PONG\r\n"      
        
class Echo:
    @classmethod
    def response(cls, store, *args):
        data = args[0]
        return f"+{data}\r\n"
    
    
class Set:
    @classmethod
    def response(self, store, *args):
        key, value = args
        # todo: save key and value
        store.set(key, value)
        return f"+OK\r\n"
    
    
class Get:
    @classmethod
    def response(self, store, *args):
        key = args[0]
        value = store.get(key)
        return f"+{value}\r\n"
    
    
class CommandHandler:
    HANDLERS = {
        "PING": Ping,
        "ECHO": Echo,
        "SET": Set,
        "GET": Get,
    }
    
    @classmethod
    def response(cls, store, command):
        command_name = command[0].upper()
        
        if command_name not in cls.HANDLERS:
            return "-ERR unknown command\r\n"
        
        handler = cls.HANDLERS[command_name]
        return handler.response(store, *command[1:])