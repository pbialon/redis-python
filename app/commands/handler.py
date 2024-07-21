from app.commands.echo import Echo
from app.commands.get import Get
from app.commands.info import Info
from app.commands.set import Set
from app.commands.ping import Ping


class CommandHandler:
    HANDLERS = {
        "PING": Ping,
        "ECHO": Echo,
        "SET": Set,
        "GET": Get,
        "INFO": Info,
    }
    

    def __init__(self, kv_store, metadata_store):
        self._kv_store = kv_store
        self._metadata_store = metadata_store

        self._handlers = {
            handler_name: handler(kv_store, metadata_store)
            for handler_name, handler in self.HANDLERS.items()
        }

    def response(self, command):
        command_name = command[0].upper()

        if command_name not in self.HANDLERS:
            return "-ERR unknown command\r\n"

        handler = self._handlers[command_name]
        return handler.response(*command[1:])
