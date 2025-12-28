--get_students_by_group(group_id)

CREATE function get_students_by_group (gid int) 
returns table (student_id int , last_name text , first_name text)
AS $$
SELECT student_id,last_name,first_name FROM student s 
WHERE s.group_id=gid;
$$
LANGUAGE sql;

--get_students_by_section(section_id)

create function get_students_by_section(se_id text)
returns table(student_id int , last_name text , first_name text)
as $$
SELECT student_id,last_name,first_name FROM student s 
where s.section_id=se_id;
$$
LANGUAGE sql;


--get_instructor_timetable(instructor_id)

create function get_instructor_timetable(inst_id int)
RETURNS table(reserv_date  DATE , start_time TIME , end_time TIME)
as $$
SELECT reserv_date,start_time,end_time 
FROM reservation r
WHERE r.instructor_id=inst_id;
$$
LANGUAGE sql;

--get_student_timetable( group_id)

create function get_student_timetable_group( gr_id int)
returns table (reserv_date  DATE , start_time TIME , end_time TIME)
as $$
SELECT reserv_date,start_time,end_time 
FROM reservation r
where (r.course_id ,r.department_id) in (
    SELECT course_id , department_id  FROM enrollment e
    where e.student_id in (
        SELECT student_id FROM student s
        where s.group_id = gr_id
     ) 
)

$$
LANGUAGE sql;


--get_student_timetable(section_id)

create function get_student_timetable_section(sect_id text)
returns table (reserv_date  DATE , start_time TIME , end_time TIME)
as $$
SELECT reserv_date,start_time,end_time 
FROM reservation r
where (r.course_id ,r.department_id) in (
    SELECT course_id , department_id  FROM enrollment e
    where e.student_id in (
        SELECT student_id FROM student s
        where s.section_id = sect_id
     ) 
)

$$
LANGUAGE sql;

--calculate_student_grade(student_id, course_id)

create function calculate_student_grade(stu_id int, cou_id int , dep_id int)
returns numeric
as $$
    SELECT avg(mark_value) from mark  m
    WHERE m.student_id = stu_id and (m.course_id,m.department_id) = row(cou_id,dep_id);
$$
LANGUAGE sql;

--get_students_passed_semester()

create function get_students_passed_semester()
returns table(student_id int , f_name text, l_name text)
as $$

  

$$
LANGUAGE sql

--The list of disqualifying mark by module

CREATE function disqualifying_mark_by_course()
RETURNS table (disqualifying_mark numeric , cou_id int , dep_id int)
as $$

SELECT 0.6*avg(mark_value),course_id,department_id
from mark
group by course_id,department_id ;

$$
LANGUAGE sql;

--The list of the average marks by course 

CREATE function avg_mark_by_course()
RETURNS table (disqualifying_mark numeric , cou_id int , dep_id int)
as $$

SELECT avg(mark_value),course_id,department_id
from mark
group by course_id,department_id ;

$$
LANGUAGE sql;

--The list of the average marks  by group

create function avg_mark_by_group()
returns table(avg_mark numeric , gr_id int , se_id varchar(1))
as $$
SELECT avg(mark_value),group_id,section_id 
from mark join student on mark.student_id=student.student_id
group by group_id,section_id;
$$
LANGUAGE sql;


--) The students who received a failing grade in a module.

create function tudents_who_received_a_failing_grade_in_a_module()
returns table(student_id int , course_id int , department_id int)
as $$

SELECT * from mark join student on mark.student_id=student.section_id
where course_id

$$
LANGUAGE sql

--get_students_passed_semester()