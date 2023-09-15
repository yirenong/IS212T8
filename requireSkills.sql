SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `skills` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `skills`;

DROP TABLE IF EXISTS `skills`;
CREATE TABLE IF NOT EXISTS `skills` (
    `roleID` int NOT NULL,
    `skill` varchar(64) NOT NULL,
    FOREIGN KEY (`roleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `skills` (`roleID`,`skill`) VALUES
(1, `testSkill`);
(1, `testSkill2`);
(1, `testSkill3`);
ALTER TABLE skills