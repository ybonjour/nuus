delimiter $$
USE nuus$$
DROP TABLE IF EXISTS `article`$$
DROP TABLE IF EXISTS `feed`$$

CREATE TABLE `feed` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Url` varchar(255) Db  NULL,
  `Title` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `article` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) DEFAULT NULL,
  `Content` text,
  `Feed` int(11) DEFAULT NULL,
  `Updated` timestamp NULL DEFAULT NULL,
  `TitleWordCount` int(11) DEFAULT NULL,
  `ContentWordCount` int(11) DEFAULT NULL,
  `Language` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Feed` (`Feed`),
  CONSTRAINT `Feed` FOREIGN KEY (`Feed`) REFERENCES `feed` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=732 DEFAULT CHARSET=utf8$$

CREATE TABLE `word` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Word` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Word_UNIQUE` (`Word`)
) ENGINE=InnoDB AUTO_INCREMENT=36121 DEFAULT CHARSET=utf8$$

CREATE TABLE `word_index` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Word` int(11) NOT NULL,
  `Article` int(11) NOT NULL,
  `Position` int(11) NOT NULL,
  `InTitle` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Id`),
  KEY `Word` (`Word`),
  KEY `Article` (`Article`),
  CONSTRAINT `Article` FOREIGN KEY (`Article`) REFERENCES `article` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `Word` FOREIGN KEY (`Word`) REFERENCES `word` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$



