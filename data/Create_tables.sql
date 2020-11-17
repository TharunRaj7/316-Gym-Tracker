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
Location VARCHAR(256) NOT NULL CHECK(Location IN ('Wilson','Brodie')),
ResourceDisplay INTEGER CHECK(ResourceDisplay IN (0,1))
);

CREATE TABLE ClassSchedule
(ClassID       INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
 ClassType VARCHAR(256) NOT NULL, 
 ClassDay      VARCHAR(256) NOT NULL, 
 ClassTime     TIME NOT NULL, 
 ClassLocation VARCHAR(256) NOT NULL, 
 EnrollmentCap INTEGER,
 ClassDate DATE
 ClassDisplay INTEGER CHECK(ClassDisplay IN (0,1))
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
 ClassDate DATE NOT NULL,
 PRIMARY KEY(ClassID, UserID), 
 FOREIGN KEY(ClassID) REFERENCES ClassSchedule(ClassID),
 FOREIGN KEY (UserID) REFERENCES User(ID)
);


--INSERETED, CHECKED & WORKS
CREATE TRIGGER `enrollment_cap` 
AFTER INSERT ON Enrollments 
FOR EACH ROW
UPDATE ClassSchedule SET EnrollmentCap = EnrollmentCap-1 
WHERE new.ClassID = ClassSchedule.ClassID;

CREATE TRIGGER `enrollment_deletion` 
AFTER DELETE ON Enrollments 
FOR EACH ROW
UPDATE ClassSchedule SET EnrollmentCap = EnrollmentCap+1 
WHERE old.ClassID = ClassSchedule.ClassID;

CREATE TRIGGER `resource_deletion` 
AFTER DELETE ON Resources 
FOR EACH ROW
DELETE from Bookings WHERE Bookings.ResourceID = old.ResourceID;

CREATE TRIGGER `class_deletion` 
AFTER DELETE ON ClassSchedule 
FOR EACH ROW
DELETE from Enrollments WHERE Enrollments.ClassID = OLD.ClassID;

--doesn't work

CREATE TRIGGER `account_deletion` 
AFTER DELETE ON User 
FOR EACH ROW
BEGIN
DELETE from Bookings WHERE Bookings.UserID = OLD.ID;
DELETE from Enrollments WHERE Enrollments.UserID = OLD.ID;
END;

-- Trigger for Bookings at conflicting times with Enrollment and Bookings
CREATE TRIGGER `booking_conflict` 
BEFORE INSERT ON Bookings 
FOR EACH ROW

BEGIN

IF EXISTS( 
select *
from Bookings
where new.UserID = UserID and new.DateBookedOn = DateBookedOn and new.TimeBookedAt = TimeBookedAt)
then raise exception "You cannot book more than one resource at the same time.";

ELSE IF EXISTS(
select Enrollments.UserID
from Enrollments, ClassSchedule
where new.UserID = Enrollments.UserID and new.DateBookedOn = Enrollments.ClassDate and 
Enrollments.ClassID= ClassSchedule.ClassID and new.TimeBookedAt =  ClassSchedule.ClassTime
) 
THEN rollback transaction raiserror "You cannot enroll in a class at the same time as you have booked a resource.";


END IF;
RETURN NEW;

END;









-- Trigger for Enrollment at conflicting times with Enrollment and Bookings








-- CLASSSCHEDULE DATA --

