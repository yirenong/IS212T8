SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `Staff` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Staff`;

DROP TABLE IF EXISTS `Staff`;
CREATE TABLE IF NOT EXISTS `Staff` (
    `Staff_ID` int(5) PRIMARY KEY,
    `Staff_FName` varchar(50) NOT NULL,
    `Staff_LName` varchar(50) NOT NULL,
    `Dept` varchar(50) NOT NULL,
    `Country` varchar(50) NOT NULL,
    `Email` varchar(50) NOT NULL,
    `Access_Rights` FOREIGN KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `employee` (`Staff_ID`,`Staff_FName`,`Staff_LName`,`Dept`,`Country`,`Email`,`Access_rights`)VALUES 
(10001, `Jeremy`, `Wong`, ``,`Vietnam`,`jeremywong@gmail.com`,`manager`);
(10002, `Charlie`, `Gipson`, ``, `Malaysia`,`chalieG@gmail.com`,`admin`);
(10003, `Cindy`, `Chan`, ``,`Hong Kong`,`cindychan@gmail.com`,`users`);
ALTER TABLE Staff
