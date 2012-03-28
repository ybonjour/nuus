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
  PRIMARY KEY (`Id`),
  KEY `Feed` (`Feed`),
  CONSTRAINT `Feed` FOREIGN KEY (`Feed`) REFERENCES `feed` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE  TABLE `word` (
  `Id` INT(11)  NOT NULL AUTO_INCREMENT ,
  `Word` VARCHAR(255) CHARACTER SET utf8 DEFAULT NULL ,
  PRIMARY KEY (`Id`)
)
ENGINE=InnoDB DEFAULT CHARACTER SET = utf8$$
