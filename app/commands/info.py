from app.commands.base_command import BaseCommand
from app.protocol.parser import BulkString


class Info(BaseCommand):
    def response(self, *args):
        role = self._metadata_store.role()
        offset = self._metadata_store.master_repl_offset()
        replication_id = self._metadata_store.replication_id()

        message = (
            f"role:{role}master_repl_offset:{offset}master_replid:{replication_id}"
        )

        return BulkString.encode(message)
