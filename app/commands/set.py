from app.commands.base_command import BaseCommand
from app.store.kv_store import SetCommandOptions


class Set(BaseCommand):
    def response(self, *args):
        set_command_options = self.get_args(args)
        self._kv_store.set(set_command_options)
        return f"+OK\r\n"

    def get_args(self, args):
        key = args[0]
        value = args[1]

        if len(args) == 4 and args[2] == "px":
            expire_time = int(args[3])
            return SetCommandOptions(key, value, expire_time)

        return SetCommandOptions(key, value, None)
