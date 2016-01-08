import uuid

class ApiKey:
    def __init__(self, owner):
        self.api_key    = str(uuid.uuid4())
        self.owner      = owner
        self.permission = 0
    
    def get_api_key(self):
        return self.api_key
    
    def get_owner(self):
        return self.owner
    
    def get_permission(self):
        return self.permission