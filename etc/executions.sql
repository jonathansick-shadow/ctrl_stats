CREATE TABLE IF NOT EXISTS `executions` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `condorId` varchar(24) default NULL,
  `dagNode` varchar(24) default NULL,
  `executionHost` varchar(24) default NULL,
  `imageSize` int(11) default NULL,
  `memoryUsageMb` int(11) default NULL,
  `residentSetSizeKb` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;