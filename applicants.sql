SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `applicants` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `applicants`;

DROP TABLE IF EXISTS `applicants`;
CREATE TABLE IF NOT EXISTS `applicants` (
    `EmployeeID` int NOT NULL,
    `roleID` int NOT NULL,
    `EmployeeName` varchar(64) NOT NULL,
    PRIMARY KEY (`EmployeeID`,`roleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `applicants` (`applicantID`,`EmployeeID`,`roleID`,`EmployeeName`) VALUES
(10002, 1, `Charlie`);
(10003, 1, `Cindy`);
ALTER TABLE applicants