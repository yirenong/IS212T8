SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `roles` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `roles`;

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
    `roleID` int NOT NULL AUTO_INCREMENT,
    `role_name` varchar(64) NOT NULL,
    `description` varchar(64) NOT NULL,
    PRIMARY KEY (`roleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `roles` (`roleID`,`role_name`,`description`) VALUES
(1,`Product Manager`,`In charge of product development`);
ALTER TABLE roles