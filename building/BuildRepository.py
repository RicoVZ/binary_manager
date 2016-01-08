import os.path
import shutil

from building.BinaryInfo import BinaryInfo
from data.DbManager import DbManager
from config.Config import Config

class BuildRepository:
    
    def __init__(self):

        if not os.path.exists(Config.samples_dir):
            os.mkdir(Config.samples_dir)
        if not os.path.exists(Config.binaries_dir):
            os.mkdir(Config.binaries_dir)

    def add_all_samples(self):
        
        files = os.listdir(Config.samples_dir)
        dbm   = DbManager()
        
        dbm.open_connection()
        
        for file in files:
            if os.path.isfile(Config.samples_dir + "//" + file):
                b_info = BinaryInfo(Config.samples_dir + "//" + file)
                
                if not dbm.binary_info_exists(b_info):
                    print("Inserting " + b_info.get_sha256())
                    if dbm.save_binary_info(b_info):
                        shutil.copy(Config.samples_dir + "//" + file, Config.binaries_dir + "//" + b_info.get_sha256())

        dbm.close_connection()

    def check_db_missing_info(self, fix=False):

        files  = os.listdir(Config.binaries_dir)
        dbm    = DbManager()
        errors = 0

        dbm.open_connection()

        for file in files:
            b_info = BinaryInfo(Config.binaries_dir + "//" + file)
            if not dbm.binary_info_exists(b_info):
                print("No info found on " + b_info.get_sha256())
                errors += 1

                if fix:
                    dbm.save_binary_info(b_info)
                    if not os.path.isfile(Config.binaries_dir + "//" + b_info.get_sha256()):
                        shutil.copy(Config.binaries_dir + "//" + file, Config.binaries_dir + "//" + b_info.get_sha256())
                    print("Added info to database")

        if errors < 1:
            print("No missing binary info in database")

        dbm.close_connection()

    def check_missing_binaries(self, fix=False):

        files  = os.listdir(Config.binaries_dir)
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