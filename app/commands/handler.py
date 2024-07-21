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

    @classmethod
    def response(cls, store, command):
        command_name = command[0].upper()

        if command_name not in cls.HANDLERS:
            return "-ERR unknown command\r\n"

        handler = cls.HANDLERS[command_name]
        return handler.response(store, *command[1:])
