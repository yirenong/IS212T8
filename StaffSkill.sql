SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `Staff_Skill` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Staff_Skill`;

DROP TABLE IF EXISTS `Staff_Skill`;
CREATE TABLE IF NOT EXISTS `Staff_Skill` (
    `Staff_ID` int FOREIGN KEY,
    `Skill_Name` varchar(20) FOREIGN KEY,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Staff_Skill` (`Staff_ID`,`Skill_Name`) VALUES
(10001, `testSkill`);
(10001, `testSkill3`);
(10002, `testSkill2`);
(10002, `testSkill4`);
(10003, `testSkill1`);
(10003, `testSkill2`);
(10003, `testSkill3`);
ALTER TABLE Staff_Skill
