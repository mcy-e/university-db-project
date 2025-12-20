--? Departments

INSERT INTO Department VALUES (1, 'SADS');
INSERT INTO Department VALUES (2, 'CCS');
INSERT INTO Department VALUES (3, 'GRC');
INSERT INTO Department VALUES (4, 'INS');

--? Students

INSERT INTO Student VALUES
(1, 'Ali', 'Ben Ali', '1979-02-18', '50, 1st street', 'Algiers', '16000', '0143567890', NULL, 'A1@yahoo.fr');

INSERT INTO Student VALUES
(2, 'Amar', 'Ben Ammar', '1980-08-23', '10, Avenue b', 'BATNA', '05000', '0678567801', NULL, 'pt@yahoo.fr');

INSERT INTO Student VALUES
(3, 'Ameur', 'Ben Ameur', '1978-05-12', '25, 2nd street', 'Oran', '31000', '0145678956', '0145678956', 'o@yahoo.fr');

INSERT INTO Student VALUES
(4, 'Aissa', 'Ben Aissa', '1979-07-15', '56, Road', 'Annaba', '23000', '0678905645', NULL, 'd@hotmail.com');

INSERT INTO Student VALUES
(5, 'Fatima', 'Ben Abdedallah', '1979-08-15', '45, Faubourg', 'Constantine', '25000', NULL, NULL, NULL);

--? Instructors

INSERT INTO Instructor VALUES
(1, 1, 'Abbas', 'BenAbbes', 'MCA', '4185', '4091', 'Ab@yahoo.fr');

INSERT INTO Instructor VALUES
(2, 1, 'Mokhtar', 'BenMokhtar', 'Substitute', NULL, NULL, NULL);

INSERT INTO Instructor VALUES
(3, 1, 'Djemaa', 'Ben Mohamed', 'MCB', NULL, NULL, NULL);

INSERT INTO Instructor VALUES
(4, 1, 'Lahlou', 'Mohamed', 'PROF', NULL, NULL, NULL);

INSERT INTO Instructor VALUES
(5, 1, 'Abla', 'Chad', 'MCA', NULL, NULL, 'ab@lgmail.com');

INSERT INTO Instructor VALUES
(6, 4, 'Mariam', 'BALI', 'Substitute', NULL, NULL, NULL);

--? Rooms
INSERT INTO Room VALUES ('B', '020', 15);
INSERT INTO Room VALUES ('B', '022', 15);
INSERT INTO Room VALUES ('A', '301', 45);
INSERT INTO Room VALUES ('C', 'Lecture Hall 1', 500);
INSERT INTO Room VALUES ('C', 'Lecture Hall 2', 200);

--? Courses

INSERT INTO  Course VALUES
(1, 1, 'Databases',
 'Licence(L3) : Modeling E/A and UML, Relational Model, Relational Algebra, Relational calculs, SQL, NFs and FDs');

INSERT INTO Course VALUES
(2, 1, 'C++ progr.', 'Level Master 1');

INSERT INTO Course VALUES
(3, 1, 'Advanced DBs', 'Level Master 2-Program Licence and Master 1');

INSERT INTO Course VALUES
(4, 4, 'English', '');

--? Rooms 

INSERT INTO Room VALUES('B','020','15');
INSERT INTO Room VALUES('B','022','15');
INSERT INTO Room VALUES('A','301','45');
INSERT INTO Room VALUES('C','Hall 1','500');
INSERT INTO Room VALUES('C','Hall 2','200');

--? Reservations

INSERT INTO Reservation VALUES
(1, 'B', '022', 1, 1, 1, '2006-10-15', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(2, 'B', '022', 1, 1, 4, '2006-11-04', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(3, 'B', '022', 1, 1, 4, '2006-11-07', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(4, 'B', '020', 1, 1, 5, '2006-10-20', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(5, 'B', '020', 1, 1, 4, '2006-12-09', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(6, 'A', '301', 2, 1, 1, '2006-09-02', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(7, 'A', '301', 2, 1, 1, '2006-09-03', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(8, 'A', '301', 2, 1, 1, '2006-09-10', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(9, 'A', '301', 3, 1, 1, '2006-09-24', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(10, 'B', '022', 3, 1, 1, '2006-10-15', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(11, 'A', '301', 3, 1, 1, '2006-10-01', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(12, 'A', '301', 3, 1, 1, '2006-10-08', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(13, 'B', '022', 1, 1, 4, '2006-11-03', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(14, 'B', '022', 1, 1, 5, '2006-10-20', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(15, 'B', '022', 1, 1, 4, '2006-12-09', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(16, 'B', '022', 1, 1, 4, '2006-09-03', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(17, 'B', '022', 1, 1, 5, '2006-09-10', '08:30:00', '11:45:00', 3);

INSERT INTO Reservation VALUES
(18, 'B', '022', 1, 1, 4, '2006-09-24', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(19, 'B', '022', 1, 1, 5, '2006-10-01', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(20, 'B', '022', 1, 1, 1, '2006-10-08', '13:45:00', '17:00:00', 3);

INSERT INTO Reservation VALUES
(21, 'B', '022', 1, 1, 4, '2003-09-02', '08:30:00', '11:45:00', 3);
