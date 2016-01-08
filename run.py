#!/usr/bin/env python

import os
import argparse

from building.BinaryInfo import BinaryInfo
from building.BuildRepository import BuildRepository
from data.DbManager import DbManager
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
        repository.add_all_samples()
        repository.check_db_missing_info(args.fix)
        repository.check_missing_binaries(args.fix)

        Config.binaries_full_dir = str(os.getcwd()) + "//" + Config.binaries_dir

        api.ApiServer.start_server()
