from app.commands.base_command import BaseCommand


class ReplConf(BaseCommand):
    def response(self, *args):
        return "+OK\r\n"