SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `IS212` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `IS212`;

-- Create Access Rights Table
DROP TABLE IF EXISTS `Access_Rights`;
CREATE TABLE IF NOT EXISTS `Access_Rights` (
    `Access_Level` varchar(50) PRIMARY KEY NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Access_Rights` (`Access_Level`)
VALUES ('Basic'), ('Manager');

-- Create Staff Table
DROP TABLE IF EXISTS `Staff`;
CREATE TABLE IF NOT EXISTS `Staff` (
    `Staff_ID` int(5) PRIMARY KEY NOT NULL,
    `Staff_FName` varchar(50) NOT NULL,
    `Staff_LName` varchar(50) NOT NULL,
    `Email` varchar(128) NOT NULL,
    `Dept` varchar(50) NOT NULL,
    `Country` varchar(50) NOT NULL,
    `Access_Level` varchar(50) NOT NULL,
    FOREIGN KEY (`Access_Level`) REFERENCES `Access_Rights`(`Access_Level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Staff` (`Staff_ID`, `Staff_FName`, `Staff_LName`, `Dept`, `Country`, `Email`, `Access_Level`) VALUES 
(10001, 'John', 'Doe', 'IT', 'USA', 'john.doe@example.com', 'Basic'),
(10002, 'Jane', 'Smith', 'HR', 'Canada', 'jane.smith@example.com', 'Basic'),
(10003, 'Michael', 'Johnson', 'Finance', 'UK', 'michael.j@example.com', 'Manager');

-- Create Skills Table
DROP TABLE IF EXISTS `Skills`;
CREATE TABLE IF NOT EXISTS `Skills` (
    `Skill_ID` int(5) PRIMARY KEY AUTO_INCREMENT,
    `Skill` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Skills
INSERT INTO `Skills` (`Skill`)
VALUES ('Java'), ('Python'), ('Database Management');

-- Create Role Table
DROP TABLE IF EXISTS `Role`;
CREATE TABLE IF NOT EXISTS `Role` (
    `Role_ID` int(5) PRIMARY KEY NOT NULL,
    `Title` varchar(64) NOT NULL,
    `Description` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Role
INSERT INTO `Role` (`Role_ID`, `Title`, `Description`)
VALUES (1, 'Software Engineer', 'Develops software applications'),
       (2, 'Database Administrator', 'Manages and maintains databases'),
       (3, 'Project Manager', 'Oversees project development');


-- Create Role_Skill Table
DROP TABLE IF EXISTS `Role_Skill`;
CREATE TABLE IF NOT EXISTS `Role_Skill` (
    `Role_ID` int(5) NOT NULL,
    `Skill_ID` int(5) NOT NULL,
    `Title` varchar(64) NOT NULL,
    `Description` varchar(500) NOT NULL,
    `Opening` int(5) NOT NULL,
    PRIMARY KEY (`Role_ID`, `Skill_ID`),
    FOREIGN KEY (`Role_ID`) REFERENCES `Role`(`Role_ID`),
    FOREIGN KEY (`Skill_ID`) REFERENCES `Skills`(`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Role_Skill
INSERT INTO `Role_Skill` (`Role_ID`, `Skill_ID`, `Title`, `Description`, `Opening`)
VALUES (1, 1, 'Java Developer', 'Develops software using Java', 5),
       (1, 2, 'Python Developer', 'Develops software using Python', 3),
       (2, 3, 'Database Administrator', 'Manages and maintains databases', 2),
       (3, 1, 'Project Manager', 'Oversees software projects', 1);

-- Create Job_Listing Table
DROP TABLE IF EXISTS `Job_Listing`;
CREATE TABLE IF NOT EXISTS `Job_Listing` (
    `Listing_ID` int(5) PRIMARY KEY NOT NULL,
    `Role_ID` int(5) NOT NULL,
    `Opening` int(5) NOT NULL,
    `Date_posted` DATE NOT NULL,
    FOREIGN KEY (`Role_ID`) REFERENCES `Role`(`Role_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Job_Listing
INSERT INTO `Job_Listing` (`Listing_ID`, `Role_ID`, `Opening`, `Date_posted`)
VALUES (1, 1, 3, '2023-09-28'),
       (2, 2, 2, '2023-09-29'),
       (3, 3, 1, '2023-09-30');


-- Create Application Table
DROP TABLE IF EXISTS `Application`;
CREATE TABLE IF NOT EXISTS `Application` (
    `Application_ID` int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `Staff_ID` int(5) NOT NULL,
    `Role_ID` int(5) NOT NULL,
    `Date` DATE NOT NULL,
    `Status` varchar(10) NOT NULL,
    FOREIGN KEY (`Role_ID`) REFERENCES `Role`(`Role_ID`),
    FOREIGN KEY (`Staff_ID`) REFERENCES `Staff`(`Staff_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Application
INSERT INTO `Application` (`Staff_ID`, `Role_ID`, `Date`, `Status`)
VALUES (10001, 1, '2023-09-28', 'Pending'),
       (10002, 2, '2023-09-29', 'Approved'),
       (10003, 3, '2023-09-30', 'Pending');

