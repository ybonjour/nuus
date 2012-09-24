delimiter $$
USE nuus$$
DROP TABLE IF EXISTS `word_index_entries`$$
DROP TABLE IF EXISTS `words`$$
DROP TABLE IF EXISTS `stream_entries`$$
DROP TABLE IF EXISTS `articles`$$
DROP TABLE IF EXISTS `clusters`$$
DROP TABLE IF EXISTS `feeds`$$
DROP TABLE IF EXISTS `users`$$

CREATE  TABLE `users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT, 
  `email` VARCHAR(255) NOT NULL ,
  `password_digest` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`user_id`) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)
) ENGINE = InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `feeds` (
  `feed_id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NULL,
  `title` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `clusters` (
  `cluster_id` int(11) NOT NULL AUTO_INCREMENT,
  `centroid` int(11) NOT NULL,
  PRIMARY KEY (`cluster_id`),
  UNIQUE KEY `Centroid_UNIQUE` (`centroid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `articles` (
  `article_id` int(11) NOT NULL AUTO_INCREMENT,
  `feed_id` int(11) DEFAULT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `updated` timestamp NULL DEFAULT NULL,
  `language` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`article_id`),
  KEY `feed` (`feed_id`),
  KEY `cluster` (`cluster_id`),
  CONSTRAINT `cluster_article`
	FOREIGN KEY (`cluster_id`)
	REFERENCES `clusters` (`cluster_id`)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION,
  CONSTRAINT `feed_article`
	FOREIGN KEY (`feed_id`)
	REFERENCES `feeds` (`feed_id`)
	ON DELETE CASCADE
	ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

ALTER TABLE `clusters` 
  ADD CONSTRAINT `centroid`
  FOREIGN KEY (`centroid` )
  REFERENCES `articles` (`article_id` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `centroid` (`centroid` ASC)$$

CREATE TABLE `words` (
  `word_id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`word_id`),
  UNIQUE KEY `word_UNIQUE` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE TABLE `word_index_entries` (
  `word_index_entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `word_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `count` int(11) NOT NULL DEFAULT '1',
  `firstOccurence` int(11) NOT NULL,
  `inTitle` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`word_index_entry_id`),
  UNIQUE KEY `index_unique` (`word_id`,`article_id`,`inTitle`),
  KEY `word` (`word_id`),
  KEY `article` (`article_id`),
  CONSTRAINT `article_index`
	FOREIGN KEY (`article_id`)
	REFERENCES `articles` (`article_id`)
	ON DELETE CASCADE
	ON UPDATE NO ACTION,
  CONSTRAINT `word_index`
	FOREIGN KEY (`word_id`)
	REFERENCES `words` (`word_id`)
	ON DELETE CASCADE
	ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

CREATE  TABLE `stream_entries` (
  `stream_entry_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `user_id` INT(11) NOT NULL ,
  `article_id` INT(11) NOT NULL ,
  `weightning` DECIMAL NULL DEFAULT 1 ,
  `read` BIT NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`stream_entry_id`) ,
  INDEX `user_stream_entry` (`user_id` ASC) ,
  INDEX `article_stream_entry` (`article_id` ASC) ,
  CONSTRAINT `user_stream_entry`
    FOREIGN KEY (`user_id` )
    REFERENCES `nuus`.`users` (`user_id` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `article_stream_entry`
    FOREIGN KEY (`article_id` )
    REFERENCES `nuus`.`articles` (`article_id` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET=utf8$$

