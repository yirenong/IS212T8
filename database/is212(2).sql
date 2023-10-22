-- new 
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `IS212` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `IS212`;

-- Create Access Rights Table
DROP TABLE IF EXISTS `Access`;
CREATE TABLE IF NOT EXISTS `Access` (
    `Access_Rights` varchar(50) PRIMARY KEY NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Access` (`Access_Rights`)
VALUES ('Basic'), ('Manager');

-- Create Role Table
DROP TABLE IF EXISTS `Role`;
CREATE TABLE IF NOT EXISTS `Role` (
    `Role_ID` int(5) PRIMARY KEY NOT NULL,
    `Role_Name` varchar(64) NOT NULL,
    `Description` varchar(500) NOT NULL,
    `Department` varchar(50) NOT NULL,
    INDEX `idx_department` (`Department`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Role
INSERT INTO `Role` (`Role_ID`, `Role_Name`, `Description`, `Department`) VALUES 
(1, 'Software Engineer', 'Develops software applications', 'IT'),
(2, 'Database Administrator', 'Manages and maintains databases', 'IT'),
(3, 'Project Manager', 'Oversees project development', 'IT'),
(4, 'HR Manager', 'Manages HR activities', 'HR'),
(5, 'Financial Analyst', 'Analyzes financial data', 'Finance');

-- Create Staff Table
DROP TABLE IF EXISTS `Staff`;
CREATE TABLE IF NOT EXISTS `Staff` (
    `Staff_ID` int(5) PRIMARY KEY NOT NULL,
    `Staff_FName` varchar(50) NOT NULL,
    `Staff_LName` varchar(50) NOT NULL,
    `Email` varchar(128) NOT NULL,
    `Password` varchar(128) NOT NULL,
    `Dept` varchar(50) NOT NULL,
    `Country` varchar(50) NOT NULL,
    `Access_Rights` varchar(50) NOT NULL,
    `Role_ID` int(5) NOT NULL,
    FOREIGN KEY (`Access_Rights`) REFERENCES `Access`(`Access_Rights`),
    FOREIGN KEY (`Role_ID`) REFERENCES `Role`(`Role_ID`)
    -- FOREIGN KEY (`Dept`) REFERENCES `Role`(`Department`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Staff` (`Staff_ID`, `Staff_FName`, `Staff_LName`, `Dept`, `Country`, `Email`, `Access_Rights`, `Role_ID`, `Password`) VALUES 
(10001, 'John', 'Doe', 'IT', 'USA', 'john.doe@example.com', 'Basic', 1, 'password'),
(10002, 'Jane', 'Smith', 'HR', 'Canada', 'jane.smith@example.com', 'Basic', 4, 'password'),
(10003, 'Michael', 'Johnson', 'Finance', 'UK', 'michael.j@example.com', 'Manager', 5, 'password');

-- Create Skills Table
DROP TABLE IF EXISTS `Skills`;
CREATE TABLE IF NOT EXISTS `Skills` (
    `Skill_ID` int(5) PRIMARY KEY AUTO_INCREMENT,
    `Skill_Name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Skills
INSERT INTO `Skills` (`Skill_Name`)
VALUES ('Java'), ('Python'), ('Database Management');

DROP TABLE IF EXISTS `Staff_Skill`;
CREATE TABLE IF NOT EXISTS `Staff_Skill` (
    `Staff_ID` int(5) NOT NULL,
    `Skill_ID` int(5) NOT NULL,
    `Skill_Name` varchar(64) NOT NULL,
    PRIMARY KEY (`Staff_ID`, `Skill_ID`),
    FOREIGN KEY (`Staff_ID`) REFERENCES `Staff`(`Staff_ID`),
    FOREIGN KEY (`Skill_ID`) REFERENCES `Skills`(`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `Staff_Skill` (`Staff_ID`, `Skill_ID`, `Skill_Name`)
VALUES (10001, 1, 'Java'),
       (10001, 2, 'Python'),
       (10002, 3, 'Database Management'),
       (10003, 1, 'Java'),
       (10003, 2, 'Python'),
       (10003, 3, 'Database Management');

-- Create Role_Skill Table
DROP TABLE IF EXISTS `Role_Skill`;
CREATE TABLE IF NOT EXISTS `Role_Skill` (
    `Role_ID` int(5) NOT NULL,
    `Skill_ID` int(5) NOT NULL,
    PRIMARY KEY (`Role_ID`, `Skill_ID`),
    FOREIGN KEY (`Role_ID`) REFERENCES `Role`(`Role_ID`),
    FOREIGN KEY (`Skill_ID`) REFERENCES `Skills`(`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Insert Role_Skill
INSERT INTO `Role_Skill` (`Role_ID`, `Skill_ID`)
VALUES (1, 1),
       (1, 2),
       (2, 3),
       (3, 1);

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

