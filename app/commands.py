

class CommandHandler:
    @classmethod
    def response(cls, command):
        command_name = command[0].upper()
        if command_name == "PING":
            return "+PONG\r\n"
        if command_name == "ECHO":
            return f"+{command[1]}\r\n"