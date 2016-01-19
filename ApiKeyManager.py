#!/usr/bin/env python
import argparse
import sys

from api.ApiKey import ApiKey
from data.DbManager import DbManager

class ApiKeyManager:
    
    def store_new_key(self, owner):
        
        api_key = ApiKey(owner)
        
        dbm = DbManager()
        dbm.open_connection()
        
        dbm.store_api_key(api_key)
        
        dbm.close_connection()
        
        print("API Key: " + api_key.get_api_key())
    
    def del_key(self, key):
    
        dbm = DbManager()
        dbm.open_connection()
        
        if dbm.delete_api_key(key):
            print("Api key deleted")
        
        dbm.close_connection()
    
    def del_owner(self, owner):
        
        dbm = DbManager()
        dbm.open_connection()
        
        if dbm.delete_api_key_owner(owner):
            print("All api keys for " + owner + " deleted")
        
        dbm.close_connection()
    
    def del_all_keys(self):
        
        dbm = DbManager()
        dbm.open_connection()
        
        if dbm.delete_all_api_keys():
            print("All api keys deleted")
        
        dbm.close_connection()
    
    def list_all_keys(self):
        
        dbm = DbManager()
        dbm.open_connection()
        
        keys = dbm.get_all_api_keys()
        
        dbm.close_connection()
        print("{0:38} {1:10}".format("Api keys", "Owners"))
        for key in keys:
            print("| {0:10} | {1:10} |".format(key[0], key[1]))
    
if __name__ == "__main__":
    
    optparser = argparse.ArgumentParser("Api key manager")
    optparser.add_argument("-n", "--new", dest="owner", help="Add new api key with specified owner")
    optparser.add_argument("-l", "--list", help= "List all api keys and their owners" ,action="store_true")
    optparser.add_argument("-dk", "--delkey", help= "Delete specified api key")
    optparser.add_argument("-do", "--delowner", help= "Delete all keys for specified owner")
    optparser.add_argument("-DA", "--delall", help= "Delete ALL api keys", action="store_true")
    args = optparser.parse_args()
    
    if len(sys.argv) < 2:
        optparser.print_help()
    
    if args.delkey:
        ApiKeyManager().del_key(args.delkey)
    
    if args.delowner:
        ApiKeyManager().del_owner(args.delowner)
        
    if args.delall:
        ApiKeyManager().del_all_keys()
    
    if args.owner:
        manager = ApiKeyManager()
        manager.store_new_key(args.owner)
        sys.exit(0)
        
    if args.list:
        ApiKeyManager().list_all_keys()
        sys.exit(0)