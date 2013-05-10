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
import datetime
from lsst.ctrl.stats.data.coresPer import CoresPer
#
# calculate the number of cores that are being used each second of the
# execution time span
#
class CoresPerSecond(CoresPer):

    def __init__(self, dbm, entries):
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where UNIX_TIMESTAMP(executionStartTime) > 0 and dagNode != 'A' and dagNode != 'B' order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        self.values = []
        # cycle through the seconds, counting the number of cores being used
        # during each second
        for thisSecond in range(startTime, stopTime+1):
            x = 0
            length = entries.getLength()
            for i in range(length):
                ent = entries.getEntry(i)
                if ent.dagNode == 'A':
                    continue
                if ent.dagNode == 'B':
                    continue
                if (thisSecond >= ent.executionStartTime) and (thisSecond <= ent.executionStopTime):
                    x = x + 1
            
            self.values.append([thisSecond,x])

        self.maximumCores, self.timeFirstUsed, self.timeLastUsed = calculateMax()
