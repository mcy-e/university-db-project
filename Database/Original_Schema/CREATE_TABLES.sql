
--? Create Department table

CREATE TABLE Department (
    Department_id INTEGER,
    name VARCHAR(25) NOT NULL,
    CONSTRAINT UN_Department_Name UNIQUE (name),
    CONSTRAINT PK_Department PRIMARY KEY (Department_id)
);

--? Create Student table

CREATE TABLE Student (
    Student_ID INTEGER,
    Last_Name VARCHAR(25) NOT NULL,
    First_Name VARCHAR(25) NOT NULL,
    DOB DATE NOT NULL,
    Address VARCHAR(50),
    City VARCHAR(25),
    Zip_Code VARCHAR(9),
    Phone VARCHAR(10),
    Fax VARCHAR(10),
    Email VARCHAR(100),
    CONSTRAINT PK_Student PRIMARY KEY (Student_ID)
);

--? Create Course table

CREATE TABLE Course (
    Course_ID INT4 NOT NULL,
    Department_ID INT4 NOT NULL,
    name VARCHAR(60) NOT NULL,
    Description VARCHAR(1000),
    CONSTRAINT PK_Course PRIMARY KEY (Course_ID, Department_ID),
    CONSTRAINT FK_Course_Department
        FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

--? Create Instructor table

CREATE TABLE Instructor (
    Instructor_ID INTEGER,
    Department_ID INTEGER NOT NULL,
    Last_Name VARCHAR(25) NOT NULL,
    First_Name VARCHAR(25) NOT NULL,
    Rank VARCHAR(25),
    Phone VARCHAR(10),
    Fax VARCHAR(10),
    Email VARCHAR(100),
    CONSTRAINT CK_Instructor_Rank
        CHECK (Rank IN ('Substitute', 'MCB', 'MCA', 'PROF')),
    CONSTRAINT PK_Instructor PRIMARY KEY (Instructor_ID),
    CONSTRAINT FK_Instructor_Department
        FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

--? Create Room table

CREATE TABLE Room (
    Building VARCHAR(1),
    RoomNo VARCHAR(10),
    Capacity INTEGER CHECK (Capacity > 1),
    CONSTRAINT PK_Room PRIMARY KEY (Building, RoomNo)
);

--? Create Reservation table

CREATE TABLE Reservation (
    Reservation_ID INTEGER,
    Building VARCHAR(1) NOT NULL,
    RoomNo VARCHAR(10) NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Instructor_ID INTEGER NOT NULL,
    Reserv_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Start_Time TIME NOT NULL DEFAULT CURRENT_TIME,
    End_Time TIME NOT NULL DEFAULT '23:00:00',
    Hours_Number INTEGER NOT NULL,

    CONSTRAINT PK_Reservation PRIMARY KEY (Reservation_ID),

    CONSTRAINT FK_Reservation_Room
        FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT FK_Reservation_Course
        FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT FK_Reservation_Instructor
        FOREIGN KEY (Instructor_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT CK_Reservation_Hours
        CHECK (Hours_Number >= 1),

    CONSTRAINT CK_Reservation_StartEndTime
        CHECK (Start_Time < End_Time)
);

--? Create Enrollment table

CREATE TABLE Enrollment (
    Student_ID INT NOT NULL,
    Course_ID INT NOT NULL,
    Department_ID INT NOT NULL,
    Enrollment_Date DATE NOT NULL,

    CONSTRAINT PK_Enrollment
        PRIMARY KEY (Student_ID, Course_ID, Department_ID),

    CONSTRAINT FK_Enrollment_Student
        FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT FK_Enrollment_Course
        FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

--? Create Mark table

CREATE TABLE Mark (
    Mark_ID SERIAL,
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Mark_Value NUMERIC(4,2) NOT NULL,
    Mark_Date DATE NOT NULL,

    CONSTRAINT PK_Mark
        PRIMARY KEY (Mark_ID),

    CONSTRAINT FK_Mark_Student
        FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT FK_Mark_Course
        FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT CK_Mark_Value
        CHECK (Mark_Value >= 0 AND Mark_Value <= 20)
);
