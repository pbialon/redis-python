from app.commands.base_command import BaseCommand


class Ping(BaseCommand):
    def response(self, *args):
        return "+PONG\r\n"
