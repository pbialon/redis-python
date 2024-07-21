from app.commands.base_command import BaseCommand


class Get(BaseCommand):
    def response(self, *args):
        key = args[0]
        value = self._kv_store.get(key)
        if value is None:
            return "$-1\r\n"
        return f"+{value}\r\n"
