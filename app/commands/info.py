from app.commands.base_command import BaseCommand
from app.protocol.parser import BulkString


class Info(BaseCommand):
    def response(self, *args):
        role = self._metadata_store.get_role()
        return BulkString.encode(f"role:{role}")
