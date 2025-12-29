--15- get_average_of_students()

create function  get_average_of_students()
returns table(stu_id int , average numeric )
as $$
select student_id,avg(mark_value)
from mark
group by student_id;
$$
LANGUAGE sql ;

--1-get_students_by_group(group_id)

CREATE function get_students_by_group (gid int) 
returns table (student_id int , last_name text , first_name text)
AS $$
SELECT student_id,last_name,first_name FROM student s 
WHERE s.group_id=gid;
$$
LANGUAGE sql;

--2-get_students_by_section(section_id)

create function get_students_by_section(se_id text)
returns table(student_id int , last_name text , first_name text)
as $$
SELECT student_id,last_name,first_name FROM student s 
where s.section_id=se_id;
$$
LANGUAGE sql;


--3-get_instructor_timetable(instructor_id)

create function get_instructor_timetable(inst_id int)
RETURNS table(reserv_date  DATE , start_time TIME , end_time TIME)
as $$
SELECT reserv_date,start_time,end_time 
FROM reservation r
WHERE r.instructor_id=inst_id;
$$
LANGUAGE sql;

--4-get_student_timetable( group_id)

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


--5-get_student_timetable(section_id)

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

--6-calculate_student_grade(student_id, course_id)

create function calculate_student_grade(stu_id int, cou_id int , dep_id int)
returns numeric
as $$
    SELECT avg(mark_value) from mark  m
    WHERE m.student_id = stu_id and (m.course_id,m.department_id) = row(cou_id,dep_id);
$$
LANGUAGE sql;



--7-The list of disqualifying mark by module

CREATE function disqualifying_mark_by_course()
RETURNS table (disqualifying_mark numeric , cou_id int , dep_id int)
as $$

SELECT 0.6*avg(mark_value),course_id,department_id
from mark
group by course_id,department_id ;

$$
LANGUAGE sql;

---9The list of the average marks by course 

CREATE function avg_mark_by_course()
RETURNS table (disqualifying_mark numeric , cou_id int , dep_id int)
as $$

SELECT avg(mark_value),course_id,department_id
from mark
group by course_id,department_id ;

$$
LANGUAGE sql;

--10-The list of the average marks  by group

create function avg_mark_by_group()
returns table(avg_mark numeric , gr_id int , se_id varchar(1))
as $$
SELECT avg(mark_value),group_id,section_id 
from mark join student on mark.student_id=student.student_id
group by group_id,section_id;
$$
LANGUAGE sql;



--13-get_average_marks_by_course_group()

CREATE function get_average_marks_by_course_group()
returns table (avg_mark numeric , cou_id int , d_id int , g_id int , s_id text)
as $$

select avg(mark.mark_value),mark.course_id,mark.department_id , student.group_id , student.section_id
FROM mark
join student on mark.student_id=student.student_id
group by mark.course_id,mark.department_id , student.group_id , student.section_id ;

$$
LANGUAGE sql;


--14-get_List_of_students_AND_the_num_of_abcsence_from_the_module()

CREATE function get_List_of_students_AND_the_num_of_abcsence_from_the_module()
returns table (stu_id int,number_of_abscence int,  cou_id int , dep_id int)
as $$
SELECT attendance_to_activities.student_id ,count(attendance_to_activities.statu),course_id,department_id
from  activity 
join attendance_to_activities on activity.activity_id=attendance_to_activities.activity_id
WHERE attendance_to_activities.statu='absent' 
group by attendance_to_activities.student_id,activity.course_id,activity.department_id;
$$
LANGUAGE sql;


---11- The students who received a failing grade in a module.

create function students_who_received_a_failing_grade_in_a_module()
returns table(stud_id int  , course_id int , department_id int, mark_value numeric , disqualifying_mark numeric)
as $$

select mark.student_id,course_id, department_id,mark_value,disqualifying_mark
from mark
join student  on mark.student_id=student.student_id
join disqualifying_mark_by_course() d on (mark.course_id,mark.department_id)= row(d.cou_id,d.dep_id)
where mark.mark_value <= d.disqualifying_mark;

$$
LANGUAGE sql;

--12-get_students_passed_semester()

CREATE function get_students_passed_semester()
RETURNS table (stu_id int)
as $$
SELECT student_id 
from student
WHERE 
student_id not in( SELECT stud_id
 from students_who_received_a_failing_grade_in_a_module()                           
)
and
student_id not in(
    select stu_id
    from get_average_of_students()
    where average <10
)
and student_id not in(
    select stu_id from get_List_of_students_AND_the_num_of_abcsence_from_the_module() where number_of_abscence>5;
)
$$
LANGUAGE sql;