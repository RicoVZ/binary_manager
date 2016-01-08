import os.path
import json

from flask import Flask
from flask.helpers import send_file

from building.BinaryInfo import BinaryInfo
from data.DbManager import DbManager
from config.Config import Config

server    = Flask(__name__)

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

        binary = Config.binaries_full_dir + "//" + name[0]

        if os.path.exists(binary):
            return send_file(binary)
        else:
            return "Binary missing ", 404

    else:
        return "",404

@server.route("/management/stats")
def get_total():
    
    stats = {}
    
    dbm = DbManager()
    dbm.open_connection()
    
    stats["total_binaries"] = dbm.get_total_binaries()[0]

    dbm.close_connection()
    
    return json.dumps(stats)
    

def start_server():

    server.run(Config.listen_ip, Config.listen_port, debug=True)