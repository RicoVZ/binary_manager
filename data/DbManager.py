import sqlite3
import logging

class DbManager:
    def __init__(self):
        self.conn    = None
        self.cursor  = None
        self.db_name = "binary_manager.sqlite"
        
    def open_connection(self):
        
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
        
        if self.cursor is None:
            self.cursor = self.conn.cursor()
        
        self._run_table_sql()
    
    def close_connection(self):
        
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        
        if self.conn is not None:
            self.conn.close()
            self.conn = None
                
    def save_binary_info(self, b_info):
        
        success = False
        query = "INSERT INTO file_info VALUES (?, ?, ?, ?, ?)"
        
        try:
            self.cursor.execute(query, (b_info.get_sha256(), 
                                        b_info.get_md5(),
                                        b_info.get_sha1(),
                                        b_info.get_sha256(),
                                        b_info.get_sha512()))
            self.conn.commit()
            success = True
        except sqlite3.Error as e:
            logging.error("Failed to insert binary_info: " + e.message)
        
        return success
    
    def store_api_key(self, api_key):
        
        success = False
        query = "INSERT INTO api_key VALUES(?,?,?)"
        
        try:
            self.cursor.execute(query,(api_key.get_api_key(),
                                       api_key.get_owner(),
                                       api_key.get_permission()
                                       ))
            self.conn.commit()
            success = True
        except sqlite3.Error as e:
            logging.error("Failed to store api key " + e.message)
            
        return success
    
    def get_all_api_keys(self):
        
        query = "SELECT api_key, owner FROM api_key"
        keys  = []
        
        try:
            self.cursor.execute(query)
            keys = self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error("Failed to get all api keys " + e.message)
        
        return keys
    
    def delete_api_key(self, key):
        
        success = False
        query  = "DELETE FROM api_key WHERE api_key = ?"
        
        try:
            self.cursor.execute(query, (key,))
            self.conn.commit()
            success = True
        except sqlite3.Error as e:
            logging.error("Failed to delete api key: " + e.message)
        
        return success
    
    def delete_api_key_owner(self, owner):
        
        success = False
        query   = "DELETE FROM api_key WHERE owner = ?"
        
        try:
            self.cursor.execute(query, (owner,))
            self.conn.commit()
            success = True
        except sqlite3.Error as e:
            logging.error("Failed to delete api key: " + e.message)
            
        return success
    
    def delete_all_api_keys(self):
        
        success = False
        query   = "DELETE FROM api_key"
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            success = True
        except sqlite3.Error as e:
            logging.error("Failed to delete all api keys: " + e.message)
        
        return success
    
    def api_key_exists(self, key):
        
        found = False
        query = "SELECT api_key FROM api_key WHERE api_key = ?"
        
        try:
            self.cursor.execute(query, (key,))
            
            if self.cursor.fetchone() is not None:
                found = True
        
        except sqlite3.Error as e:
            logging.error("Failed to select on api key " + e.message)
        
        return found
    
    def binary_info_exists(self, b_info):
        
        found = False
        query = "SELECT name FROM file_info WHERE name = ?"
        
        try:
            self.cursor.execute(query, (b_info.get_sha256(),))
            
            if self.cursor.fetchone() is not None:
                found = True
        
        except sqlite3.Error as e:
            logging.error("Failed to select on binary name " + e.message)
        
        return found
    
    def get_all_file_names(self):
        
        query   = "SELECT name FROM file_info"
        results = []
        
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

        except sqlite3.Error as e:
            logging.error("Failed to select all name: " + e.message)
        
        return results
    
    def remove_file_info(self, sha256):
        
        query = "DELETE FROM file_info WHERE name = ?"
        
        try:
            self.cursor.execute(query, (sha256,))
            self.conn.commit()
            
        except sqlite3.Error as e:
            logging.error("Failed to delete binary info: " + e.message)
    
    def search_file_name_for(self, hashtype, hash):
        
        name  = None
        
        if hashtype in ["md5", "sha1", "sha256", "sha512"]:
            query = "SELECT name FROM file_info WHERE %s = ?" %hashtype

            try:
                self.cursor.execute(query, (str(hash),))
                name = self.cursor.fetchone()
            except sqlite3.Error as e:
                logging.error("Failed to search binary info for: "  +str(hash) + " " + e.message)
                
        return name
    
    def get_total_binaries(self):
        
        total = 0
        query = "SELECT count(md5) FROM file_info"
        
        try:
            self.cursor.execute(query)
            total = self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error("Failed to get total binaries")

        return total
            
    
    def _run_table_sql(self):
        
        with open("sql//file_info.sql", "r") as fp:
            self.cursor.execute(fp.read())
            self.conn.commit()

        with open("sql//api_key.sql", "r") as fp:
            self.cursor.execute(fp.read())
            self.conn.commit()
        