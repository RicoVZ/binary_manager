import json
import os.path
import logging

from flask import Flask
from flask import request
from flask.helpers import send_file

from api.ApiKey import ApiKey
from building.BinaryInfo import BinaryInfo
from building.BuildRepository import BuildRepository
from config.Config import Config
from data.DbManager import DbManager

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
            logging.warn("Error! File name is not hash. Filename: " + str(name[0]))
            return "", 404

        binary = Config.binaries_full_dir + "//" + name[0]

        if os.path.exists(binary):
            return send_file(binary)
        else:
            return "{'message':'binary missing'}", 404

    else:
        return "",404

@server.route("/upload/binary", methods = ["POST"])
def upload_sample():
    if request.method == 'POST':
        if "api_key" in request.form.keys():
            api_key = request.form.get("api_key")
            
            if ApiKey.is_api_key_valid(api_key):
                if "file" in request.files.keys():
                    file = request.files["file"]
                    b_info = BinaryInfo(fp=file,close_fp=False)
                    
                    if BuildRepository().add_single_binary(b_info):
                        file.save(os.path.join(server.config["UPLOAD_FOLDER"], b_info.get_sha256()))
                        logging.info(request.remote_addr + " uploaded binary " + b_info.get_sha256() + " using API key " + api_key)
                        
                        return "{'message':'success'}", 200
                        
                    else:
                        logging.info(request.remote_addr + " tried uploading already existing binary " + b_info.get_sha256() + " using API key " + api_key)
                        
                        return "{'message':'already exists'}", 409

            else:
                logging.warn(request.remote_addr + " tried to use incorrect API key: " + api_key)
                
                return "", 403

    return "", 404

@server.route("/management/stats")
def get_total():
    
    stats = {}
    
    dbm = DbManager()
    dbm.open_connection()
    
    stats["total_binaries"] = dbm.get_total_binaries()[0]

    dbm.close_connection()
    
    return json.dumps(stats)
    

def start_server():
    
    server.config["MAX_CONTENT_LENGTH"] = Config.max_upload_size
    server.config["UPLOAD_FOLDER"]      = Config.binaries_full_dir
    
    logging.info("Starting server on: " + Config.listen_ip + ":" + str(Config.listen_port))
    
    server.run(Config.listen_ip, Config.listen_port)