import os.path
import shutil

from BinaryInfo import BinaryInfo
from DbManager import DbManager

class BuildRepository:
    
    def __init__(self):
        self.samples_folder  = "samples"
        self.binaries_folder = "binaries"

        if not os.path.exists(self.samples_folder):
            os.mkdir(self.samples_folder)
        if not os.path.exists(self.binaries_folder):
            os.mkdir(self.binaries_folder)

    def add_all_samples(self):
        
        files = os.listdir(self.samples_folder)
        dbm   = DbManager()
        
        dbm.open_connection()
        
        for file in files:
            if os.path.isfile(self.samples_folder + "//" + file):
                b_info = BinaryInfo(self.samples_folder + "//" + file)
                
                if not dbm.binary_info_exists(b_info):
                    print("Inserting " + b_info.get_sha256())
                    if dbm.save_binary_info(b_info):
                        shutil.copy(self.samples_folder + "//" + file, self.binaries_folder + "//" + b_info.get_sha256())

        dbm.close_connection()
    
    def check_db_missing_info(self, fix=False):
        
        files  = os.listdir(self.binaries_folder)
        dbm    = DbManager()
        errors = 0
        
        dbm.open_connection()
        
        for file in files:
            b_info = BinaryInfo(self.binaries_folder + "//" + file)
            if not dbm.binary_info_exists(b_info):
                print("No info found on " + b_info.get_sha256())
                errors += 1
                
                if fix:
                    dbm.save_binary_info(b_info)
                    if not os.path.isfile(self.binaries_folder + "//" + b_info.get_sha256()):
                        shutil.copy(self.binaries_folder + "//" + file, self.binaries_folder + "//" + b_info.get_sha256())
                    print("Added info to database")

        if errors < 1:
            print("No missing binary info in database")
        
        dbm.close_connection()
    
    def check_missing_binaries(self, fix=False):
        
        files  = os.listdir(self.binaries_folder)
        dbm    = DbManager()
        errors = 0
        
        dbm.open_connection()
        
        all_names = dbm.get_all_file_names()
        
        for name in all_names:
            
            if not name[0] in files:
                print("Missing binary: " + name[0])
                errors += 1
                
                if fix:
                    dbm.remove_file_info(name[0])
                    print("Remove file info from database")
            
        if errors < 1:
            print("No missing binaries")
        
        dbm.close_connection()