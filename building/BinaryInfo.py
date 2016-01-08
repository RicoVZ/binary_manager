import hashlib
import os.path

class BinaryInfo:
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.md5       = hashlib.md5()
        self.sha1      = hashlib.sha1()
        self.sha256    = hashlib.sha256()
        self.sha512    = hashlib.sha512()
        self._calc_hashes()
    
    def _calc_hashes(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, "rb") as fp:
                
                while True:
                    chunk = fp.read(4096)
                    if not chunk:
                        break
                    self.md5.update(chunk)
                    self.sha1.update(chunk)
                    self.sha256.update(chunk)
                    self.sha512.update(chunk)
        else:
            print("File: " + self.file_path + " does not exist")
    
    def get_md5(self):
        return self.md5.hexdigest()
    
    def get_sha1(self):
        return self.sha1.hexdigest()
    
    def get_sha256(self):
        return self.sha256.hexdigest()
    
    def get_sha512(self):
        return self.sha512.hexdigest()
    
    @staticmethod
    def is_possible_hash(value):
        
        supported_length = [32,40,64,128]
        if len(value) in supported_length:
            return True
        else:
            return False
    
    @staticmethod
    def get_propable_hash_type(value):
        
        hash_types = {32:"md5",40:"sha1",64:"sha256",128:"sha512"}
        return hash_types[len(value)]
    
    @staticmethod
    def is_hexdigest(value):
        
        is_digest = False
        
        try:
            int(value, 16)
            is_digest = True
        except Exception:
            is_digest = False
        
        return is_digest