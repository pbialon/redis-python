class MetadataStore:
    def __init__(self, role):
        self._role = role

    def role(self):
        return self._role

    def replication_id(self):
        return "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"

    def master_repl_offset(self):
        return 0
