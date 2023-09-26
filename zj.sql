SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `IS212` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `IS212`;

DROP TABLE IF EXISTS `Access_Rights`;
CREATE TABLE IF NOT EXISTS `Access_Rights` (
    `Access_Rights_ID` int(5) PRIMARY KEY AUTO_INCREMENT,
    `Access_Level` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Access_Rights` (`Access_Level`)
VALUES ('Basic'), ('Intermediate'), ('Advanced');

DROP TABLE IF EXISTS `Staff`;
CREATE TABLE IF NOT EXISTS `Staff` (
    `Staff_ID` int(5) PRIMARY KEY,
    `Staff_FName` varchar(50) NOT NULL,
    `Staff_LName` varchar(50) NOT NULL,
    `Dept` varchar(50) NOT NULL,
    `Country` varchar(50) NOT NULL,
    `Email` varchar(50) NOT NULL,
    `Access_Rights` int(5),
    FOREIGN KEY (`Access_Rights`) REFERENCES `Access_Rights`(`Access_Rights_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `Role_Skill`;
CREATE TABLE IF NOT EXISTS `Role_Skill` (
    `Role_Name` varchar(20) NOT NULL,
    `Skill_Name` varchar(50) NOT NULL,
    INDEX (`Skill_Name`), -- Adding index to Skill_Name
    PRIMARY KEY (`Role_Name`, `Skill_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `Staff_Skill`;
CREATE TABLE IF NOT EXISTS `Staff_Skill` (
    `Staff_ID` int NOT NULL,
    `Skill_Name` varchar(20),
    PRIMARY KEY (`Staff_ID`, `Skill_Name`),
    FOREIGN KEY (`Staff_ID`) REFERENCES `Staff`(`Staff_ID`),
    FOREIGN KEY (`Skill_Name`) REFERENCES `Role_Skill`(`Skill_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Staff_Skill` (`Staff_ID`,`Skill_Name`) VALUES
(10001, 'testSkill'),
(10001, 'testSkill3'),
(10002, 'testSkill2'),
(10002, 'testSkill4'),
(10003, 'testSkill1'),
(10003, 'testSkill2'),
(10003, 'testSkill3');

INSERT INTO `Role_Skill` (`Role_Name`,`Skill_Name`) VALUES
("Business Analyst", 'testSkill'),
("Business Analyst", 'testSkill3'),
("Business Analyst", 'testSkill2'),
("Accounting A1", 'testSkill4'),
("Accounting A1", 'testSkill1'),
("Assistant", 'testSkill2'),
("Assistant", 'testSkill3');
