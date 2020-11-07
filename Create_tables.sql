CREATE TABLE User
(ID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(256) NOT NULL,
Email VARCHAR(256) NOT NULL,
AccountCreated DATETIME NOT NULL
);

CREATE TABLE Resources 
(ResourceID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
ResourceName VARCHAR(256), 
ResourceType VARCHAR(256) NOT NULL CHECK(ResourceType IN ('Space','Equipment')), 
Location VARCHAR(256) NOT NULL CHECK(Location IN ('Wilson','Brodie'))
);

CREATE TABLE ClassSchedule
(ClassID       INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
 ClassType VARCHAR(256) NOT NULL, 
 ClassDay      VARCHAR(256) NOT NULL, 
 ClassTime     TIME NOT NULL, 
 ClassLocation VARCHAR(256) NOT NULL, 
 EnrollmentCap INTEGER
);

CREATE TABLE Bookings
(BookingID    INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
 UserID       INTEGER NOT NULL, 
 DateBookedOn DATE NOT NULL, 
 TimeBookedAt TIME NOT NULL, 
 ResourceID   INTEGER NOT NULL, 
 ResourceType VARCHAR(256) NOT NULL CHECK(ResourceType IN ('Space','Equipment')),
 FOREIGN KEY (UserID) REFERENCES User(ID),
 FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID)
);


CREATE TABLE Enrollments
(ClassID   INTEGER NOT NULL, 
 UserID    INTEGER NOT NULL, 
 ClassDate INTEGER NOT NULL,
 PRIMARY KEY(ClassID, UserID, ClassDate), 
 FOREIGN KEY(ClassID) REFERENCES ClassSchedule(ClassID),
 FOREIGN KEY (UserID) REFERENCES User(ResourceID)
);

INSERT INTO ClassSchedule VALUES(1,'Yoga','Monday','16:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(2,'Zumba','Monday','17:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(3,'Kickboxing','Monday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(4,'Pilates Bar','Tuesday','16:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(5,'Rhythm Cardio + Core','Tuesday','17:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(6,'Outdoor HIIT','Tuesday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(7,'Rhythm Strength/ MP','Wednesday','16:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(8,'Power Yoga','Wednesday','17:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(9,'Pilates Burn','Thursday','16:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(10,'Zumba','Thursday','17:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(11,'Outdoor HIIT','Thursday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(12,'Hatha Yoga','Friday','16:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(13,'Express HIIT','Friday','17:30:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(14,'Outdoor Yoga','Saturday','10:15:00','Kville',20);
INSERT INTO ClassSchedule VALUES(15,'Kickboxing','Saturday','12:00:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(16,'Rhythm HIIT','Sunday','11:00:00','Zoom',20);
INSERT INTO ClassSchedule VALUES(17,'Power Yoga','Sunday','17:00:00','Zoom',20);


-- CREATION OF TRIGGERS 

-- FOLLOWING TRIGGER ARE FOR ACCOUNT DELETION, RESOURCE DELETION, CLASS DELETION
--(LAST TWO FOR ADMIN PURPOSES)

USE `GymReservation`;
DELIMITER 
$$
CREATE TRIGGER `account_deletion` 
AFTER DELETE ON User FOR EACH ROW
BEGIN
DELETE from Bookings WHERE User.ID = OLD.ID;
DELETE from Enrollments WHERE User.ID = OLD.ID;
END;
$$

USE `GymReservation`;
DELIMITER 
$$
CREATE TRIGGER `resource_deletion` 
AFTER DELETE ON Resources FOR EACH ROW
BEGIN
DELETE from Bookings WHERE Booking.ResourceID = OLD.ResourceID;
END;
$$

USE `GymReservation`;
DELIMITER 
$$
CREATE TRIGGER `class_deletion` 
AFTER DELETE ON ClassSchedule FOR EACH ROW
BEGIN
DELETE from Enrollments WHERE Enrollments.ClassID = OLD.ClassID;
END;
$$
