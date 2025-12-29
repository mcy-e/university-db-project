--(a) The list of students by group.

SELECT * from student
order by group_id;


--(b) The list of students by section.

SELECT * from student
order by section_id;

--(c) The time table of each instructor using the function.

SELECT * from get_instructor_timetable(inst_id int);

--(d) The time table of students by section, then by group.

SELECT * from get_student_timetable_group( gr_id int);
SELECT * from get_student_timetable_section( gr_id int);

--(e) The list of students who passed the semester.

SELECT * from get_students_passed_semester();

--(f) The list of disqualifying mark by module.

SELECT * from disqualifying_mark_by_course();

--(g) The list of the average marks by course and by group

SELECT * from avg_mark_by_course();

--(h) The students who received a failing grade in a module.

SELECT * from students_who_received_a_failing_grade_in_a_module();

--(i) The students eligible for a resit.

SELECT * from student where student_id not in (select * from get_students_passed_semester()); 



--(j) List of students excluded from the module

select * from get_List_of_students_AND_the_num_of_abcsence_from_the_module() where number_of_abscence>5;

