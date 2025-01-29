create	database travell;
use travell;

CREATE TABLE UpcomingTravels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    destination VARCHAR(100),
    travel_date DATE,
    duration INT,
    preferences TEXT,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE CompletedTravels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    destination VARCHAR(100),
    travel_date DATE,
    duration INT,
    preferences TEXT,
    feedback TEXT,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE UserOTP (
    mobile_number VARCHAR(10) PRIMARY KEY,
    otp INT NOT NULL,
    expiry_time DATETIME NOT NULL
);


CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);



select * from UpcomingTravels limit 1 ;
select * from CompletedTravels  ;
ALTER TABLE CompletedTravels ADD COLUMN image_path VARCHAR(255);
ALTER TABLE Users MODIFY COLUMN password VARCHAR(255);


SET GLOBAL wait_timeout = 28800;
SET GLOBAL interactive_timeout = 28800;