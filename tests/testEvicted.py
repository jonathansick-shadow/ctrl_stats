#!/usr/bin/env python
# 
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
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
import os
import unittest
import lsst.ctrl.stats.records as recordslib
from datetime import date
from lsst.ctrl.stats.reader import Reader

# This is a set of tests for HTCondor user (non-dagman) job logs for a job
# that was evicted
class test1(unittest.TestCase):
    def setUp(self):
        filename = os.path.join("tests","testfiles","evicted.log")
        reader = Reader(filename)
        self.records = reader.getRecords()
        # Condor doesn't emit the the current year in records.  The classifier
        # code assumes it's the current year, and prepends that, so we have
        # to assume that here as well when testing for the date.
        self.year = str(date.today().year)

    def test1(self):
        # check to see we have the number of records we expect
        self.assertEqual(len(self.records), 1)

    def test2(self):
        # check validity of Submitted record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][0]
        self.assertEqual(rec.__class__.__name__, "Submitted")
        self.assertEqual(rec.event, recordslib.submitted.eventCode)

    def test3(self):
        # check validity of Executing record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][1]
        self.assertEqual(rec.__class__.__name__, "Executing")
        self.assertEqual(rec.event, recordslib.executing.eventCode)
        self.assertEqual(rec.executingHostAddr, "141.142.237.121:47727")

    def test4(self):
        # check validity of first Updated record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][2]
        self.assertEqual(rec.__class__.__name__, "Updated")
        self.assertEqual(rec.event, recordslib.updated.eventCode)
        self.assertEqual(rec.imageSize, 467532)
        self.assertEqual(rec.memoryUsageMb, 10)
        self.assertEqual(rec.residentSetSizeKb, 9856)
        self.assertEqual(rec.timestamp, self.year+"-08-20 13:09:37")

    def test5(self):
        # check validity of second Updated record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][3]
        self.assertEqual(rec.__class__.__name__, "Updated")
        self.assertEqual(rec.event, recordslib.updated.eventCode)

    def test6(self):
        # check validity of Terminated record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][4]
        self.assertEqual(rec.__class__.__name__, "Evicted")
        self.assertEqual(rec.event, recordslib.evicted.eventCode)
        self.assertEqual(rec.memoryRequest, 1)
        self.assertEqual(rec.memoryUsage, 41)
        self.assertEqual(rec.runBytesReceived, 0)
        self.assertEqual(rec.runBytesSent, 0)
        self.assertEqual(rec.timestamp, self.year+"-08-20 13:12:55")
        self.assertEqual(rec.userRunLocalUsage, 0)
        self.assertEqual(rec.userRunRemoteUsage, 0)

    def test7(self):
        # check validity of job aborted record
        self.assertIn("244585.000.000", self.records)
        rec = self.records["244585.000.000"][5]
        self.assertEqual(rec.__class__.__name__, "Aborted")
        self.assertEqual(rec.timestamp, self.year+"-08-20 13:12:55")
        self.assertEqual(rec.reason, "via condor_rm (by user srp)")


if __name__ == "__main__":
    unittest.main()
