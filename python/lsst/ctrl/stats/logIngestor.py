# 
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import eups
import os
import re
from record import Record
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier

class LogIngestor(object):
    """
    Reads a Condor log file, classifies and groups all the records for
    each job, consolidates the information, adds the information to database
    tables.
    """
    def __init__(self, dbm, database):
        self.dbm = dbm

        submissionsTableName = "submissions"
        totalsTableName = "totals"
        updatesTableName = "updates"

        #
        # This load the submissions.sql, which creates the table
        # we're writing into.  The table won't be created
        # if it already exists. (see the SQL for details).

        pkg = eups.productDir("ctrl_stats")

        filePath = os.path.join(pkg,"etc","eventCodes.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","submissions.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","totals.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","updates.sql")
        dbm.loadSql(filePath, database)

        self.submissionsTable = database+"."+submissionsTableName
        self.updatesTable = database+"."+updatesTableName
        self.totalsTable = database+"."+totalsTableName

    def ingest(self, filename):
        # read and parse in the Condor log
        reader = Reader(filename)
        # get the record groups, which are grouped by job
        records = reader.getRecords()

        classifier = Classifier()
        for job in records:
            entries, totalsRecord, updateEntries = classifier.classify(records[job])
            # add submission records
            for ent in entries:
                ins = ent.getInsertString(self.submissionsTable)
                self.dbm.execute(ins)
            # add update records
            for ent in updateEntries:
                ins = ent.getInsertString(self.updatesTable)
                self.dbm.execute(ins)
            # add total entry
            ins = totalsRecord.getInsertString(self.totalsTable)
            self.dbm.execute(ins)
