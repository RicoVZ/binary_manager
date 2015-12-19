#!/usr/bin/env python

import os.path

from flask import Flask
from flask.helpers import send_file

from BinaryInfo import BinaryInfo
from DbManager import DbManager
from BuildRepository import BuildRepository


server = Flask(__name__)

@server.route("/download/binary/<hash>")
def download_sample(hash):
    
    if BinaryInfo.is_possible_hash(hash):
        
        hashtype = BinaryInfo.get_propable_hash_type(hash)

        dbm = DbManager()
        
        dbm.open_connection()
        name = dbm.search_file_name_for(hashtype, hash)
        dbm.close_connection()
        
        if name is None:
            return "", 404
            
        if not BinaryInfo.is_hexdigest(name[0]):
            print("Error! File name is not hash. Filename: " + str(name[0]))
            return "", 404
            
        binary = "binaries//" + name[0]
        if os.path.isfile(binary):
            return send_file(binary)
        
    else:
        return "",404

if __name__ == "__main__":
        
    repository = BuildRepository()
    repository.add_all_samples()
    repository.check_db_missing_info(fix=False)
    repository.check_missing_binaries(fix=False)
    server.run()
