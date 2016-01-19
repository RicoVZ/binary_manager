import uuid

from data.DbManager import DbManager

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
    
    @staticmethod
    def is_api_key_format(key):
        
        correct = False
        if len(key) == 36:
            try:
                uuid.UUID(key, version=4)
                correct = True
            except ValueError:
                return False
                
        return correct
    
    @staticmethod
    def is_api_key_valid(key):
        
        valid = False
        
        if ApiKey.is_api_key_format(key):
            dbm = DbManager()
            dbm.open_connection()
            
            if dbm.api_key_exists(key):
                valid = True
            
            dbm.close_connection()
            
        return valid