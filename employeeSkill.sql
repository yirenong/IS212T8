SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `employeeSkill` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `employeeSkill`;

DROP TABLE IF EXISTS `employeeSkill`;
CREATE TABLE IF NOT EXISTS `employeeSkill` (
    `EmployeeID` int NOT NULL,
    `skill` varchar(64) NOT NULL,
    FOREIGN KEY(`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `employeeSkill` (`employeeID`,`skill`) VALUES
(10001, `testSkill`);
(10001, `testSkill3`);
(10002, `testSkill2`);
(10002, `testSkill4`);
(10003, `testSkill1`);
(10003, `testSkill2`);
(10003, `testSkill3`);
ALTER TABLE employeeSkill