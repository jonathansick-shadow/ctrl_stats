CREATE TABLE IF NOT EXISTS `submissions` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `condorId` varchar(24) default NULL,
  `dagNode` varchar(10) default NULL,
  `executionHost` varchar(80) default NULL,
  `slotName` varchar(10) default NULL,
  `submitTime` datetime default NULL,
  `executionStartTime` datetime default NULL,
  `executionStopTime` datetime default NULL,
  `updateImageSize` int(11) default NULL,
  `updateMemoryUsageMb` int(11) default NULL,
  `updateResidentSetSizeKb` int(11) default NULL,
  `userRunRemoteUsage` int(11) default NULL,
  `sysRunRemoteUsage` int(11) default NULL,
  `finalDiskUsageKb` int(11) default NULL,
  `finalDiskRequestKb` int(11) default NULL,
  `finalMemoryUsageMb` int(11) default NULL,
  `finalMemoryRequestMb` int(11) default NULL,
  `bytesSent` int(11) default NULL,
  `bytesReceived` int(11) default NULL,
  `terminationTime` datetime default NULL,
  `terminationCode` varchar(3) default NULL,
  `terminationReason` varchar(4096) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
