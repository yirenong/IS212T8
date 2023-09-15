SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `employee` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `employee`;

DROP TABLE IF EXISTS `emoloyee`;
CREATE TABLE IF NOT EXISTS `employee` (
    `EmployeeID` int(5) NOT NULL AUTO_INCREMENT,
    `EmployeeName` varchar(64) NOT NULL,
    `age` int NOT NULL,
    `jobTitle` varchar(64) NOT NULL,
    PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `employee` (`EmployeeID`,`EmployeeName`)VALUES 
(10001, `Jeremy`, 29, `sales`);
(10002, `Charlie`, 32, `HR manager`);
(10003, `Cindy`, 27, `solution developer`);
ALTER TABLE employee