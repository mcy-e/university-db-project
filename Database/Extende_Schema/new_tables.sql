-- create an enum for activity
create type Activity_type as enum('lecture','toturiol','practical');

--create an enum for attendence

create type status as enum('present', 'absent');

-- activity table
create table activity (
    activity_id BIGSERIAL not null primary key,
    Activity_Type Activity_type not null,
    reservation_id int not null,
    course_id int not null,
    department_id int not null , 
    constraint activity_course_fk
       FOREIGN KEY (course_id,department_id)
       REFERENCES course (course_id,department_id)
       ON DELETE RESTRICT,
    constraint activity_reservation_fk
       FOREIGN KEY(reservation_id)
       REFERENCES reservation(reservation_id)
       on DELETE RESTRICT
);

-- exam table
create table exam(
    exam_id BIGSERIAL not null primary key,
    duration int not null , -- with minutes
    exam_type varchar(25) not null ,
    course_id int not null ,
    department_id int not null , 
    constraint course_exam_fk
       FOREIGN key (course_id,department_id)
       REFERENCES course (course_id,department_id)
       ON DELETE RESTRICT
);


--takes an exam table
create table student_takes_an_exam (
    exam_id int not null,
    student_id int not null,
    statu status NOT NULL,
    primary key (exam_id,student_id),
    constraint exam_fk
       FOREIGN key(exam_id)
       REFERENCES exam(exam_id)
       ON DELETE RESTRICT,
    constraint student_fk
       FOREIGN key(student_id)
       REFERENCES student(student_id)
       ON DELETE RESTRICT   
);


--attendence table 

CREATE TABLE attendance_to_activities (
    student_id INT,
    activity_id INT,
    attendance_date DATE NOT NULL,
    statu status NOT NULL
        CHECK (statu IN ('present', 'absent')),
    PRIMARY KEY (student_id, activity_id, attendance_date),
    FOREIGN KEY (student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (activity_id)
        REFERENCES activity(activity_id)
        ON DELETE CASCADE
);

-- add group and section into students as an attribute

alter table student
add column group_id int ;

alter table student
add column section_id VARCHAR(1);

     --adding data then adding not null
 update  student
 set group_id =1
 where student_id in (1,3,6);
 update  student
 set group_id =1
 where student_id in (2,4,5);
     
alter table student
alter column group_id set not null;

update  student
set section_id='A';

alter table student
alter column section_id set not null;

 
-- Create  mark_Audit_Log table

CREATE TABLE mark_Audit_Log (
LogID SERIAL PRIMARY KEY,
OperationType VARCHAR(50) NOT NULL,
OperationTime TIMESTAMP NOT NULL,
Description TEXT
);

-- Create  attendance_Audit_Log table

CREATE TABLE attendance_Audit_Log (
LogID SERIAL PRIMARY KEY,
OperationType VARCHAR(50) NOT NULL,
OperationTime TIMESTAMP NOT NULL,
Description TEXT
);