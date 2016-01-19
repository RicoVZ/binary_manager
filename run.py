#!/usr/bin/env python

import argparse
import os
import sys

from building.BuildRepository import BuildRepository
from config.Config import Config
import api.ApiServer

if __name__ == "__main__":

    optparser = argparse.ArgumentParser("Binary repository")
    optparser.add_argument("-i", "--checkinfo", help="Check if all binaries in the binaries folder are known in the database, without starting the server", action="store_true")
    optparser.add_argument("-b", "--checkbin", help="Check if binaries known to the database still exist in the binaries folder, without starting the server", action="store_true")
    optparser.add_argument("-f", "--fix", help="Fix any errors found the by using the -i or -b option or when starting the server", action="store_true")
    args = optparser.parse_args()

    run        = True
    repository = BuildRepository()

    if args.checkinfo:
        run = False
        repository.check_db_missing_info(args.fix)

    if args.checkbin:
        run = False
        repository.check_missing_binaries(args.fix)

    if run:
        
        repository.check_db_missing_info(True)
        repository.check_missing_binaries(True)
        repository.add_all_samples()
        
        try:
            Config()
        except Exception as e:
            print("Error reading config file: " + str(e))
            sys.exit(1)
        
        try:
            api.ApiServer.start_server()
        except Exception as e:
            print("Error in server: " + str(e))
            sys.exit(1)
