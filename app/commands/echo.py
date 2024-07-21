from app.commands.base_command import BaseCommand


class Echo(BaseCommand):
    def response(self, *args):
        data = args[0]
        return f"+{data}\r\n"
