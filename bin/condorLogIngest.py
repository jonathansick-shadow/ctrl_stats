#!/usr/bin/env python

import os, sys
import argparse
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.ctrl.stats.logIngestor import LogIngestor
from lsst.daf.persistence import DbAuth
from lsst.pex.policy import Policy

if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-H", "--host", action="store", default=None, dest="host", help="mysql host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=None, dest="port", help="mysql port", type=str, required=True)
    parser.add_argument("-d", "--database", action="store", default=None, dest="database", help="database name", type=str, required=True)
    parser.add_argument("-f", "--file", action="store", default=None, dest="filenames", help="condor log files", nargs='+', type=str, required=True)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")

    args = parser.parse_args()

    host = args.host
    port = args.port
    database = args.database
    
    #
    # get database authorization info
    #
    home = os.getenv("HOME")
    pol = Policy(os.path.join(home,".lsst","db-auth.paf"))
    
    dbAuth = DbAuth()
    user = dbAuth.username(host, port)
    password = dbAuth.password(host, port)

    # connect to the database
    dbm = DatabaseManager(host, int(port), user, password)

    # create the database if it doesn't exist
    if not dbm.dbExists(database):
        dbm.createDb(database) 

    # create the LogIngestor, which creates all the tables, and will
    # be used to consolidate file information
    logIngestor = LogIngestor(dbm, database)

    # go through the list of files and ingest them, ignoring any
    # that don't exist.
    for filename in args.filenames:
        if not os.path.exists(filename):
            if args.verbose:
                print "warning: %s does not exist." % filename
            continue
        logIngestor.ingest(filename)
