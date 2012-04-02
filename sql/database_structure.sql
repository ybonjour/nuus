delimiter $$
USE nuus$$
DROP TABLE IF EXISTS `word_index`$$
DROP TABLE IF EXISTS `word`$$
DROP TABLE IF EXISTS `article`$$
DROP TABLE IF EXISTS `cluster`$$
DROP TABLE IF EXISTS `feed`$$

CREATE TABLE `feed` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Url` varchar(255) NULL,
  `Title` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `cluster` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Centroid` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Centroid_UNIQUE` (`Centroid`)
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
  `Cluster` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Feed` (`Feed`),
  KEY `Cluster` (`Cluster`),
  CONSTRAINT `Feed_Article` FOREIGN KEY (`Feed`) REFERENCES `feed` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `Cluster_Article` FOREIGN KEY (`Cluster`) REFERENCES `cluster` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

ALTER TABLE `cluster` 
  ADD CONSTRAINT `Centroid`
  FOREIGN KEY (`Centroid` )
  REFERENCES `article` (`Id` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `Centroid` (`Centroid` ASC)$$

CREATE TABLE `word` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Word` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Word_UNIQUE` (`Word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `word_index` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Word` int(11) NOT NULL,
  `Article` int(11) NOT NULL,
  `Count` int(11) NOT NULL DEFAULT '1',
  `FirstOccurence` int(11) NOT NULL,
  `InTitle` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `index_unique` (`Word`,`Article`,`InTitle`),
  KEY `Word` (`Word`),
  KEY `Article` (`Article`),
  CONSTRAINT `Article_Index` FOREIGN KEY (`Article`) REFERENCES `article` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `Word_Index` FOREIGN KEY (`Word`) REFERENCES `word` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$






