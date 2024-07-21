
class MetadataStore:
    def __init__(self, role, replication_id):
        self._role = role
        self._replication_id = replication_id
        
    def get_role(self):
        return self._role