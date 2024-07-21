from app.commands.base_command import BaseCommand


class Psync(BaseCommand):
    def response(self, *args):
        repl_id = self._metadata_store.replication_id()
        return f"+FULLRESYNC {repl_id} 0\r\n"
