from app.parser import BulkString
from app.store import SetCommandOptions


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
    def response(cls, store, *args):
        set_command_options = cls.get_args(args)
        store.set(set_command_options)
        return f"+OK\r\n"
    
    @classmethod
    def get_args(cls, args):
        key = args[0]
        value = args[1]

        if len(args) == 4 and args[2] == "px":
            expire_time = int(args[3])
            return SetCommandOptions(key, value, expire_time)

        
        return SetCommandOptions(key, value, None)
    
    
class Get:
    @classmethod
    def response(self, store, *args):
        key = args[0]
        value = store.get(key)
        if value is None:
            return "$-1\r\n"
        return f"+{value}\r\n"
    
class Info:
    @classmethod
    def response(cls, store, *args):
        role = store.get_role()
        return BulkString.encode(f"role:{role}")


class CommandHandler:
    HANDLERS = {
        "PING": Ping,
        "ECHO": Echo,
        "SET": Set,
        "GET": Get,
        "INFO": Info,
    }
    
    @classmethod
    def response(cls, store, command):
        command_name = command[0].upper()
        
        if command_name not in cls.HANDLERS:
            return "-ERR unknown command\r\n"
        
        handler = cls.HANDLERS[command_name]
        return handler.response(store, *command[1:])