INSERT INTO ClassSchedule VALUES(1,'Yoga','Monday','16:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(2,'Zumba','Monday','17:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(3,'Kickboxing','Monday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(4,'Pilates Bar','Tuesday','16:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(5,'Rhythm Cardio + Core','Tuesday','17:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(6,'Outdoor HIIT','Tuesday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(7,'Rhythm Strength/ MP','Wednesday','16:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(8,'Power Yoga','Wednesday','17:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(9,'Pilates Burn','Thursday','16:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(10,'Zumba','Thursday','17:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(11,'Outdoor HIIT','Thursday','18:00:00','Kville',20);
INSERT INTO ClassSchedule VALUES(12,'Hatha Yoga','Friday','16:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(13,'Express HIIT','Friday','17:30:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(14,'Outdoor Yoga','Saturday','10:15:00','Kville',20);
INSERT INTO ClassSchedule VALUES(15,'Kickboxing','Saturday','12:00:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(16,'Rhythm HIIT','Sunday','11:00:00','Brodie',20);
INSERT INTO ClassSchedule VALUES(17,'Power Yoga','Sunday','17:00:00','Brodie',20);

-- USER DATA --

INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (101, 'laboriosam', 'clair80@example.net', '1997-05-02 10:36:16');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (2, 'alias', 'brown.rafael@example.net', '2006-02-13 03:38:06');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (3, 'aut', 'trycia.gislason@example.org', '1984-01-24 11:25:29');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (4, 'consequatur', 'etowne@example.net', '1987-09-22 10:34:08');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (5, 'sint', 'zemlak.griffin@example.com', '1979-03-04 09:07:55');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (6, 'sit', 'jacklyn.fahey@example.net', '1999-11-25 11:22:37');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (7, 'corporis', 'koss.derrick@example.com', '1979-01-09 11:42:47');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (8, 'voluptate', 'nestor.simonis@example.org', '1990-10-03 00:13:27');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (9, 'molestiae', 'jazlyn46@example.com', '2001-02-03 13:25:42');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (10, 'vel', 'hills.karen@example.org', '1992-09-28 04:46:12');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (103, 'sed', 'princess.nikolaus@example.org', '2017-11-05 04:00:56');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (102, 'quasi', 'jones.wilmer@example.net', '2002-10-11 02:54:52');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (104, 'veritatis', 'carmine.pollich@example.net', '1979-09-28 09:04:25');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (14, 'blanditiis', 'hershel.tillman@example.com', '1992-01-16 10:43:21');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (15, 'quisquam', 'esta36@example.org', '2013-09-13 16:02:27');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (16, 'dolore', 'frida71@example.net', '1996-11-19 20:20:34');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (17, 'quam', 'maxwell41@example.com', '1980-01-26 13:53:59');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (18, 'maxime', 'noemi86@example.com', '2009-08-25 11:48:39');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (19, 'dolor', 'mvandervort@example.org', '1995-07-19 14:07:19');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (20, 'qui', 'bart.crist@example.com', '1972-09-21 13:46:58');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (21, 'voluptas', 'rippin.clint@example.org', '1996-04-06 10:37:05');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (22, 'eum', 'skye.schoen@example.net', '1975-04-26 17:01:35');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (23, 'ullam', 'ztreutel@example.org', '1999-02-26 04:05:27');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (24, 'aut', 'kenyatta.davis@example.com', '1981-04-21 15:11:02');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (25, 'voluptatibus', 'sallie02@example.com', '1976-06-11 13:57:29');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (26, 'odit', 'kiehn.joana@example.net', '1995-01-02 11:23:22');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (27, 'laborum', 'joy98@example.org', '2005-04-10 16:08:02');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (28, 'sit', 'hweissnat@example.org', '1994-07-18 19:28:12');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (29, 'ut', 'guadalupe14@example.org', '1999-10-17 14:42:13');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (30, 'molestiae', 'ystreich@example.com', '1974-09-08 02:16:24');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (31, 'et', 'wzieme@example.org', '1975-02-15 20:04:57');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (32, 'molestiae', 'goodwin.sandrine@example.net', '2018-03-07 17:04:29');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (33, 'inventore', 'kory.pfannerstill@example.org', '2009-05-10 08:01:52');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (34, 'consequatur', 'bednar.erich@example.org', '1988-08-29 18:59:57');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (35, 'labore', 'lexi.upton@example.org', '2017-05-29 22:01:48');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (36, 'qui', 'shanie46@example.org', '2011-08-22 20:25:20');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (37, 'eum', 'stoltenberg.hilbert@example.com', '1984-08-18 23:04:21');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (38, 'voluptatem', 'qglover@example.com', '1971-04-11 10:51:57');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (39, 'est', 'laurianne.botsford@example.net', '2006-07-22 11:47:27');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (40, 'esse', 'wkuhic@example.org', '1998-01-09 13:50:02');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (41, 'ullam', 'vladimir99@example.com', '2004-08-20 09:01:10');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (42, 'ut', 'thilll@example.net', '1978-01-06 14:44:18');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (43, 'aut', 'rachael80@example.com', '2009-04-09 16:46:13');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (44, 'magnam', 'flo.stroman@example.net', '2008-05-01 13:25:29');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (45, 'recusandae', 'tkunde@example.net', '1985-08-01 20:27:44');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (46, 'non', 'schmitt.rigoberto@example.com', '1970-12-28 22:48:42');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (47, 'repellendus', 'schmeler.sherwood@example.net', '1997-05-30 19:02:09');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (48, 'dolor', 'aaliyah11@example.org', '2004-06-16 07:00:06');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (49, 'a', 'tschumm@example.org', '2009-10-19 01:20:48');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (50, 'molestiae', 'judd75@example.com', '1973-08-28 10:11:31');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (51, 'temporibus', 'vhickle@example.com', '1989-08-06 20:07:00');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (52, 'illo', 'daniella51@example.net', '1987-03-06 08:06:48');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (53, 'quos', 'shaniya37@example.com', '2004-11-19 21:50:50');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (54, 'modi', 'qsipes@example.org', '2014-04-07 06:41:47');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (55, 'voluptatem', 'zpowlowski@example.com', '1989-06-02 21:24:25');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (56, 'nulla', 'qlabadie@example.com', '1976-11-07 04:25:04');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (57, 'et', 'wzemlak@example.net', '1970-11-04 04:12:11');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (58, 'numquam', 'pwelch@example.net', '1996-04-04 13:08:46');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (59, 'nihil', 'waters.howard@example.net', '2019-10-22 17:02:59');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (60, 'a', 'bauch.jacinthe@example.org', '2011-08-27 13:45:00');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (61, 'qui', 'jkub@example.net', '1972-01-21 21:03:56');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (62, 'qui', 'felton67@example.net', '2008-09-02 23:35:19');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (63, 'rerum', 'greyson.spinka@example.org', '1998-01-23 10:59:17');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (64, 'architecto', 'demmerich@example.net', '1976-07-17 15:44:31');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (65, 'maxime', 'madge17@example.com', '2012-05-16 11:01:16');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (66, 'molestias', 'jarrett61@example.com', '1974-12-10 16:50:36');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (67, 'tenetur', 'cecilia.daugherty@example.com', '1993-08-04 20:18:00');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (68, 'aut', 'hblick@example.net', '2016-03-07 21:00:08');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (69, 'nulla', 'cdubuque@example.org', '2012-05-14 12:14:33');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (70, 'eaque', 'conner.amie@example.com', '2018-11-06 13:00:06');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (71, 'dolorem', 'kelly55@example.org', '1990-12-27 23:56:02');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (72, 'impedit', 'webster12@example.net', '1981-07-23 05:34:33');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (73, 'nostrum', 'bednar.floy@example.com', '2008-08-10 18:12:54');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (74, 'nemo', 'emmie.ziemann@example.org', '2011-09-21 23:51:42');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (75, 'omnis', 'adele96@example.com', '1988-08-06 21:12:54');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (76, 'facere', 'jaqueline.franecki@example.org', '2015-01-13 06:34:33');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (77, 'voluptatibus', 'damien.gutkowski@example.com', '2001-08-08 05:26:49');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (78, 'blanditiis', 'vhilll@example.org', '1981-10-13 01:34:14');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (79, 'corporis', 'ed.emmerich@example.net', '1996-11-15 05:18:50');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (80, 'distinctio', 'whahn@example.net', '2000-06-23 09:27:19');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (81, 'debitis', 'francisco.hilpert@example.org', '1979-12-02 17:06:28');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (82, 'ut', 'hipolito22@example.net', '1972-05-28 12:26:53');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (83, 'a', 'fbahringer@example.com', '1999-04-14 01:28:41');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (84, 'recusandae', 'runte.blair@example.com', '2005-09-09 09:21:47');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (85, 'a', 'wendell89@example.net', '2014-05-14 04:18:46');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (86, 'deleniti', 'warren92@example.net', '2001-03-14 08:17:36');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (87, 'possimus', 'uswift@example.org', '2020-03-27 15:25:04');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (88, 'dolorem', 'sabrina.crona@example.org', '2009-10-07 18:02:47');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (89, 'quam', 'dulce.waelchi@example.org', '1984-03-30 05:30:52');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (90, 'omnis', 'gibson.darwin@example.com', '1980-09-20 11:57:20');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (91, 'quas', 'chanelle07@example.net', '2003-03-30 04:51:05');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (92, 'qui', 'gerlach.franco@example.com', '1987-08-06 11:16:52');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (93, 'qui', 'wrice@example.net', '1975-10-14 02:29:22');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (94, 'repellendus', 'conner@example.net', '1982-04-26 21:33:34');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (95, 'aperiam', 'mayra.schamberger@example.org', '1996-12-19 00:32:41');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (96, 'voluptatem', 'mathew.collier@example.org', '1990-06-09 10:57:14');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (97, 'cumque', 'durgan.johnathan@example.net', '1983-09-20 19:38:38');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (98, 'beatae', 'von.marie@example.net', '2012-01-10 05:45:44');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (99, 'qui', 'lang.clifford@example.net', '2018-12-09 07:58:30');
INSERT INTO `User` (`ID`, `Name`, `Email`, `AccountCreated`) VALUES (100, 'corporis', 'weimann.alexandrine@example.com', '1995-01-07 15:43:27');




