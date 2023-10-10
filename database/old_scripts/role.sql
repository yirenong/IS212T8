SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `Role_Skill` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Role_Skill`;

DROP TABLE IF EXISTS `Role_Skill`;
CREATE TABLE IF NOT EXISTS `Role_Skill` (
    `Role_Name` varchar(20) PRIMARY KEY,
    `Skill_Name` varchar(50) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Role_Skill` (`roleID`,`role_name`,`description`) VALUES
(`Product Manager`,`Incharge of product development`);
ALTER TABLE Role_Skill
